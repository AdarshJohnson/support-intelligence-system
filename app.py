from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import json
import time
from logic import apply_business_logic

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY:", API_KEY)

MODELS = [
    "openrouter/free",
    "google/gemma-3-12b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "qwen/qwen3-8b:free",
    "nvidia/llama-3.1-nemotron-nano-8b-v1:free"
]

class Query(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "AI Support Triage API is running"}


@app.post("/analyze")
def analyze(query: Query):

    prompt = open("prompt.txt").read()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query.message}
        ]
    }

    result = None
    used_model = None
    raw_content = None

    # Try each model until one returns valid content
    for model in MODELS:
        data["model"] = model
        print(f"Trying model: {model}")

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            result = response.json()

            # Skip if API returned an error
            if "error" in result:
                print(f"Model {model} error: {result['error'].get('message', 'Unknown')}")
                time.sleep(2)
                continue

            # Skip if content is null or empty
            content = result["choices"][0]["message"]["content"]
            if not content or content.strip() == "":
                print(f"Model {model} returned empty content, trying next...")
                time.sleep(2)
                continue

            # We have valid content
            raw_content = content
            used_model = model
            print(f"Success with model: {model}")
            break

        except Exception as e:
            print(f"Exception with model {model}: {str(e)}")
            time.sleep(2)
            continue

    # All models failed
    if not raw_content:
        return {
            "error": "All models failed or returned empty responses. Please try again later.",
            "raw": result
        }

    # Parse AI JSON response
    try:
        output = raw_content.strip()

        # Strip markdown code blocks if model added them
        if output.startswith("```json"):
            output = output[7:]
        elif output.startswith("```"):
            output = output[3:]
        if output.endswith("```"):
            output = output[:-3]
        output = output.strip()

        parsed = json.loads(output)

    except Exception as e:
        return {
            "error": "Model did not return valid JSON",
            "raw_content": raw_content,
            "exception": str(e)
        }

    # Apply business logic
    final = apply_business_logic(parsed)
    final["model_used"] = used_model

    return final