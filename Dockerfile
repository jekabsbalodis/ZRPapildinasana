FROM python:3.10.8

RUN useradd zrapp

WORKDIR /home/zrapp

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY ZRApp.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP ZRApp.py

RUN chown -R zrapp:zrapp ./
USER zrapp

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]