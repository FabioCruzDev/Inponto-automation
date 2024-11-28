import unittest
from utils import is_weekend_or_holiday, send_whatsapp_msg
from tasks import get_dates, periodic_task_add_point_inponto
from freezegun import freeze_time
from datetime import datetime


# Classe de testes
class TestDataUtils(unittest.TestCase):
    
    # Testa a geração de data no formato ISO e log
    def test_gerar_data_com_variacao(self):
        _, iso_date, date_log = get_dates()
        
        # Testa se a data gerada no formato ISO está no padrão correto
        self.assertTrue(iso_date.endswith("-03:00"))  # Verifica o fuso horário correto
        self.assertEqual(len(iso_date), 32)  # Formato ISO correto tem 26 caracteres
        
        # Testa se a data legível para log está no formato correto
        self.assertTrue(date_log.count(":") == 2)  # Deve conter dois ":" (hora e minuto)
        self.assertEqual(len(date_log), 19)  # Formato "DD/MM/YYYY HH:MM:SS" tem 19 caracteres
    
    @freeze_time("2024-12-01 12:00:00")
    def test_verificar_final_de_semana(self):
        # Testa final de semana
        self.assertTrue(is_weekend_or_holiday(datetime.now()))
    
    @freeze_time("2024-12-25 12:00:00")
    def test_feriados(self):
        # Testa feriado
        self.assertTrue(is_weekend_or_holiday(datetime.now()))

    @freeze_time("2024-12-25 12:00:00")
    def test_task_bater_ponto_feriado(self):
        self.assertFalse(periodic_task_add_point_inponto())

    @freeze_time("2024-12-01 12:00:00")
    def test_task_bater_ponto_final_de_semana(self):
        self.assertFalse(periodic_task_add_point_inponto())

    def test_whatsapp_message(self):
        send_whatsapp_msg('GAY')