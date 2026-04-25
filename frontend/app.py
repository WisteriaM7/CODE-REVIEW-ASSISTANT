import streamlit as st
import requests

st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Code Review Assistant")
st.markdown("Powered by **DeepSeek-Coder via Ollama** · FastAPI backend · Streamlit frontend")
st.divider()

LANGUAGES = [
    "auto", "Python", "JavaScript", "TypeScript", "Java", "C", "C++",
    "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "SQL", "Other"
]

SAMPLE_CODE = {
    "Python": '''\
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    average = total / len(numbers)
    return average

result = calculate_average([10, 20, 30])
print("Average:", result)
''',
    "JavaScript": '''\
function fetchUser(id) {
    fetch("https://api.example.com/users/" + id)
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
}

fetchUser(5)
'''
}

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("Select Language", LANGUAGES, index=0)

    st.divider()
    st.subheader("📌 Load Sample Code")
    sample_lang = st.selectbox("Pick a sample:", ["—"] + list(SAMPLE_CODE.keys()))
    load_sample = st.button("Load Sample", use_container_width=True)

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Paste your code in the editor\n2. Select the language (optional)\n3. Click **Review Code**\n4. Read the AI feedback")

# Main layout
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("📄 Your Code")

    default_code = ""
    if load_sample and sample_lang != "—":
        default_code = SAMPLE_CODE.get(sample_lang, "")

    code_input = st.text_area(
        "Paste your code here:",
        value=default_code,
        height=400,
        placeholder="# Paste any code here...\ndef hello():\n    print('Hello, World!')",
        label_visibility="collapsed"
    )

    char_count = len(code_input)
    line_count = code_input.count("\n") + 1 if code_input.strip() else 0
    st.caption(f"Lines: {line_count} · Characters: {char_count}")

    review_btn = st.button("🔍 Review Code", type="primary", use_container_width=True)

with right_col:
    st.subheader("📋 AI Review & Feedback")

    if review_btn:
        if not code_input.strip():
            st.warning("⚠️ Please paste some code before requesting a review.")
        else:
            with st.spinner("DeepSeek-Coder is reviewing your code..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/review/",
                        data={"code": code_input, "language": language},
                        timeout=150
                    )

                    if response.status_code == 200:
                        result = response.json()
                        review = result.get("review", "No feedback returned.")

                        st.success("✅ Review complete!")
                        st.divider()
                        st.markdown(review)

                    elif response.status_code == 400:
                        st.error(f"❌ {response.json().get('detail', 'Bad request.')}")
                    elif response.status_code == 503:
                        st.error("❌ Ollama is not running. Start it with `ollama serve`.")
                    else:
                        st.error(f"❌ Server error {response.status_code}: {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot reach the backend. Run `uvicorn backend.main:app --reload`.")
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. DeepSeek-Coder may need more time — try again.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
    else:
        st.info("👈 Paste your code on the left and click **Review Code** to get started.")
        st.markdown("""
**What you'll get:**
- 🐛 **Bug Detection** — Logical errors and runtime risks
- 💡 **Improvement Suggestions** — Readability and design
- ⚡ **Optimization Tips** — Performance and efficiency
- ✅ **Best Practice Recommendations** — Coding standards
        """)

st.divider()
st.caption("Ensure Ollama is running (`ollama serve`) and the backend is active (`uvicorn backend.main:app --reload`).")
