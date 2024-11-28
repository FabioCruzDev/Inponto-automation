from twilio.rest import Client
from settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, MY_NUMBER

# Twilio dashboard : https://console.twilio.com
class WhatsAppApi():
    def __init__(self) -> None:
        self.account_sid = TWILIO_ACCOUNT_SID  # Substitua com seu SID
        self.auth_token = TWILIO_AUTH_TOKEN    # Substitua com seu Auth Token
        self.from_whatsapp_number = f'whatsapp:{TWILIO_PHONE_NUMBER}'  # O número de WhatsApp fornecido pelo Twilio
        self.to_whatsapp_number = f'whatsapp:{MY_NUMBER}'  # Seu número do WhatsApp (incluindo o código do país)
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, msg):
        message = self.client.messages.create(
            body=msg,
            from_=self.from_whatsapp_number,
            to=self.to_whatsapp_number
        )

        print(f'Mensagem enviada com sucesso! SID: {message.sid}')