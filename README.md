# 🔍 Code Review Assistant (DeepSeek-Coder)

An AI-powered code review tool using the **DeepSeek-Coder model** via Ollama, with a FastAPI backend and a split-panel Streamlit frontend. Paste any code and receive structured feedback across four categories — all locally, no API key needed.

---

## 🧠 Tech Stack

| Layer     | Technology                  |
|-----------|-----------------------------|
| LLM       | DeepSeek-Coder (via Ollama) |
| Backend   | FastAPI + Uvicorn           |
| Frontend  | Streamlit                   |
| Language  | Python 3.10+                |

---

## 📁 Project Structure

```
code-review-deepseek/
│
├── backend/
│   ├── __init__.py
│   └── main.py          # FastAPI app with /review/ endpoint
│
├── frontend/
│   └── app.py           # Streamlit split-panel UI
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/code-review-deepseek.git
cd code-review-deepseek
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama & Pull the DeepSeek-Coder Model

- Download Ollama from: https://ollama.com
- Pull the model:

```bash
ollama pull deepseek-coder
```

---

## 🚀 Running the App

Open **two separate terminals**:

**Terminal 1 — Start the Backend:**

```bash
uvicorn backend.main:app --reload
```

Backend runs at: `http://localhost:8000`

**Terminal 2 — Start the Frontend:**

```bash
streamlit run frontend/app.py
```

Frontend runs at: `http://localhost:8501`

---

## 📌 API Endpoints

| Method | Endpoint   | Description                         |
|--------|------------|-------------------------------------|
| GET    | `/`        | Health check                        |
| POST   | `/review/` | Submit code, returns structured review |

### Example Request (curl)

```bash
curl -X POST http://localhost:8000/review/ \
  -F "code=def add(a,b): return a+b" \
  -F "language=Python"
```

### Example Response

```json
{
  "review": "1. 🐛 Bug Detection\n No major bugs...\n2. 💡 Improvement Suggestions\n...",
  "language": "Python"
}
```

---

## ✅ Features

- Structured 4-section review: bugs, improvements, optimization, best practices
- Optional language selection (Python, JS, Java, Go, and more)
- Side-by-side split-panel UI — code on the left, review on the right
- Built-in sample code loader for quick testing
- Line count and character count display
- CORS-enabled FastAPI backend with proper error handling

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| Backend not connecting | Run `uvicorn backend.main:app --reload` |
| Ollama not responding | Run `ollama serve` and check with `ollama list` |
| Request timeout | DeepSeek-Coder is thorough — wait longer or try shorter code |
| Empty review returned | Retry — model may have had an off response |
| Model not found | Run `ollama pull deepseek-coder` first |
