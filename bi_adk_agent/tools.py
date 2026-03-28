from agents.analyst import analyze_data
from utils.data_loader import load_data


def run_analysis(csv_path: str, question: str) -> dict:
    df = load_data(csv_path)
    analysis = analyze_data(df, question)
    return {
        "generated_code": analysis.get("generated_code", ""),
        "result": str(analysis.get("result", "")),
    }