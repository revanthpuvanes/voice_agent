from pathlib import Path
from datetime import datetime

from utils.data_loader import load_data
from agents.planner import create_plan
from agents.analyst import analyze_data
from agents.reporter import generate_report
from agents.verifier import verify
from agents.visualizer import create_charts


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_run(question, plan, analysis, report, verification, chart_paths):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"run_{timestamp}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"QUESTION:\n{question}\n\n")
        f.write(f"PLAN:\n{plan}\n\n")
        f.write(f"GENERATED CODE:\n{analysis['generated_code']}\n\n")
        f.write(f"ANALYSIS RESULT:\n{analysis['result']}\n\n")
        f.write(f"REPORT:\n{report}\n\n")
        f.write(f"VERIFICATION:\n{verification}\n\n")
        f.write("CHARTS:\n")
        for path in chart_paths:
            f.write(f"- {path}\n")

    return file_path


def run_pipeline():
    print("\n=== Autonomous BI Analyst ===\n")

    data_path = input("Enter CSV path [default: data/sample.csv]: ").strip()
    if not data_path:
        data_path = "data/sample.csv"

    question = input("Enter your business question: ").strip()
    if not question:
        print("No question provided.")
        return

    try:
        df = load_data(data_path)
    except Exception as e:
        print(f"\nError loading data: {e}")
        return

    print("\n📌 QUESTION:", question)

    plan = create_plan(question)
    print("\n🧠 PLAN:\n", plan)

    analysis = analyze_data(df, question)
    print("\n📊 GENERATED CODE:\n", analysis["generated_code"])
    print("\n📊 ANALYSIS RESULT:\n", analysis["result"])

    report = generate_report(question, analysis["result"])
    print("\n📝 REPORT:\n", report)

    verification = verify(question, analysis["result"], report)
    print("\n🛡️ VERIFICATION:\n", verification)

    chart_paths = create_charts(df)
    print("\n📈 CHARTS SAVED:")
    for path in chart_paths:
        print(path)

    saved_file = save_run(question, plan, analysis, report, verification, chart_paths)
    print(f"\n💾 Run saved to: {saved_file}")


if __name__ == "__main__":
    run_pipeline()