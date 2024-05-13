import logging
import threading

import dispatch
import requests
from kafka import KafkaConsumer


BROKERS = ["localhost:9092", "localhost:9093", "localhost:9094"]
TOPIC = "topic1"
GROUP = "group1"


@dispatch.function
def send_message(url, payload):
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response


def forward_messages(url):
    consumer = KafkaConsumer(TOPIC, group_id=GROUP, bootstrap_servers=BROKERS)
    try:
        for message in consumer:
            send_message.dispatch(url, payload)
    finally:
        consumer.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"error: {sys.argv[0]} <URL>")
        exit(1)

    _, url = sys.argv

    # Start Dispatch in a background thread.
    thread = threading.Thread(target=dispatch.run)
    thread.start()

    # Forward messages from Kafka.
    forward_messages(url)
