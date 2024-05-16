# Fetch cat facts

Fetch random cat facts from a very unreliable API that frequently fails with 500.

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

## Run example

Start the application via the following command:

```
dispatch run -- python app.py
```

Note that requests to cat facts API may fail, but Dispatch automatically retries until successful response.
