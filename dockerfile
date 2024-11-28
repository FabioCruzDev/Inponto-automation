FROM python:3.11.10

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD bash -c "celery -A inponto.tasks worker --loglevel=info & celery -A inponto.tasks beat --loglevel=info"
