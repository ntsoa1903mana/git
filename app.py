from fastapi import FastAPI, HTTPException
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

@app.post("/generate_response")
async def generate_response(prompt_request: PromptRequest):
    user_prompt = prompt_request.prompt
    print(user_prompt)
    fbid = prompt_request.fbid

    # Define messages for conversation
    messages = [
        {"role": "system", "content": "answer the question directlygive 1 exemple "},
        {"role": "user", "content": user_prompt},
    ]

    try:
        # Use OpenAI GPT-3 for chat completion
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["Human: ", "AI: "]
        )

        response_content = chat_completion['choices'][0]['message']['content']
        print(response_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error gen response")

    return {"fbid": fbid, "response": response_content}

@app.get("/")
async def home():
    print("Home endpoint reached")
    return {"message": "OpenAI GPT-3 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
