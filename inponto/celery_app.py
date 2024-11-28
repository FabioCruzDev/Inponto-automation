from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://inponto-redis:6379/0', backend='redis://inponto-redis:6379/0')

app.conf.beat_schedule = {
    'executar-8-da-manha': {
        'task': 'tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=8, minute=0),  # Variação de minutos
    },
    'executar-12-da-tarde': {
        'task': 'tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=12, minute=0),  # Variação de minutos
    },
    'executar-13:30': {
        'task': 'tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=13, minute=30),  # Variação em torno de 30 minutos
    },
    'executar-18-da-tarde': {
        'task': 'tasks.periodic_task_add_point_inponto',
        'schedule': crontab(hour=18, minute=0),  # Variação de minutos
    },
}

app.conf.update(
    timezone='America/Sao_Paulo',
    enable_utc=True,
    beat_max_loop_interval=1  # Define intervalo de 1 segundo
)
app.autodiscover_tasks()