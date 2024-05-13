# Forward messages from Kafka to endpoint

The example shows how to forward messages from Kafka to an endpoint.

## Setup

Setup a virtualenv with the required dependencies:

```
python3 -m venv env
source ./env/bin/activate
pip install -r requirements
```

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

## Setup Kafka

To setup an ephemeral Kafka cluster using [Docker Compose](https://docs.docker.com/compose/), run:

```
make up
```

Messages can be written to the cluster by starting a producer in the terminal

```
make producer
```

Enter one message per line and then hit enter to write it to the Kafka cluster.


## Forward messages from Kafka

To generate a test endpoint, visit:

[https://webhook.site/](https://webhook.site/)

Forward messages from Kafka to the endpoint using Dispatch (replacing the URL with your endpoint):

```
dispatch run -- python main.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd
```
