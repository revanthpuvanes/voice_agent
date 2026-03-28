from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .tools import run_analysis

MODEL = LiteLlm(model="mistral/mistral-small-latest")

root_agent = LlmAgent(
    name="VoiceBIAgent",
    model=MODEL,
    instruction="""
You are a BI analysis agent.

Call run_analysis using:
- csv_path
- question

Return only the analysis output.
""",
    tools=[run_analysis],
    output_key="analysis",
)