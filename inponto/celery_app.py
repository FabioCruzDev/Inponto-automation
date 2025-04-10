from celery import Celery
from celery.schedules import crontab
from decouple import config

CELERY_BROKER_URL= config('CELERY_BROKER_URL')
app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)

app.conf.beat_schedule = {
    'executar-8-da-manha': {
        'task': 'inponto.tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=8, minute=0),  # Variação de minutos
    },
    'executar-12-da-tarde': {
        'task': 'inponto.tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=12, minute=0),  # Variação de minutos
    },
    'executar-13:30': {
        'task': 'inponto.tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=13, minute=30),  # Variação em torno de 30 minutos
    },
    'executar-18-da-tarde': {
        'task': 'inponto.tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=17, minute=30),  # Variação de minutos
    },
}

app.conf.update(
    timezone='America/Sao_Paulo',
    enable_utc=True,
    beat_max_loop_interval=1  # Define intervalo de 1 segundo
)
app.autodiscover_tasks(['inponto'])