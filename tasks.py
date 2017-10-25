from script.config import RABBITMQ_URL, MONGODB_URI, PING_URL
from celery import Celery
from celery.task import periodic_task
from celery.schedules import crontab
import requests
import os

rabbit_url = os.environ.get('RABBITMQ_BIGWIG_URL') or RABBITMQ_URL
mongodb_url = os.environ.get('MONGODB_URI') or MONGODB_URI

app = Celery('tasks', broker=rabbit_url)


@periodic_task(run_every=crontab(minute='*/1'))
def ping():
    try:
        requests.get(PING_URL)
        msg = 'PING SUCCSS!'

    except Exception as e:
        msg = 'PING ERROR!'

    return msg


@periodic_task(run_every=crontab(minute='*/15'))
def task_a():
    msg = {'msg': ''}
    try:
        # task script is here

        msg['msg'] = 'OK'
    except Exception as e:
        msg['msg'] = e

    return msg


'''
worker: celery worker -l info -A tasks:app --beat
'''
