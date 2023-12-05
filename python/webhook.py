import os
import requests


def send_webhook(user, event):
    # Customize those!
    endpoint = os.environ["DISPATCH_TO_URL"]
    api_key = os.environ["DISPATCH_API_KEY"]
    payload = {
        "from": "webhook",
        "to": user,
        "notification": {
            "event": event
        }
    }

    r = requests.post(f"https://dispatch.stealthrocket.cloud/{endpoint}",
                      headers = {
                          "Proxy-Authorization": f"Bearer {api_key}"
                      },
                      json=payload)
    r.raise_for_status()

    print(r.text)


if __name__ == '__main__':
    send_webhook('cool-person', {'action': 'starting to use', 'app': 'Dispatch'})
