# OpenAI Slack bot

> [!TIP]
> Check out our [Getting Started](https://docs.dispatch.run/getting-started/) guide to install and configure the Dispatch CLI.

Your personal assistant on Slack!

```
pip install -r requirements.txt
```

## Requirements

- Create and install a Slack app for the bot. See: https://slack.com/help/articles/202035138-Add-apps-to-your-Slack-workspace
- Create an bot toekn and signing secret
- Create an OpenAI account and token

## Configuration

Additional configuration required:

- `OPENAI_API_KEY`: provisioned OpenAI API key.
- `SLACK_BOT_TOKEN`: Token for the configured Slack app.
- `SLACK_SIGING_KEY`: Signing key for the configured Slack app.

## Run it

Run it locally with the Dispatch CLI:

```
dispatch run -- uvicorn main:app
```
