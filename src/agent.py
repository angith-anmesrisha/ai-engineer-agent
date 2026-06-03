import os
import sys
import subprocess
import json
import time
from google import genai
from dotenv import load_dotenv

# Gracefully fall back if the Groq package isn't installed yet
try:
    from groq import Groq
except ImportError:
    Groq = None

def clean_markdown_json_fences(raw_text: str) -> str:
    """
    Utility: Safely strips out markdown code fences (like ```json ... ```)
    using robust, single-quoted targets to prevent syntax interpretation errors.
    """
    text = raw_text.strip()
    
    # Clean leading fences
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
        
    # Clean trailing fences
    if text.endswith('```'):
        text = text[:-3]
        
    return text.strip()

class AutonomousFixAgent:
    def __init__(self, target_dir: str, gemini_model: str = "gemini-2.5-flash", groq_model: str = "llama-3.3-70b-versatile"):
        load_dotenv()
        self.target_dir = target_dir
        self.client = genai.Client()
        
        # Dynamically set models based on UI selection
        self.gemini_model = gemini_model
        self.groq_model = groq_model
        
        # Initialize an active list to hold operations telemetry metrics
        self.telemetry_history = []
        
        # Initialize Groq fallback engine if active
        groq_api_key = os.getenv("GROQ_API_KEY")
        if Groq and groq_api_key:
            self.groq_client = Groq(api_key=groq_api_key)
        else:
            self.groq_client = None

    def run_global_diagnostics(self):
        """Sensors: Runs pytest across the whole workspace and dynamically parses crashes."""
        print("🔍 [AGENT] Initializing global workspace telemetry scan...")
        # Using sys.executable guarantees we use the active virtual environment's python
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--tb=short"], 
            cwd=self.target_dir, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            return True, None, "All systems green."
            
        trace_log = result.stdout
        print("🚨 [AGENT] Structural anomaly detected in codebase tracking lines.")
        
        broken_file = None
        for line in trace_log.split("\n"):
            if "sandbox/src/" in line and ".py" in line:
                parts = line.split(":")
                for part in parts:
                    if "sandbox/src/" in part and part.endswith(".py"):
                        broken_file = part.strip()
                        break
            if broken_file:
                break
                
        if not broken_file:
            broken_file = "sandbox/src/finance.py"
            
        return False, broken_file, trace_log

    def execute_robust_generation(self, prompt: str, system_instruction: str, stage_name: str = "Generation") -> str:
        """Helper: Tries selected Gemini first; if throttled, automatically shifts to selected Groq."""
        start_time = time.time()
        try:
            print(f"🛰️ [JARVIS Engine] Routing payload stream via Gemini API ({self.gemini_model})...")
            response = self.client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
                config={"system_instruction": system_instruction} if system_instruction else None
            )
            duration = time.time() - start_time
            
            # Extract token telemetry dynamically from metadata
            prompt_tokens, completion_tokens, total_tokens = 0, 0, 0
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                prompt_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0)
                completion_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0)
                total_tokens = getattr(response.usage_metadata, 'total_token_count', 0)
            
            self.telemetry_history.append({
                "stage": stage_name,
                "provider": "Gemini",
                "model": self.gemini_model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "duration_sec": round(duration, 2),
                "status": "Success",
                "timestamp": time.strftime("%H:%M:%S")
            })
            return response.text
        except Exception as e:
            gemini_error = str(e)
            print(f"⚠️ [JARVIS Engine] Gemini exception caught: {gemini_error}")
            if self.groq_client:
                print(f"🎛️ [JARVIS Engine] CRITICAL FALLBACK: Deploying Groq cluster ({self.groq_model})...")
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})
                
                groq_start_time = time.time()
                groq_response = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=messages,
                    temperature=0.2
                )
                duration = time.time() - start_time # Includes the time spent on the failed Gemini call
                
                # Extract token telemetry dynamically from Groq usage logs
                prompt_tokens, completion_tokens, total_tokens = 0, 0, 0
                if hasattr(groq_response, 'usage') and groq_response.usage:
                    prompt_tokens = getattr(groq_response.usage, 'prompt_tokens', 0)
                    completion_tokens = getattr(groq_response.usage, 'completion_tokens', 0)
                    total_tokens = getattr(groq_response.usage, 'total_tokens', 0)
                
                self.telemetry_history.append({
                    "stage": stage_name,
                    "provider": "Groq Fallback",
                    "model": self.groq_model,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "duration_sec": round(duration, 2),
                    "status": "Fallback Active",
                    "error_log": gemini_error,
                    "timestamp": time.strftime("%H:%M:%S")
                })
                return groq_response.choices[0].message.content
            else:
                self.telemetry_history.append({
                    "stage": stage_name,
                    "provider": "Gemini",
                    "model": self.gemini_model,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "duration_sec": round(time.time() - start_time, 2),
                    "status": "Failed",
                    "error_log": gemini_error,
                    "timestamp": time.strftime("%H:%M:%S")
                })
                raise Exception(f"Both Gemini and Groq fallback targets are unavailable. Primary error: {gemini_error}")

    def generate_project_pitches(self, user_concept: str) -> list[dict]:
        """Phase 1: Brainstorms 3 project ideas utilizing modern stacks (Next.js, React, Node, or Python)."""
        sys_instruction = """You are a visionary product manager and software architect. Based on the user's basic concept, generate exactly 3 distinct, creative, and fully fleshed-out project implementation pitches.
        
You MUST choose the absolute best modern framework/stack (Next.js, React, Node.js, HTML/CSS, or Python) based on the user's concept.
Include a mandatory 'README.md' in the proposed files list and define a 'test_command' (e.g. ['npm', 'test'] or ['python', '-m', 'pytest']).

You MUST respond ONLY with a raw JSON array matching this exact schema layout format. Do not include any conversational filler, markdown block wrappers, or explanation words:
[
  {
    "id": 1,
    "title": "Project Title",
    "description": "Short description",
    "tech_stack": "Next.js",
    "core_features": ["Feature 1", "Feature 2"],
    "proposed_files": ["README.md", "src/main.py", "tests/test_main.py"],
    "test_command": ["python", "-m", "pytest"]
  }
]"""
        
        prompt = f"User wants to build something related to: {user_concept}"
        raw_output = self.execute_robust_generation(prompt, sys_instruction, stage_name="Brainstorming Architecture")
        
        clean_text = clean_markdown_json_fences(raw_output)
        return json.loads(clean_text)

    def build_and_deploy_project(self, chosen_pitch: dict, local_project_path: str) -> bool:
        """Phase 2: Compiles all file matrices (including custom README.md instructions) using the selected active model profile."""
        sys_instruction = """You are an elite principal software engineer. Generate the complete source code content for every single file listed in the pitch payload.
        
You MUST write a professional, extensive, and highly-detailed README.md with clear step-by-step setup, dependency installation, and local launch instructions.

Return your response ONLY as a raw, valid JSON object matching this structure. Do not include markdown code block syntax or explanations outside of the JSON:
{
  "files": [
    {
      "file_path": "README.md",
      "content": "# Project Title\\n\\n## Setup Instructions..."
    }
  ]
}"""
        
        prompt = f"APPROVED PROJECT CONFIGURATION:\n{json.dumps(chosen_pitch)}"
        raw_output = self.execute_robust_generation(prompt, sys_instruction, stage_name="Source Code Synthesis")
        
        clean_text = clean_markdown_json_fences(raw_output)
        generated_data = json.loads(clean_text)
        
        for file_entry in generated_data.get("files", []):
            file_path = file_entry["file_path"]
            content = file_entry["content"]
            full_abs_path = os.path.join(local_project_path, file_path)
            os.makedirs(os.path.dirname(full_abs_path), exist_ok=True)
            with open(full_abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"💾 [JARVIS Matrix] Isolated structural file write complete: {file_path}")
            
        return True