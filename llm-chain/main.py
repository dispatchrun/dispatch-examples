from dispatch.fastapi import Dispatch
from dispatch import gather
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import sqlite3


app = FastAPI()
dispatch = Dispatch(app)


@dispatch.function
def fetch_content_from(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return parse_html(resp.text)


def parse_html(content) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    all_text = soup.get_text(separator=' ', strip=True)
    return all_text


@dispatch.function
def summarize(doc: str) -> str:
    system = """You are a software engineer."""
    prompt = """
    You must summarize today's news from Hacker News in 3 sentences.
    """
    return prompt_openai(system, prompt, doc)


@dispatch.function
def classify(doc: str) -> str:
    system = """You are a tech journalist."""
    prompt = """
    Find a catchy title, in a single sentence,
    for today's news from Hacker News: {content}
    """
    return prompt_openai(system, prompt, doc)


def prompt_openai(system: str, prompt: str, content: str) -> str:
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", prompt),
        ]
    )
    openai = chat_prompt | ChatOpenAI()
    result = openai.invoke({"content": content})
    return result.content


@dispatch.function
def save_findings(summary: str, title: str):
    conn = sqlite3.connect('findings.db')

    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS finding (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT NOT NULL
            )
        ''')
        conn.execute('BEGIN TRANSACTION')
        cursor.execute('''
            INSERT INTO finding (title, summary)
            VALUES (?, ?)
        ''', (title, summary))
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
    finally:
        conn.close()


@dispatch.function
async def chain(url: str):
    # Fetch the content for a given URL with automated retries.
    doc = await fetch_content_from(url)

    # Execute two prompts in parallel and gather the results.
    (summary, title) = await gather(summarize(doc), classify(doc))

    # Save the findings in the DB.
    await save_findings(summary, title)


@app.post("/")
def index(url: str):
    chain.dispatch(url)
    return "OK"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
