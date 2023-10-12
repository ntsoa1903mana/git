from fastapi import FastAPI
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Get the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Set the OpenAI API key in the openai library
openai.api_key = api_key

class PromptRequest(BaseModel):
    prompt: str
    fbid: str

async def generate_response(fbid, prompt):
    user_prompt = prompt  # Note: There's a syntax error in your code, extra quotation mark (")
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=user_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Human: ", "AI: "]
    )
    return response.choices[0].text

@app.post("/generate_response")
async def handle_generate_response(prompt_request: PromptRequest):
    user_prompt = prompt_request.prompt
    fbid = prompt_request.fbid
    response_text = await generate_response(fbid, user_prompt)
    return {"fbid": fbid, "response": response_text}

@app.get("/")
async def home():
    print("Home endpoint reached")
    return {"message": "openAI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
