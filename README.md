# AI Engineer Agent 🤖🛠️

An autonomous, multi-agent framework designed to assist, streamline, and automate software engineering workflows. By leveraging advanced Large Language Models (LLMs), structural planning, and external tool integration, this agent can autonomously analyze codebases, generate robust unit tests, review pull requests, and orchestrate complex development tasks.

---

## 🌟 Key Features

* **Autonomous Code Analysis:** Deeply parses existing code structures, directory paths, and dependencies to provide context-aware insights.
* **Self-Reflecting Code Generation:** Implements execution loops to generate, test, and refine code (e.g., auto-generating unit tests) dynamically until it passes verification.
* **Multi-Agent Orchestration:** Utilizes a specialized team-based architecture where individual agents (Planner, Coder, Critic) collaborate to execute engineering tasks.
* **Tool & API Integration:** Seamlessly integrates with external development ecosystems like GitHub APIs, file-system drivers, and terminal execution environments.

---

## 🏗️ Architecture Overview

The system uses a highly coordinated multi-agent workflow to ensure safety, code accuracy, and robust problem-solving:

    [ User Prompt / Issue ]
               │
               ▼
     ┌──────────────────┐
     │  Planner Agent   │ ──► Decomposes task into structured steps
     └──────────────────┘
               │
               ▼
     ┌──────────────────┐
     │   Coder Agent    │ ──► Writes/modifies code & implements solutions
     └──────────────────┘
               │
               ▼
     ┌──────────────────┐
     │   Critic Agent   │ ──► Runs tests, checks linters, & validates logic
     └──────────────────┘
               │
        〔 Passes Validation? 〕
           ├─── No ──► (Feedback loop back to Coder Agent)
           └─── Yes ─► [ Final Output / Pull Request ]

---

## 🚀 Getting Started

### Prerequisites

* **Python:** 3.10 or higher
* **API Keys:** Access to a frontier LLM provider (e.g., OpenAI, Anthropic, or Google Gemini)
* **Git** (for codebase cloning and version control actions)

### Installation & Setup

1. **Clone the Repository:**
    git clone https://github.com/angith-anmesrisha/ai-engineer-agent.git
    cd ai-engineer-agent

2. **Set Up a Virtual Environment:**
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install Dependencies:**
    pip install -r requirements.txt

4. **Configure Environment Variables:**
    Create a .env file in the root directory of the project and supply your configurations:

    # LLM Configuration
    OPENAI_API_KEY=your_openai_api_key_here
    # Or if using Gemini/Anthropic:
    GEMINI_API_KEY=your_gemini_api_key_here
   
    # GitHub Integration (Optional)
    GITHUB_TOKEN=your_github_personal_access_token
   
    # Framework Flags
    ENVIRONMENT=development
    LOG_LEVEL=INFO

---

## 💻 Usage

Run the primary agent dashboard or CLI execution script to begin providing engineering tasks:

    python main.py --task "Write a comprehensive pytest suite for the utilities module"

### Example Tasks to Try:
* "Analyze the repository structure and find bottlenecks in data processing."
* "Refactor the database connection pooling logic to prevent dangling sessions."
* "Generate missing docstrings and markdown formatting for all files inside the source folder."

---

## 🛠️ Project Structure

    ai-engineer-agent/
    │
    ├── config/                  # Configuration files and prompt templates
    ├── src/
    │   ├── agents/              # Individual Agent logic (Planner, Worker, Critic)
    │   ├── tools/               # File system tools, executing runtimes, API wrappers
    │   └── utils/               # Common helper utilities and logging modules
    │
    ├── tests/                   # Framework unit tests
    ├── .env.example             # Template for local environment properties
    ├── main.py                  # CLI application entry point
    ├── requirements.txt         # Project package dependencies
    └── README.md                # System documentation

---

## 🤝 Contributing

Contributions are highly encouraged! Please follow these guidelines:

1. Fork the project repository.
2. Create your feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a Pull Request detailing your enhancements.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for more details.
