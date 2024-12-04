import requests
import json
import re

from loguru import logger

class Inponto():

    def __init__(self, **kwargs) -> None:
        logger.info('Init Inponto')
        self.login_url = 'https://inponto.vercel.app/api/login'
        self.hash = 'X9nmXeaNKYqKxO64Y5R7c' # ver como deixar dinamico, nao encontrei onde essa variavel é gerada, mas encontrei na pagina.
        self.authorization_tk_url = f'https://inponto.vercel.app/_next/data/{self.hash}/pt-BR/home.json'
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.payload = {"date":f"{kwargs['data']}","latitude":0,"longitude":0,"userData":{"device":"Desktop","gatewayMac":None,"ip":"","operatingSystem":"Windows 10"}}

    def execute(self):
        logger.info('execute')
        cookies = self.get_cookies()
        token = self.get_authorization_tk(cookies)
        self.add_point(cookies, token)

    def get_authorization_tk(self, cookies):
        logger.info('Capturando token de autorização.')
        data = requests.get(self.authorization_tk_url, cookies=cookies)

        if data.status_code == 404:
            self.get_new_hash(data)
            data = requests.get(self.authorization_tk_url, cookies=cookies)
            data.raise_for_status()

        resp_json = json.loads(data.content)
        return resp_json['pageProps']['persistData']['company']['fromToken']

    def get_new_hash(self, data):
        padrao = r'"buildId":"(.*?)"'
        resultado = re.search(padrao, data.content.decode('utf-8'))
        self.hash = resultado.group(1) if resultado else None
        self.authorization_tk_url = f'https://inponto.vercel.app/_next/data/{self.hash}/pt-BR/home.json'
    
    def get_cookies(self):
        logger.info('Realizando login.')
        login = requests.post(self.login_url, data={'email':self.user, 'password':self.password})
        self.get_company_and_emploee(login)
        login.raise_for_status()
        return login.cookies

    def get_company_and_emploee(self, login):
        logger.info('Capturando companyId e EmploeeId')
        response = json.loads(login.content)
        self.company_token = response['user']['companyId']
        self.employee_id = response['user']['employeeId']
    
    def add_point(self, cookies, token):
        logger.info('Registrando ponto')
        add_point_url = f'https://pontogo-api.herokuapp.com/add-point?company-token-pg={self.company_token}&employee-token-pg={self.employee_id}'
        add_point = requests.post(add_point_url, json=self.payload, cookies=cookies, headers={'authorization':token})
        add_point.raise_for_status()
