from utils.mistral_client import call_mistral

def verify(question, analysis, report):
    prompt = f"""
You are a strict data validator.

Your job is to verify if the report is supported by the analysis.

RULES:
- Do NOT trust the report blindly
- If report adds info not in analysis → mark as hallucination
- If unsure → say LOW confidence

Question: {question}
Analysis: {analysis}
Report: {report}

Return in this format:

Confidence: (High / Medium / Low)
Issues:
- bullet points of problems (if any)
Verdict:
- Is the report reliable? (Yes/No)
"""

    return call_mistral(prompt)