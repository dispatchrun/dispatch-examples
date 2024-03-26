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

[Signup for Dispatch](https://console.dispatch.run/) and then
configure the API key:

```
export DISPATCH_API_KEY="<your-api-key>"
```

Generate a webhook to send data to by visiting:

https://webhook.site/

## Sync users the naive way

Sync users to the endpoint (replacing the URL with your webhook):

```
python sync_users.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd test-token
```

## Sync users with Dispatch

Start a local Dispatch endpoint:

```
DISPATCH_ENDPOINT_URL="http://localhost:8000" python dispatch_endpoint.py
```

Start an ngrok tunnel to make the local endpoint accessible to Dispatch:

```
ngrok http http://localhost:8000
```

Sync users with Dispatch (replacing the URLs with your tunnel URL / webhook):

```
DISPATCH_ENDPOINT_URL="https://c870-2001-8004-1b30-11ad-d42-e296-350b-ca8e.ngrok-free.app" \
  python sync_users_dispatch.py https://webhook.site/834f219e-87e3-4f32-8051-0019887b13dd test-token
```
