FROM python:3.11.7

WORKDIR /tg_bot_app

COPY ./bot_project .
COPY ./django_admin .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "bot.py"]
