import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from datetime import datetime
import streamlit as st

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


st.set_page_config(page_title="Autonomous BI Analyst", layout="wide")
st.title("🧠 Autonomous BI Analyst")
st.write("Upload a CSV and ask a business question.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
question = st.text_input("Enter your business question")

run_button = st.button("Run Analysis")

if run_button:
    if uploaded_file is None:
        st.error("Please upload a CSV file.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        temp_path = OUTPUT_DIR / uploaded_file.name
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            df = load_data(temp_path)
        except Exception as e:
            st.error(f"Error loading data: {e}")
        else:
            with st.spinner("Running analysis..."):
                plan = create_plan(question)
                analysis = analyze_data(df, question)
                report = generate_report(question, analysis["result"])
                verification = verify(question, analysis["result"], report)
                chart_paths = create_charts(df)
                saved_file = save_run(
                    question, plan, analysis, report, verification, chart_paths
                )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📌 Question")
                st.write(question)

                st.subheader("🧠 Plan")
                st.write(plan)

                st.subheader("📊 Generated Code")
                st.code(analysis["generated_code"], language="python")

                st.subheader("📊 Analysis Result")
                st.write(analysis["result"])

            with col2:
                st.subheader("📝 Report")
                st.write(report)

                st.subheader("🛡️ Verification")
                st.write(verification)

                st.subheader("💾 Saved Run")
                st.write(str(saved_file))

            st.subheader("📈 Charts")
            if chart_paths:
                for chart_path in chart_paths:
                    st.image(chart_path, caption=Path(chart_path).name)
            else:
                st.info("No charts were generated.")