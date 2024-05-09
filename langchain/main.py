import uvicorn
from fastapi import FastAPI
from dispatch.fastapi import Dispatch

from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

app = FastAPI()
dispatch = Dispatch(app)


@dataclass
class TranslateParams:
    phrase: str
    language: str


@dispatch.function
def translate_with(params: TranslateParams) -> dict:
    print(f"Translating '{params.phrase}' to '{params.language}'")

    template = """You are a helpful assistant who translates between languages.
    Translate the following phrase into the specified language: {phrase}
    Language: {language}"""
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", "Translate"),
        ]
    )
    chain = chat_prompt | ChatOpenAI()
    result = chain.invoke({
        "phrase": params.phrase,
        "language": params.language,
        })
    print("Translation: ", result.content)


@app.post("/translate")
def translate(phrase: str, language: str):
    translate_with.dispatch(TranslateParams(phrase=phrase, language=language))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
