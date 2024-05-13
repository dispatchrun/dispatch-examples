import os
import sys
import sqlite3
import threading
from contextlib import closing
from dataclasses import dataclass

import dispatch
import requests


FILE = "users.db"
BATCH_SIZE = 10


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    address: str
    email: str


def export_users_to_salesforce(db, instance_url, access_token):
    with closing(db.cursor()) as cursor:
        cursor.execute("SELECT id, first_name, last_name, address, email FROM users")
        batch = dispatch.batch()
        for row in cursor:
            batch.add(send_user_to_salesforce, User(*row), instance_url, access_token)
            if len(batch.calls) == BATCH_SIZE:
                batch.dispatch()
        if len(batch.calls) > 0:
            batch.dispatch()


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
    if len(sys.argv) != 3:
        print(f"error: {sys.argv[0]} <URL> <TOKEN>")
        exit(1)

    _, instance_url, access_token = sys.argv

    # Start Dispatch in a background thread.
    thread = threading.Thread(target=dispatch.run)
    thread.start()

    # Sync users.
    db = sqlite3.connect(FILE)
    try:
        with db:
            export_users_to_salesforce(db, instance_url, access_token)
    except KeyboardInterrupt:
        pass
    finally:
        db.close()
