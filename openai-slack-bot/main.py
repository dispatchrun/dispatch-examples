from fastapi import FastAPI, Response
from dispatch.fastapi import Dispatch

from openai import OpenAI
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
from slack_sdk.signature import SignatureVerifier

import time
import os
from pydantic import BaseModel, ConfigDict
from typing import Union


class SlackBase(BaseModel):
    token: str


class SlackChallenge(SlackBase):
    challenge: str


class SlackMessageAppHome(SlackBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    team_id: str
    api_app_id: str
    event: dict
    type: str
    event_id: str
    event_time: int


app = FastAPI()
dispatch = Dispatch(app)

# OpenAI config
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Slack config
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])


@dispatch.function
def completion(msg: str) -> str:
    result = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": msg,
                }
            ],
            model="gpt-3.5-turbo",
    )
    return result.choices[0].message.content


@dispatch.function
def post_slack(msg: str) -> SlackResponse:
    return slack_client.chat_postMessage(
        channel="#notifications",
        text=msg,
    )


@dispatch.function
async def prompt_pipeline(msg: str):
    result = await completion(msg)
    await post_slack(result)


@app.post("/slack/events")
def slack_app(event: Union[SlackMessageAppHome, SlackChallenge]):
    if isinstance(event, SlackChallenge):
        return {"challenge": event.challenge}

    if isinstance(event, SlackMessageAppHome):
        print("event", event)
        print("event.event", event.event)
        print("event.event.text", event.event["text"])
        prompt_pipeline.dispatch(event.event["text"])
        return Response(status_code=200)

    return Response(status_code=404)


@app.get("/prompt")
async def prompt(msg: str):
    prompt_pipeline.dispatch(msg)
