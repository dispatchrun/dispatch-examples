import boto3
import dispatch

sqs = boto3.resource('sqs')

queue_name = 'dispatch-example-queue'
queue = sqs.get_queue_by_name(QueueName=queue_name)


# This worker consumes messages from the SQS queue and transfers them to
# Dispatch for processing.
@dispatch.worker
def consume_messages():
    while True:
        messages = queue.receive_messages()
        if not messages:
            continue
        batch = dispatch.batch()
        for m in messages:
            batch.add(handle_message, m.message_id, m.body)
        batch.dispatch()
        queue.delete_messages(Entries=[
            {'Id': m.message_id, 'ReceiptHandle': m.receipt_handle} for m in messages
        ])


# This function processes messages consumed from SQS, applying the reliability
# features of Dispatch such as retries, adaptive concurrency control, etc...
@dispatch.function
def handle_message(id: str, body: str):
    print('processing message:', id, body)


if __name__ == '__main__':
    dispatch.run()
