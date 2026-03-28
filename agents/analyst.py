from utils.mistral_client import call_mistral
from utils.code_runner import run_code

def analyze_data(df, question):
    prompt = f"""
You are a Python data analyst.

STRICT RULES:
- Return ONLY valid Python code
- NO explanations
- NO markdown
- NO comments
- Use dataframe name: df
- pandas is available as pd
- Use ONLY these columns: {list(df.columns)}
- Store final answer in variable: result
- Prefer human-readable outputs when possible
- If answering month-based questions, prefer month names over month numbers

Question: {question}
"""

    code = call_mistral(prompt)

    print("\n🧠 RAW OUTPUT:\n", code)

    output = run_code(code, df)

    return {
        "generated_code": code,
        "result": output
    }