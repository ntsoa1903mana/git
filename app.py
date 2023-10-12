from fastapi import FastAPI
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
import random

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

## Store multiple OpenAI API keys in a list
api_keys = [
    "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",
    "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",
    "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",
    # Add more API keys as needed
    # Add more API keys as needed
]

# Shuffle the API keys at the beginning to ensure better randomness
random.shuffle(api_keys)

class PromptRequest(BaseModel):
    prompt: str
    fbid: str

@app.post("/generate_response")
async def generate_response(prompt_request: PromptRequest):
    user_prompt = prompt_request.prompt
    fbid = prompt_request.fbid

    # Choose the next API key in the shuffled list
    selected_api_key = api_keys.pop(0)
    api_keys.append(selected_api_key)  # Move the used key to the end of the list for rotation

    # Set the selected API key in the openai library
    openai.api_key = selected_api_key

    # Print the selected API key
    print(f"Selected API Key: {selected_api_key}")

    # Define messages for conversation
    messages = [
        {"role": "system", "content": "anwer the question directly add small value"},
        {"role": "user", "content": user_prompt},
    ]

    # Use OpenAI GPT-3 for chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Human: ", "AI: "]
    )

    response_content = chat_completion['choices'][0]['message']['content']

    return {"fbid": fbid, "response": response_content}

@app.get("/")
async def home():
    print("Home endpoint reached")
    return {"message": "OpenAI GPT-3 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
