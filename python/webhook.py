import os
import requests

def send_webhook(src, dst, msg):
    endpoint = os.environ["DISPATCH_TO_URL"].removeprefix('https://')
    api_key = os.environ["DISPATCH_API_KEY"]
    payload = {
        "from": src,
        "to": dst,
        "message": msg
    }

    r = requests.post(f"https://dispatch.stealthrocket.cloud/{endpoint}",
                      headers = {
                          "Proxy-Authorization": f"Bearer {api_key}"
                      },
                      json=payload)
    r.raise_for_status()
    print(r.text.strip())


if __name__ == '__main__':
    send_webhook('example', 'webhook', 'hello, world!')
