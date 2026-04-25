from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Code Review Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REVIEW_PROMPT = """You are a senior software engineer conducting a thorough code review.
Analyze the following code and provide structured feedback in these four sections:

1. 🐛 Bug Detection – Identify any bugs, logical errors, or potential runtime issues.
2. 💡 Improvement Suggestions – Suggest readability, maintainability, or design improvements.
3. ⚡ Optimization Tips – Point out performance bottlenecks or inefficiencies.
4. ✅ Best Practice Recommendations – Highlight any violations of coding standards or best practices.

Be specific and reference the relevant lines or patterns in the code.

Code to review:
{code}
"""

@app.get("/")
def root():
    return {"message": "Code Review Assistant API is running!"}

@app.post("/review/")
def review_code(code: str = Form(...), language: str = Form(default="auto")):
    if not code.strip():
        raise HTTPException(status_code=400, detail="Code input cannot be empty.")

    lang_hint = f"\nLanguage: {language}" if language != "auto" else ""
    prompt = REVIEW_PROMPT.format(code=code) + lang_hint

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        result = response.json()
        review = result.get("response", "").strip()

        if not review:
            return {"review": "No feedback was generated. Try again.", "language": language}

        return {"review": review, "language": language}

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Make sure it is running on port 11434."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
