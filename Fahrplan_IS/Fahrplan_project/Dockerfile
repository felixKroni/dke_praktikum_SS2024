FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY app app
COPY app.py config.py boot.sh ./
#RUN chmod a+x boot.sh

ENV FLASK_APP app.py
RUN flask

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
