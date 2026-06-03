import streamlit as st
import os
import sys
import time
import subprocess
from dotenv import load_dotenv

# Dynamically pull credentials out of the local tracking vault
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent import AutonomousFixAgent
from src.git_tools import JarvisGitEngine

st.set_page_config(
    page_title="J.A.R.V.I.S. Project Factory OS",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling Matrix
st.markdown("""
    <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { 
            background-color: #10b981; color: white; border-radius: 4px; 
            border: 1px solid #34d399; box-shadow: 0px 0px 10px rgba(16,185,129,0.3);
            font-weight: bold; width: 100%; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #34d399; color: black; box-shadow: 0px 0px 20px #34d399; }
        .jarvis-banner { 
            padding: 20px; border: 1px solid #10b981; border-radius: 8px; 
            background-color: #161b22; box-shadow: 0px 0px 15px rgba(16, 185, 129, 0.15);
            margin-bottom: 25px;
        }
        .pitch-card {
            padding: 20px; border: 1px solid #30363d; border-radius: 8px;
            background-color: #161b22; height: 100%; transition: 0.3s;
        }
        .pitch-card:hover { border-color: #10b981; box-shadow: 0px 0px 15px rgba(16, 185, 129, 0.1); }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: MODEL SELECTION & OVERRIDE CONTROLS ---
with st.sidebar:
    st.markdown("### 🛠️ Model Orchestrator")
    selected_gemini = st.selectbox("🧠 Primary Gemini LLM:", options=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-pro-exp", "gemini-3.5-flash", "gemini-3.1-pro", "gemini-3.1-flash-lite"], index=0)
    selected_groq = st.selectbox("🎛️ Fallback Groq LLM:", options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-3.2-1b-preview", "mixtral-8x7b-32768"], index=0)
    
    st.markdown("---")
    st.markdown("### ⚙️ Operational Guards")
    # NEW: Toggle to bypass local tests for multi-lingual builds (Next.js/React)
    skip_verification = st.toggle("🚀 Protocol Override: Skip Local Tests", value=False, help="Enable this if your local machine lacks the runtime (e.g. Node/NPM) for the generated stack.")

    st.markdown("---")
    st.markdown("### 📊 Operational Telemetry")
    if "telemetry_history" in st.session_state and st.session_state.telemetry_history:
        for index, entry in enumerate(reversed(st.session_state.telemetry_history)):
            status_color = "🟢" if entry["status"] == "Success" else "🟡"
            with st.expander(f"{status_color} {entry['stage']}", expanded=(index==0)):
                st.caption(f"Model: {entry['model']} | Time: {entry['duration_sec']}s | Tokens: {entry['total_tokens']}")
    else:
        st.info("No active telemetry.")

# Initialize Engines
current_workspace = os.getcwd()
agent = AutonomousFixAgent(target_dir=current_workspace, gemini_model=selected_gemini, groq_model=selected_groq)
git_engine = JarvisGitEngine(repo_path=current_workspace)

if "pitches" not in st.session_state: st.session_state.pitches = []
if "selected_pitch" not in st.session_state: st.session_state.selected_pitch = None

# Header
st.markdown(f'<div class="jarvis-banner"><h1 style="color: #10b981; margin:0; font-family:monospace;">J.A.R.V.I.S. // PROJECT FACTORY</h1><p style="color: #8b949e; margin:5px 0 0 0;">STACK: <b>MULTI-LINGUAL (NEXT.JS, REACT, NODE, PYTHON)</b></p></div>', unsafe_allow_html=True)

user_idea = st.text_input("👑 Enter concept:", placeholder="e.g. A crypto tracking app in React")

if st.button("🧠 Brainstorm"):
    if user_idea:
        with st.spinner("Processing..."):
            st.session_state.pitches = agent.generate_project_pitches(user_idea)
            st.session_state.telemetry_history = agent.telemetry_history.copy()
            st.success("Pitches Ready.")

# Pitch Display
if st.session_state.pitches:
    cols = st.columns(3)
    for index, pitch in enumerate(st.session_state.pitches):
        with cols[index]:
            st.markdown(f'<div class="pitch-card"><h3 style="color:#10b981;">{pitch["title"]}</h3><p style="font-size:12px; color:#00f0ff;">Stack: {pitch.get("tech_stack", "N/A")}</p><p style="font-size:13px;">{pitch["description"]}</p></div>', unsafe_allow_html=True)
            if st.button(f"🏗️ Build #{pitch['id']}", key=f"sel_{pitch['id']}"):
                st.session_state.selected_pitch = pitch

# Deployment
if st.session_state.selected_pitch:
    chosen = st.session_state.selected_pitch
    st.markdown("---")
    if st.button(f"🚀 Deploy {chosen['title']} to GitHub"):
        progress = st.progress(0)
        status = st.empty()
        
        # 1. Build
        status.text("🤖 Step 1/4: Synthesizing Code & README...")
        progress.progress(25)
        clean_slug = chosen['title'].replace(" ", "-").lower()
        project_path = os.path.join(current_workspace, "creations", clean_slug)
        os.makedirs(project_path, exist_ok=True)
        agent.build_and_deploy_project(chosen, local_project_path=project_path)
        st.session_state.telemetry_history = agent.telemetry_history.copy()
        
        # 2. Verify
        status.text("🔍 Step 2/4: Local Verification Suite...")
        progress.progress(50)
        
        if skip_verification:
            test_passed = True
            test_output = "Manual Protocol Override: Local Verification Skipped."
        else:
            test_cmd = chosen.get("test_command", [])
            if not test_cmd:
                test_cmd = [sys.executable, "-m", "pytest"] if any(f.endswith(".py") for f in chosen['proposed_files']) else []
            
            if test_cmd:
                try:
                    res = subprocess.run(test_cmd, cwd=project_path, capture_output=True, text=True, shell=(os.name=='nt'))
                    test_passed = (res.returncode == 0)
                    test_output = res.stdout if res.stdout else res.stderr
                except Exception as e:
                    test_passed = False
                    test_output = str(e)
            else:
                test_passed = True
                test_output = "No test suite defined for this stack."

        if test_passed:
            # 3. GitHub
            status.text("🛰️ Step 3/4: Initializing GitHub Repository...")
            progress.progress(75)
            try:
                url = git_engine.initialize_and_push_new_repo(project_path, chosen['title'], chosen['description'])
                progress.progress(100)
                status.success("🎉 Project Live on GitHub!")
                st.balloons()
                st.markdown(f"[🔗 Open Repository]({url})")
            except Exception as e:
                st.error(f"GitHub Error: {e}")
        else:
            st.error("🚨 Verification Failed.")
            st.code(test_output)