import dispatch
import requests


@dispatch.function
def fetch_cat_fact():
    response = requests.get("https://cat-facts.dispatch.run")
    response.raise_for_status()
    print(response.text)


def main():
    # Dispatch a call to `fetch_cat_fact`
    fetch_cat_fact.dispatch()


# Initialize Dispatch and call `main` when done
dispatch.run(main)
