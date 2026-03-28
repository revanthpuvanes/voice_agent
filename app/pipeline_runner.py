from agents.planner import create_plan
from agents.analyst import analyze_data
from agents.reporter import generate_report
from agents.verifier import verify
from agents.visualizer import create_charts


def run_pipeline(df, question: str) -> dict:
    plan = create_plan(question)
    analysis = analyze_data(df, question)
    report = generate_report(question, analysis["result"])
    verification = verify(question, analysis["result"], report)
    chart_paths = create_charts(df)

    return {
        "plan": plan,
        "analysis": analysis,
        "report": report,
        "verification": verification,
        "chart_paths": chart_paths,
    }