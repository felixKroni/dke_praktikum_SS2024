FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography
RUN pip install gevent


COPY app app
COPY app.py config.py ./


ENV FLASK_APP app.py
RUN flask

EXPOSE 5000
ENTRYPOINT ["gunicorn", "-k", "gevent", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]