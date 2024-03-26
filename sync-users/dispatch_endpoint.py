import sys
import sqlite3
import threading
import requests
import uvicorn
from fastapi import FastAPI
from dispatch.fastapi import Dispatch
from contextlib import closing
from dataclasses import dataclass


app = FastAPI()
dispatch = Dispatch(app)


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    address: str
    email: str


@dispatch.function
def send_user_to_salesforce(user, instance_url, access_token):
    url = f"{instance_url}/services/data/v52.0/sobjects/User"

    headers = {"Authorization": f"Bearer {access_token}"}

    data = {
        "FirstName": user.first_name,
        "LastName": user.last_name,
        "Address": user.address,
        "Email": user.email,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response


if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_level="info")
