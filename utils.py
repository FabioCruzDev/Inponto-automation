import holidays
from loguru import logger
from whatsapp_app.whatsapp import WhatsAppApi

def is_weekend_or_holiday(date):
    today = date.date()
    if today.weekday() in (5,6): # 5 = Sabado, 6 = Domingo
        logger.info('Hoje é final de semana.')
        return True
    elif today in holidays.Brazil():
        logger.info('Hoje é feriado.')
        return True
    
    return False

def send_whatsapp_msg(msg):
    whatsapp = WhatsAppApi()
    whatsapp.send_message(msg)
    return True