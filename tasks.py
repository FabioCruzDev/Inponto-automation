from celery_app import app
from inponto.main import Inponto
from datetime import datetime, timedelta, timezone
from loguru import logger
import random
from utils import is_weekend_or_holiday, send_whatsapp_msg
from settings import USER, PASSWORD

@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=60, retry_jitter=True, retry_kwargs={'max_retries': 5})
def periodic_task_add_point_inponto(_):
    logger.info('Iniciando task bater ponto.')
    date, iso_date, date_log = get_dates()

    if not is_weekend_or_holiday(date):
        logger.info(f'Horario definido: {date_log}')
        try:
            inponto = Inponto(user=USER, password=PASSWORD, data=iso_date)
            inponto.execute()
            send_whatsapp_msg(f'Ponto batido as {date_log}')
            logger.success('execução concluida com sucesso.')
            return True
        except:
            send_whatsapp_msg(f'Erro ao bater ponto as {date_log}')
            raise Exception('Erro ao bater ponto.')
    
    return False

def get_dates():
    variacao = random.randint(-5, 5)
    now = datetime.now(timezone(timedelta(hours=-3)))
    date = now + timedelta(minutes=variacao)
    iso_date = date.isoformat()
    date_log = date.strftime("%d/%m/%Y %H:%M:%S")
    return date,iso_date,date_log

