FROM python:slim

RUN useradd zrapp

WORKDIR /home/zrapp

COPY requirements.txt requirements.txt
RUN mkdir db
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY zrapp.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP zrapp.py
ENV FLASK_CONFIG docker

RUN chown -R zrapp:zrapp ./
USER zrapp

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]