from kafka import KafkaConsumer

brokers = ["localhost:9092", "localhost:9093", "localhost:9094"]
topic = "topic1"
group_id = "group1"

consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=brokers)

try:
    for message in consumer:
        print(message.value)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
