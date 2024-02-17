FROM python:3.11.7

WORKDIR /tg_bot_app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "manage.py", "runserver", "0:8000"]
