import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import ollama
import json

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", status_code=200)
async def rate_resume(data: dict):
    print(f"working {data}")
    context_prompt = """
    You are a Resume analyzer. Rate the resume and provide:
    1. A score from 0-100
    2. Overall feedback (2-3 sentences)
    3. Top 3-5 specific recommendations for improvement

    Format your response EXACTLY as JSON:
    {
      "score": <number>,
      "feedback": "<string>",
      "suggestions": ["<string>", "<string>", ...]
    }

    """
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": context_prompt},
            {"role": "user", "content": data["resume"]}
        ]
    )
    resume_rating = response["message"]["content"]
    resume_rating_parsed = json.loads(resume_rating)
    return resume_rating_parsed


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)