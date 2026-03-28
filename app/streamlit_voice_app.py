import sys
import os
import tempfile
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

from voice_agent.transcribe import transcribe_audio
from voice_agent.speak import speak_text
from bi_adk_agent.agent import root_agent
from bi_adk_agent.runner import run_bi_adk

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Voice BI Analyst", layout="wide")
st.title("🎤 Voice-Powered BI Analyst")
st.write("Upload a CSV and record your business question.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
audio_input = st.audio_input("Record your business question")

if uploaded_file is not None and audio_input is not None:
    csv_path = OUTPUT_DIR / uploaded_file.name
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_input.getvalue())
        temp_audio_path = tmp.name

    st.audio(audio_input)

    with st.spinner("Transcribing audio..."):
        question = transcribe_audio(temp_audio_path)

    st.subheader("🗣️ Transcribed Question")
    st.write(question)

    try:
        with st.spinner("Running ADK BI analysis..."):
            adk_result = run_bi_adk(
                root_agent=root_agent,
                app_name="voice_bi_adk",
                user_id="streamlit_user",
                csv_path=str(csv_path),
                question=question,
            )
    except Exception as e:
        st.error(f"ADK pipeline failed: {e}")
        st.stop()

    state = adk_result.get("state", {})
    analysis = state.get("analysis", "")

    st.subheader("📊 Analysis Output")

    if isinstance(analysis, dict):
        st.code(analysis.get("generated_code", ""), language="python")
        st.write(analysis.get("result", ""))
    else:
        st.write(analysis)

    if isinstance(analysis, dict):
        spoken_summary = str(analysis.get("result", "Analysis completed."))[:300]
    else:
        spoken_summary = str(analysis)[:300]
    with st.spinner("Generating speech..."):
        output_audio = speak_text(spoken_summary)

    st.subheader("🔊 Spoken Output")
    if os.path.exists(output_audio) and os.path.getsize(output_audio) > 0:
        with open(output_audio, "rb") as audio_bytes:
            st.audio(audio_bytes.read(), format="audio/wav")
    else:
        st.warning(f"Audio file was not created correctly: {output_audio}")

    st.write(spoken_summary)
else:
    st.info("Upload a CSV and record your question to begin.")

# import sys
# import os
# import tempfile
# from pathlib import Path

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# import streamlit as st

# from voice_agent.transcribe import transcribe_audio
# from voice_agent.speak import speak_text
# from utils.data_loader import load_data
# from app.pipeline_runner import run_pipeline

# from google.adk.sessions import InMemorySessionService

# from bi_adk_agent.agent import root_agent
# from bi_adk_agent.runner import run_bi_adk

# OUTPUT_DIR = Path("outputs")
# OUTPUT_DIR.mkdir(exist_ok=True)

# st.set_page_config(page_title="Voice BI Analyst", layout="wide")
# st.title("🎤 Voice-Powered BI Analyst")
# st.write("Upload a CSV and record your question with the microphone.")

# uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
# audio_input = st.audio_input("Record your business question")

# # run_button = st.button("Run Voice Analysis")

# if uploaded_file is not None and audio_input is not None:
#     if uploaded_file is None:
#         st.error("Please upload a CSV file.")
#     elif audio_input is None:
#         st.error("Please record your question.")
#     else:
#         csv_path = OUTPUT_DIR / uploaded_file.name
#         with open(csv_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
#             tmp.write(audio_input.getvalue())
#             temp_audio_path = tmp.name

#         st.audio(audio_input)

#         try:
#             df = load_data(csv_path)
#         except Exception as e:
#             st.error(f"Error loading data: {e}")
#         else:
#             with st.spinner("Transcribing audio..."):
#                 question = transcribe_audio(temp_audio_path)

#             st.subheader("🗣️ Transcribed Question")
#             st.write(question)

#             with st.spinner("Running BI pipeline..."):
#                 result = run_pipeline(df, question)

#             col1, col2 = st.columns(2)

#             with col1:
#                 st.subheader("🧠 Plan")
#                 st.write(result["plan"])

#                 st.subheader("📊 Generated Code")
#                 st.code(result["analysis"]["generated_code"], language="python")

#                 st.subheader("📊 Analysis Result")
#                 st.write(result["analysis"]["result"])

#             with col2:
#                 st.subheader("📝 Report")
#                 st.write(result["report"])

#                 st.subheader("🛡️ Verification")
#                 st.write(result["verification"])

#             st.subheader("📈 Charts")
#             if result["chart_paths"]:
#                 for chart_path in result["chart_paths"]:
#                     st.image(chart_path, caption=Path(chart_path).name)
#             else:
#                 st.info("No charts were generated.")

#             spoken_summary = str(result["report"])[:800]

#             with st.spinner("Generating speech..."):
#                 output_audio = speak_text(spoken_summary)

#             st.subheader("🔊 Spoken Summary")
#             if os.path.exists(output_audio) and os.path.getsize(output_audio) > 0:
#                 with open(output_audio, "rb") as audio_bytes:
#                     st.audio(audio_bytes.read(), format="audio/wav")
#             else:
#                 st.warning(f"Audio file was not created correctly: {output_audio}")

#             st.write(spoken_summary)