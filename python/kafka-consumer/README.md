# Forward messages from Kafka to endpoint

[Apache Kafka](https://kafka.apache.org/) is an open-source distributed event streaming
platform used by thousands of companies for high-performance data pipelines, streaming analytics,
data integration, and mission-critical applications.

Although Kafka has many desirable attributes as a message queue, including its excellent
performance and durability characteristics, it suffers from a serious flaw with some uses cases;
head-of-line blocking. When message processing fails with a temporary error, the consumer
cannot make progress on subsequent messages in the queue. It must either retry the operation
inline, or copy the message to another location so that it can continue to make progress.

When paired with Dispatch, Kafka's head-of-line blocking flaw is no longer an issue. Dispatch
takes over scheduling the processing of each message, allowing the consumer to make progress
even when there are issues that prevent messages from being processed.

In this example, we look at how to send messages from Kafka to an endpoint. Since there is a
network between the consumer (this script) and the endpoint, the request to send the message
may fail. This failure is automatically handled by Dispatch. Dispatch also automatically
adapts processing concurrency to match the capabilities of the endpoint. The user does not
have to think about manual retries to ensure messages get through, and to think about
throttling consumption of messages to ensure the endpoint isn't overloaded.

## Setup

### Setup Dispatch

Install the [Dispatch CLI](https://github.com/dispatchrun/dispatch):

```
brew tap dispatchrun/dispatch
brew install dispatch
```

For other ways to install, see the [Dispatch CLI README](https://github.com/dispatchrun/dispatch).

Login to Dispatch, or create a free account:

```
dispatch login
```

### Setup Kafka

To setup an ephemeral Kafka cluster using [Docker Compose](https://docs.docker.com/compose/), run:

```
make up
```

Messages can be written to the cluster by starting a producer in the terminal

```
make producer
```

Enter one message per line and then hit enter to write it to the Kafka cluster.

### Setup the example

Setup a virtualenv with the required dependencies:

```
python3 -m venv env
source ./env/bin/activate
pip install -r requirements
```

### Setup a temporary endpoint

To generate a test endpoint, visit:

[https://webhook.site/](https://webhook.site/)

## Forward messages from Kafka

Forward messages from Kafka to the endpoint using Dispatch (replacing the URL with your endpoint):

```
dispatch run -- python main.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd
```
