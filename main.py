from fastapi import FastAPI
app = FastAPI()

from openai import OpenAI

import uvicorn
from pydantic import BaseModel
import os
from config import api_key, assistant_id

class Body(BaseModel):
    text: str

api_key = os.environ['OPENAI_API']

# Initialize OpenAI API
client = OpenAI(api_key=api_key)

# get, post, put, and delete actions

@app.get("/")
def welcome():
   return {"message": "Hello, this is the LLM ChatGPT API V2!"}

@app.get("/home")
def home():
   return {"message": "Welcome to the LLM ChatGPT API! Home!"}

@app.post("/dummy") 
def demo_function(data):
    return {"message": data}

@app.post("/generate-llm-response")
def generate(body: Body):
    prompt = body.text # user input
    thread = client.beta.threads.create()
    print(prompt)
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id=assistant_id
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            print(text)
            break;
    response = {
        "llm_response": text
    }
    return response   

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=80)