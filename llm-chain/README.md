# How to chain LLMs with Dispatch

> [!TIP]
> Check out our [Getting Started](https://docs.dispatch.run/getting-started/) guide to install and configure the Dispatch CLI.

This example demonstrates how to chain requests to LLM APIs. For the example, we use the [Langchain Python SDK](https://www.langchain.com/) to interact with OpenAI.

```
pip install -r requirements.txt
```

You will need to create and expose an [OpenAI API key](https://platform.openai.com/api-keys):

```
export OPENAI_API_KEY=sk-...
```

To run the app:

```
dispatch run -- python3 main.py
```

Then ask for a translation:

```
curl -X POST "http://localhost:8000?url=https://news.ycombinator.com"
```

The chain will fetch the content of the passed URL, summarize it, create a catchy title and write the result into a sqlite DB.

Check the result:

```
sqlite3 -json findings.db "select * from finding;" | jq .
```
