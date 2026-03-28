from utils.mistral_client import call_mistral

def create_plan(question):
    prompt = f"""
Break this business question into 3-4 short analysis steps.

Question: {question}

Return ONLY bullet points.
"""

    response = call_mistral(prompt)
    return response