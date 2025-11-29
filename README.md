# AI Red Teaming Multi-Agent System

An autonomous AI-powered penetration testing framework using **4 specialized agents** coordinated through **LangGraph**. Automates reconnaissance, vulnerability assessment, exploitation planning, and reporting phases of security assessments.

---

## 🎯 Key Features

- **Multi-Agent Architecture**: 4 specialized agents (Planner, Reconnaissance, Initial Access, Summary)
- **Security Tools**: nmap, masscan, nuclei, hydra, sqlmap, msfconsole, and more
- **Streamlit Web Interface**: Real-time agent communication display
- **Model Selection**: Support for OpenAI and Anthropic models
- **Memory System**: LangMem for semantic search + InMemorySaver for state
- **Docker Integration**: Isolated Kali Linux environment for tool execution

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker Desktop
- OpenAI API Key or Anthropic API Key

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
copy .env.example .env
# Edit .env and add your API keys (OPENAI_API_KEY and/or ANTHROPIC_API_KEY)

# Start Docker container
docker-compose up -d
```

### Running the System

**Option 1: Using PowerShell Script (Recommended)**
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate

# Run the startup script
.\run_app.ps1
```

**Option 2: Single Command (Windows PowerShell)**
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe src/tools/mcp/Reconnaissance.py" ; Start-Sleep -Seconds 2 ; Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe src/tools/mcp/Initial_Access.py" ; Start-Sleep -Seconds 3 ; .\venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py
```

**Option 3: Manual (3 terminals)**

```powershell
# Terminal 1 - Reconnaissance MCP Server
python src/tools/mcp/Reconnaissance.py

# Terminal 2 - Initial Access MCP Server
python src/tools/mcp/Initial_Access.py

# Terminal 3 - Streamlit App
streamlit run frontend/streamlit_app.py
```

**Open Browser**: http://localhost:8501

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
# .env file (copy from .env.example)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LANGGRAPH_TRACING_V2=false
LOG_LEVEL=INFO
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

## 📋 Project Overview

**Objective**: Demonstrate automation of penetration testing tasks through coordinated AI agents

**System Features**:
- Multi-agent architecture with clear roles and responsibilities
- Real-time cost tracking per agent and operation
- Built-in safety measures and user approval prompts
- Comprehensive documentation and reporting
- Docker-based isolation for security tools
- MCP (Model Context Protocol) integration for tool communication
- LangGraph orchestration for complex workflows

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

---

## ⚠️ Disclaimer

This tool is for **authorized security testing only**. Users are responsible for ensuring they have proper authorization before scanning or testing any systems. Unauthorized use may violate laws and regulations.

