FROM python:3.11.10

# Copiar os arquivos do projeto para dentro do container
WORKDIR /app
COPY . /app

# Instalar as dependências do projeto (se aplicável)
RUN pip install -r requirements.txt

# Comando padrão, será sobrescrito pelo docker-compose
CMD bash -c "celery -A tasks worker --loglevel=info & celery -A tasks beat --loglevel=info"
