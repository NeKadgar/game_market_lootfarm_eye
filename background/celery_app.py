from celery import Celery, Task
from datetime import timedelta
from kombu import Exchange, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import config

app = Celery(__name__, include=['background.tasks'], )

app.conf.broker_url = config.CELERY_BROKER_URL
app.conf.result_backend = config.CELERY_RESULT_BACKEND

default_exchange = Exchange("default_lootfarm", type="direct")  # Internal connections queue
providers_exchange = Exchange("providers_exchange", type="direct")  # External connections queue

app.conf.task_queues = (
    Queue("lootfarm_queue", default_exchange, routing_key="lootfarm_route"), # noqa
)

engine = create_engine(config.DATABASE_URL_SYNC)


class SQLAlchemyTask(Task):
    _session = None

    def _set_engine_session(self):
        session = sessionmaker(engine)
        with session() as db_session:
            self._session = db_session

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.commit()
            self._session.close()

    @property
    def session(self):
        if self._session is None:
            self._set_engine_session()
        return self._session


app.conf.beat_schedule = {
    # Executes every 2 hours
    "parse": {
        "task": "background.tasks.parser.parse",
        "schedule": timedelta(minutes=30),
        'options': {
            'queue': 'lootfarm_queue',
            # 'expires': timedelta(hours=2),
        },
    },
}
