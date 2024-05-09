# Langchain

Simple example of using Dispatch to build a durable Langchain based application.

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
curl -X POST "http://localhost:8000/translate?phrase=hello%20world&language=Spanish"
```

You will see the result in the logs:

```
python3  | Translating 'hello world' to 'spanish'
python3  | Translation:  Hola mundo
```
