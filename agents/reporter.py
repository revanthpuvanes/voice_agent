from utils.mistral_client import call_mistral

def generate_report(question, analysis):
    prompt = f"""
You are a business analyst.

STRICT RULES:
- Use ONLY the provided analysis
- Do NOT invent causes
- Do NOT assume missing data
- If the result is a month number, convert it to month name
- Keep output short and clear

Question: {question}
Analysis: {analysis}

Return in this format:

Key finding:
Reason:
Recommendation:
"""
    return call_mistral(prompt)