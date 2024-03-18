import logging
import threading

import requests
from fastapi import FastAPI
from dispatch.fastapi import Dispatch
from kafka import KafkaConsumer


logging.basicConfig(level=logging.WARNING)


BROKERS = ["localhost:9092", "localhost:9093", "localhost:9094"]
TOPIC = "topic1"
GROUP = "group1"

URL = "https://c8955422caa67b92b294cef222afe991.m.pipedream.net"


app = FastAPI()
dispatch = Dispatch(app)


@dispatch.function
def send_message(payload):
    response = requests.post(URL, data=payload)
    response.raise_for_status()
    return resopnse


def consume_messages():
    consumer = KafkaConsumer(TOPIC, group_id=GROUP, bootstrap_servers=BROKERS)
    try:
        for message in consumer:
            forward_batch([message])
    finally:
        consumer.close()


def forward_batch(messages):
    batch = dispatch.batch()
    for message in messages:
        batch.add(send_message, message.value)
    batch.dispatch()


# Consume messages in the background.
thread = threading.Thread(target=consume_messages)
thread.start()
