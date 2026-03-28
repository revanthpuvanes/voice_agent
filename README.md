# 🎤 TalkToData - Voice Analytics Agent (Google ADK + Whisper + Mistral AI)

A **voice-enabled business intelligence assistant** that allows users to ask questions about data using natural speech and receive analytical insights instantly.

This project combines **speech recognition, multi-agent orchestration, and data analysis** into a single interactive system.

---

## 🚀 Features

- 🎤 **Live Voice Input** - Ask questions using your microphone  
- 🧠 **AI-Powered Analysis** - Multi-agent workflow using Google ADK  
- 📊 **Data Processing** - Executes analysis on CSV datasets using pandas  
- 🔊 **Spoken Output** - Responses are read aloud using offline TTS  
- ⚡ **Real-time Interaction** - End-to-end pipeline from voice → insights → speech  

---

## 🧠 Architecture
User Voice Input
↓
Whisper (Speech-to-Text)
↓
Google ADK Agent
↓
BI Analysis Tool (pandas execution)
↓
Text Response
↓
pyttsx3 (Text-to-Speech)

---

## 🛠️ Tech Stack

- Agent Orchestration: Google ADK  
- LLM Backend: Mistral AI  
- Speech-to-Text: Whisper  
- Text-to-Speech: pyttsx3 (offline)  
- Frontend: Streamlit  
- Data Processing: pandas, matplotlib  

---

## 📦 Installation

### 1. Clone the repo
```
git clone https://github.com/your-username/voice-bi-analyst.git
cd voice-bi-analyst
```

### 2. Create virtual environment
```
python3 -m venv .venv
source .venv/bin/activate 
```
### 3. Install dependencies
```
pip install -r requirements.txt
pip install google-adk litellm openai-whisper pyttsx3 streamlit
```
### 4. Install system dependencies (Ubuntu)
```
sudo apt update
sudo apt install -y ffmpeg espeak-ng libespeak1
```
## 🔑 Environment Variables
Create a .env file:
```
MISTRAL_API_KEY=your_api_key_here
```
## ▶️ Run the App
```
PYTHONPATH=. streamlit run app/streamlit_voice_app.py
```
## 🧪 How to Use
1. Upload a CSV dataset
2. Click the microphone and ask a question
3. The system will:
   - transcribe your voice
   - run analysis using AI agents
   - display results
   - speak the answer

## 📁 Project Structure
```
voice-bi-analyst/
├── app/
│   └── streamlit_voice_app.py
├── agents/
├── utils/
├── voice_agent/
│   ├── transcribe.py
│   └── speak.py
├── bi_adk_agent/
│   ├── agent.py
│   ├── tools.py
│   └── runner.py
├── data/
├── outputs/
└── requirements.txt
```
## ⚠️ Limitations
- Dependent on Mistral API rate limits
- Whisper runs on CPU (slower inference)
- Analysis execution uses dynamic code generation (not sandboxed)

## 🔮 Future Improvements
- Structured JSON outputs for agents
- Multi-turn conversational memory
- Real-time continuous voice interaction
- Safer execution environment (sandboxing)
- Deployment with Docker/cloud hosting
