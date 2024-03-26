# Sync users from a database

The example shows how to sync users from a database to an endpoint.

## Setup

Setup a virtualenv with the required dependencies:

```
python3 -m venv env
source ./env/bin/activate
pip install -r requirements
```

Generate a fake user database:

```console
make users
```

Generate a test endpoint by visiting:

```
https://webhook.site/
```

## Sync users the naive way

Sync users to the endpoint (replacing the URL with your endpoint):

```
python sync_users.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd test-token
```

