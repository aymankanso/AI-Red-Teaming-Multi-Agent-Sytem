# AI Red Teaming Multi-Agent System

An autonomous AI-powered penetration testing framework using **4 specialized agents** coordinated through **LangGraph**. Automates reconnaissance, vulnerability assessment, exploitation planning, and reporting phases of security assessments.

> ⚠️ **LEGAL DISCLAIMER**: For **AUTHORIZED SECURITY TESTING ONLY**. Unauthorized access is **ILLEGAL** under CFAA and international laws.

---

## 🎯 Key Features

- **Multi-Agent Architecture**: 4 specialized agents (Planner, Reconnaissance, Initial Access, Summary)
- **36+ Security Tools**: nmap, masscan, nuclei, hydra, sqlmap, msfconsole, and more
- **Streamlit Web Interface**: Real-time agent communication display
- **Model Selection**: Support for OpenAI and Anthropic models
- **Memory System**: LangMem for semantic search + InMemorySaver for state
- **Docker Integration**: Isolated Kali Linux environment for tool execution

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop
- OpenAI API Key

### Installation

```bash
# Clone repository
git clone <repository-url>
cd agent

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start Docker container
docker-compose up -d
```

### Running the System

**Option 1: Single Command (Windows PowerShell)**
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe src/tools/mcp/Reconnaissance.py"
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe src/tools/mcp/Initial_Access.py"
Start-Sleep -Seconds 3
.\venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py
```

**Option 2: Manual (3 terminals)**

```powershell
# Terminal 1 - Reconnaissance MCP Server
python src/tools/mcp/Reconnaissance.py

# Terminal 2 - Initial Access MCP Server
python src/tools/mcp/Initial_Access.py

# Terminal 3 - Streamlit App
streamlit run frontend/streamlit_app.py
```

**Open Browser**: http://localhost:8501

### First Run
1. Select your model (GPT-4o mini recommended)
2. Read and acknowledge the legal disclaimer
3. Enter your objective (e.g., "Scan 192.168.1.100 for vulnerabilities")
4. Approve any high-risk operations when prompted
5. Review the generated security report

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)                   │
│         • Model Selection  • Real-time Agent Display             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   LangGraph Swarm Coordinator                    │
│      • InMemorySaver  • InMemoryStore  • Active Agent Router    │
└─┬───────────┬─────────────┬─────────────┬───────────────────────┘
  │           │             │             │
  ▼           ▼             ▼             ▼
┌───────┐ ┌────────┐ ┌─────────────┐ ┌─────────┐
│Planner│ │ Recon  │ │ InitAccess  │ │ Summary │
│ Agent │ │ Agent  │ │   Agent     │ │  Agent  │
└───┬───┘ └───┬────┘ └──────┬──────┘ └────┬────┘
    │         │             │             │
    └─────────┴─────────────┴─────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    MCP Tool Servers               │
│      nmap, nuclei, hydra, sqlmap, msfconsole, gobuster...       │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                Docker Container (Kali Linux)                     │
│                  Isolated Execution Environment                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Roles

### Planner Agent 🎯
**Role**: Strategic Coordinator & Task Orchestrator
- Parses user objectives into actionable subtasks
- Routes tasks to appropriate specialist agents
- Monitors progress and adjusts strategy

### Reconnaissance Agent 🔍
**Role**: Information Gathering & Intelligence Collection
- Network discovery and enumeration
- Service identification and versioning
- Vulnerability scanning and assessment

### Initial Access Agent 🎯
**Role**: Exploitation Planning & Credential Attacks
- Analyzes vulnerabilities for exploitability
- Plans exploitation strategies
- Executes attacks

### Summary Agent 📝
**Role**: Report Generation & Findings Aggregation
- Synthesizes findings from all agents
- Generates comprehensive security reports
- Provides remediation recommendations

---

## 🛠️ Tools

### Network Scanners
`nmap`, `masscan`, `unicornscan`, `hping3`, `arping`, `fping`, ...

### Vulnerability Scanners
`nuclei`, `nikto`

### Exploitation Tools
`msfconsole`, `msfvenom`, `searchsploit`

### Enumeration Tools
`gobuster`, `dirb`, `wfuzz`, `ffuf`

---

## ⚙️ Configuration

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0
```

### Project Structure
```
src/
├── agents/swarm/          # Agent implementations
│   ├── Planner.py
│   ├── Recon.py
│   ├── InitAccess.py
│   └── Summary.py
├── graphs/                # LangGraph orchestration
├── tools/                 # MCP tool integration
└── prompts/               # Agent prompts
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | Verify `OPENAI_API_KEY` in `.env` file |
| Docker not running | Run `docker-compose up -d` |
| Import errors | Run `pip install -r requirements.txt` |
| MCP connection failed | Ensure MCP servers are running first |
| Tool timeout | Check Docker container status |

---

## 🔒 Safety & Ethics

**AUTHORIZED TESTING ONLY** - You must have written authorization before testing any system.

- ✅ Test only in controlled lab environments or systems you own
- ✅ Obtain formal penetration testing engagement authorization
---

## Project

**Objective**: Demonstrate automation of penetration testing tasks

**System Features**:
- Multi-agent architecture with clear roles
- Real-time cost tracking per agent
- Safety measures (human-in-loop, disclaimers)
- Comprehensive documentation

