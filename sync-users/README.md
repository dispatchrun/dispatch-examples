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

## Sync users the naive way

Generate a webhook to send data to by visiting:

[https://webhook.site/](https://webhook.site/)

Sync users to the endpoint (replacing the URL with your webhook):

```
python sync_users.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd test-token
```

## Sync users with Dispatch

Sync users to the endpoint using Dispatch (replacing the URL with your webhook):

```
dispatch run -- python sync_users_dispatch.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd test-token
```
