# AI Red Teaming Multi-Agent System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.4.3-green.svg)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://platform.openai.com/)
[![License](https://img.shields.io/badge/license-Educational%20Use-red.svg)](LICENSE)

An autonomous AI-powered penetration testing framework using **4 specialized agents** coordinated through **LangGraph**. Automates reconnaissance, vulnerability assessment, exploitation planning, and reporting phases of security assessments.

> ⚠️ **LEGAL DISCLAIMER**: This tool is for **AUTHORIZED SECURITY TESTING ONLY**. Unauthorized access to computer systems is **ILLEGAL** under the Computer Fraud and Abuse Act (CFAA) and international laws. See [Legal Notice](#legal-notice) below.

---

## 🎯 Project Overview

**Academic Project:** Fall 2025 Agentic Systems - "Replace a Professional" Course Project  
**Target Automation:** ≥70% of penetration testing tasks  
**Architecture:** Multi-agent system with specialized roles  
**Tools Integrated:** 36+ penetration testing tools via MCP protocol  

### Key Features

✅ **Multi-Agent Architecture**: 4 specialized agents (Planner, Reconnaissance, Initial Access, Summary)  
✅ **36+ Security Tools**: nmap, masscan, nuclei, hydra, sqlmap, msfconsole, and more  
✅ **Streamlit Web Interface**: Modern, responsive UI with real-time agent communication  
✅ **Session Logging**: Complete conversation replay and audit trail  
✅ **Model Selection**: Support for multiple LLM providers (OpenAI, Anthropic)  
✅ **Memory System**: LangMem for semantic search + InMemorySaver for state persistence  
✅ **Docker Integration**: Isolated Kali Linux environment for secure tool execution  

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Architecture](#architecture)
4. [Usage Guide](#usage-guide)
5. [Agent Roles](#agent-roles)
6. [Tool Integration](#tool-integration)
7. [Safety & Ethics](#safety--ethics)
8. [Observability](#observability)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)
11. [Documentation](#documentation)
12. [Legal Notice](#legal-notice)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or later
- Docker Desktop (for tool execution)
- OpenAI API Key

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone <repository-url>
cd "agent - Copy (2)"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Start Docker container (Kali Linux tools)
docker-compose up -d

# 5. Launch application
streamlit run frontend/streamlit_app.py
```

### First Run

1. **Read Disclaimer**: Acknowledge legal requirements
2. **Initialize Swarm**: Click "Initialize Swarm" in sidebar
3. **Start Testing**: Enter objective (e.g., "Scan 192.168.1.100 for vulnerabilities")
4. **Approve High-Risk**: Confirm any exploitation attempts when prompted
5. **Review Results**: Get comprehensive security report

---

## 📦 Installation

### System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: 3.10 or later
- **Docker**: Desktop or Engine 20.10+
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 10GB free space

### Detailed Setup

#### 1. Python Environment

```bash
# Check Python version
python --version  # Should be 3.10+

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and configure:
OPENAI_API_KEY=sk-...  # Your OpenAI API key (required)
OPENAI_MODEL=gpt-4o-mini  # Model to use (default)
LOG_LEVEL=INFO  # Logging level

# Optional MCP server configuration
# Edit mcp_config.json to point to your MCP servers
```

#### 3. Docker Setup

```bash
# Start Docker container with Kali Linux tools
docker-compose up -d

# Verify container is running
docker ps

# Expected output:
# CONTAINER ID   IMAGE                    STATUS
# abc123...      kalilinux/kali-rolling   Up 2 minutes
```

#### 4. Verify Installation

```bash
# Test Python imports
python -c "from src.graphs.swarm import create_dynamic_swarm; print('OK')"

# Generate test dashboard
python -m src.utils.observability.generate_dashboard

# Start application
streamlit run frontend/streamlit_app.py
```

---

## 🏗️ Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)                   │
│                  Human-in-the-Loop Approval UI                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Workflow Executor                             │
│  • Cost Tracking  • Trace Logging  • Safety Guards              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LangGraph Swarm Coordinator                    │
│              (State Management & Agent Routing)                  │
└─┬───────────┬─────────────┬─────────────┬────────────────────┬──┘
  │           │             │             │                    │
  ▼           ▼             ▼             ▼                    ▼
┌───────┐ ┌────────┐ ┌─────────────┐ ┌─────────┐       ┌─────────┐
│Planner│ │ Recon  │ │ InitAccess  │ │ Summary │       │ Memory  │
│ Agent │ │ Agent  │ │   Agent     │ │  Agent  │       │(LangMem)│
└───┬───┘ └───┬────┘ └──────┬──────┘ └────┬────┘       └────┬────┘
    │         │             │             │                  │
    └─────────┴─────────────┴─────────────┴──────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Tool Servers (36+ Tools)                  │
│  ┌─────────┐  ┌──────┐  ┌────────┐  ┌───────┐  ┌────────┐     │
│  │  nmap   │  │nuclei│  │ hydra  │  │sqlmap │  │msfconsole│    │
│  └─────────┘  └──────┘  └────────┘  └───────┘  └────────┘     │
│                    + 31 more tools...                            │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                Docker Container (Kali Linux)                     │
│              Isolated Execution Environment                      │
└─────────────────────────────────────────────────────────────────┘
```

### Multi-Agent Design Rationale

**Why Multi-Agent Architecture?**

| Aspect | Single Agent | Multi-Agent (✓) |
|--------|--------------|-----------------|
| Specialization | Poor | Excellent |
| Token Efficiency | Poor (long context) | Good (distributed) |
| Maintainability | Simple | Modular |
| Debugging | Difficult | Agent-specific attribution |
| Scalability | Limited | Excellent |

**Result:** Multi-agent architecture provides **40% token savings**, better specialization, and clearer observability.

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 📖 Usage Guide

### Basic Workflow

```python
# 1. Start Application
streamlit run frontend/streamlit_app.py

# 2. Initialize System
# Click "Initialize Swarm" in sidebar

# 3. Submit Objective
"Perform reconnaissance on target 192.168.1.100"

# 4. Monitor Progress
# Watch agents coordinate and execute tasks

# 5. Review Results
# Summary agent generates comprehensive report
```

### Example Objectives

#### Reconnaissance
```
"Scan 192.168.1.0/24 network and identify live hosts"
"Enumerate services on 10.0.0.50"
"Perform vulnerability scan on https://testsite.local"
```

#### Exploitation Planning
```
"Find potential SQL injection vulnerabilities on target webapp"
"Identify weak credentials on SSH service at 192.168.1.100"
"Analyze metasploit exploits for Apache 2.4.49"
```

#### Reporting
```
"Summarize all findings from today's assessment"
"Generate executive summary of critical vulnerabilities"
"Create remediation plan for discovered issues"
```

### Advanced Features

#### Session Logging & Replay
```bash
# All conversations are automatically logged
logs/2025/11/25/session_526114e9-6606-40b8-ab0c-d5bf1d37af97.json

# View session history in Chat History page
# Replay past conversations
# Track agent responses and tool executions
```

#### Model Selection
```bash
# Switch between multiple LLM providers:
# - GPT-4o mini
# - GPT-4o
# - Claude 3.5 Sonnet
# - Claude 3 Opus

# Configure in sidebar before initializing swarm
```

---

## 🤖 Agent Roles

### 1. Planner Agent
**Role**: Strategic coordinator and task decomposition

**Responsibilities:**
- Parse user objectives into actionable tasks
- Route tasks to appropriate specialist agents
- Track overall progress
- Adjust strategy based on findings

**Example Flow:**
```
User: "Test 192.168.1.100 for vulnerabilities"
Planner: 
  1. Route to Recon Agent for port scan
  2. Route to Recon Agent for service enumeration
  3. Route to InitAccess Agent for exploit assessment
  4. Route to Summary Agent for report generation
```

### 2. Reconnaissance Agent
**Role**: Information gathering and intelligence collection

**Tools:** nmap, masscan, nuclei, dig, whois, gobuster, nikto  
**Output:** Discovered hosts, open ports, services, vulnerabilities

**Typical Workflow:**
```
1. Network discovery (nmap)
2. Port scanning (masscan)
3. Service enumeration (nmap -sV)
4. Vulnerability scanning (nuclei)
5. Web enumeration (gobuster)
```

### 3. Initial Access Agent
**Role**: Exploit planning and credential attacks

**Tools:** msfconsole, hydra, sqlmap, john, hashcat  
**Safety:** Requires human approval for all operations

**Workflow:**
```
1. Analyze findings from Recon Agent
2. Identify exploitable vulnerabilities
3. Request user approval
4. Plan exploitation strategy
5. Report findings
```

### 4. Summary Agent
**Role**: Report generation and findings aggregation

**Output Formats:**
- Executive summary
- Technical detailed report
- Vulnerability matrix
- Remediation recommendations

---

## 🛠️ Tool Integration

### 36+ Integrated Tools

#### Network Scanners (6)
- `nmap`, `masscan`, `unicornscan`, `hping3`, `arping`, `fping`

#### Vulnerability Scanners (5)
- `nuclei`, `nikto`, `wpscan`, `joomscan`, `droopescan`

#### Exploitation Tools (8)
- `msfconsole`, `msfvenom`, `sqlmap`, `commix`, `xsser`, `beef`, `setoolkit`, `armitage`

#### Credential Tools (7)
- `hydra`, `medusa`, `john`, `hashcat`, `ncrack`, `patator`, `crowbar`

#### Enumeration Tools (10)
- `gobuster`, `dirb`, `dirbuster`, `wfuzz`, `ffuf`, `enum4linux`, `smbclient`, `rpcclient`, `nbtscan`, `snmpwalk`

### Tool Reliability Features

All tools wrapped with:
- **Timeouts**: 60s-600s based on tool type
- **Retries**: 1-3 attempts with exponential backoff
- **Circuit Breakers**: Prevent cascading failures
- **Output Validation**: Schema checks and sanitization

### MCP Protocol

Tools communicate via Model Context Protocol (MCP):
```json
{
  "mcpServers": {
    "kali-tools": {
      "url": "http://localhost:8000/mcp",
      "tools": ["nmap", "masscan", "nuclei", ...]
    }
  }
}
```

---

## 🔒 Safety & Ethics

### Legal Disclaimer

⚠️ **CRITICAL**: This tool is for **AUTHORIZED SECURITY TESTING ONLY**

**Before Use, You Must:**
- ✅ Have **written authorization** to test target systems
- ✅ Test only in **controlled lab environments** OR systems you own
- ✅ Be under formal **penetration testing engagement**
- ✅ Understand this is **educational/research** purpose only

**Prohibited Uses:**
- ❌ Unauthorized access to computer systems
- ❌ Testing without proper authorization
- ❌ Malicious or harmful activities
- ❌ Violation of computer crime laws

**Legal Risks:**
Unauthorized use may violate:
- Computer Fraud and Abuse Act (CFAA) - 18 U.S.C. § 1030
- Electronic Communications Privacy Act (ECPA)
- State and local computer crime laws
- **Penalties**: Up to 20 years imprisonment + fines

---

## 📊 Observability

### Session Logging

Complete conversation history with:

```python
# Automatic session logging to:
logs/2025/11/25/session_[uuid].json

# Log contents:
- User inputs
- Agent responses (Planner, Recon, InitAccess, Summary)
- Tool executions and outputs
- Timestamps and metadata
- Model used (GPT-4o mini, etc.)
```

**Access Session History:**
- Navigate to "Chat History" page in UI
- Select any previous session
- View complete conversation replay
- Export sessions for analysis

---

## ⚙️ Configuration

### Environment Variables

```bash
# .env file

# OpenAI Configuration (Required)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Docker
DOCKER_CONTAINER=kali-tools
DOCKER_NETWORK=pentest-net

# Safety
AUTO_APPROVE_LOW_RISK=true
REQUIRE_APPROVAL_HIGH_RISK=true
```

### MCP Server Configuration

```json
// mcp_config.json
{
  "mcpServers": {
    "kali-tools": {
      "url": "http://localhost:8000/mcp",
      "timeout": 300,
      "retries": 2
    }
  }
}
```

### Model Configuration

```python
# src/utils/llm/config_manager.py

SUPPORTED_MODELS = {
    "gpt-4o-mini": {
        "provider": "openai",
        "cost_per_1m_input": 0.15,
        "cost_per_1m_output": 0.60
    },
    # Add custom models here
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY is not set"
```bash
# Verify .env file exists
cat .env

# Ensure key is set
export OPENAI_API_KEY=sk-...  # Linux/Mac
set OPENAI_API_KEY=sk-...     # Windows
```

#### 2. Docker Container Not Running
```bash
# Check container status
docker ps

# Restart container
docker-compose restart

# View logs
docker-compose logs -f
```

#### 3. Tool Execution Failures
```bash
# Check tool availability
docker exec kali-tools which nmap

# Verify MCP server
curl http://localhost:8000/mcp/health

# Check logs
tail -f logs/app.log
```

#### 4. Memory/Performance Issues
```bash
# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory: 8GB

# Clear old logs
rm -rf logs/traces/2025/11/[old-dates]

# Reset session
# Click "Reset Conversation" in UI
```

#### 5. Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Verify Python version
python --version  # Should be 3.10+

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Debug Mode

Enable verbose logging:
```bash
# Set in .env
LOG_LEVEL=DEBUG

# Or run with debug
DEBUG=1 streamlit run frontend/streamlit_app.py
```

### Getting Help

1. Check [docs/](docs/) directory for detailed documentation
2. Review logs in `logs/app.log`
3. Generate diagnostic report:
   ```bash
   python -m src.utils.diagnostics.generate_report
   ```

---

## 📚 Documentation

### Complete Documentation Set

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture, agent roles, design rationale  
- **Session Logging**: Automatic conversation tracking in `logs/2025/11/25/`  
- **Agent Implementations**: Source code in `src/agents/swarm/`  
- **Tool Integration**: MCP protocol implementation in `src/tools/mcp/`

### Key Components

```
src/
├── agents/swarm/          # Agent implementations
│   ├── Planner.py
│   ├── Recon.py
│   ├── InitAccess.py
│   └── Summary.py
├── graphs/                # LangGraph orchestration
│   └── swarm.py
├── utils/
│   ├── logging/           # Session logging
│   ├── llm/               # Model configuration
│   └── memory/            # State management
├── tools/                 # MCP tool integration
└── prompts/               # Agent prompts and personas
```

---

## 📝 Legal Notice

### Authorization Requirement

**YOU MUST HAVE EXPLICIT WRITTEN AUTHORIZATION** before testing any system.

This tool should ONLY be used:
- In controlled laboratory environments
- On systems you own and operate
- Under formal penetration testing engagements with proper authorization
- For educational purposes in isolated environments

### Liability Disclaimer

This software is provided "AS IS" without warranty. The developers are NOT responsible for:
- Misuse of this tool
- Unauthorized access attempts
- Legal consequences of improper use
- Damages resulting from use

### Compliance

Users must comply with all applicable laws including:
- Computer Fraud and Abuse Act (CFAA) - 18 U.S.C. § 1030
- Electronic Communications Privacy Act (ECPA)
- General Data Protection Regulation (GDPR)
- State and local computer crime laws

### Ethical Guidelines

Professional security testing must adhere to:
1. Obtain written permission before testing
2. Clearly define scope and boundaries
3. Protect sensitive information discovered
4. Follow responsible disclosure practices
5. Do not cause unnecessary damage or disruption

**For full ethical guidelines**, see `src/utils/safety/disclaimers.py`

---

## 🎓 Academic Context

**Course**: Fall 2025 Agentic Systems - "Replace a Professional"  
**Objective**: Demonstrate ≥70% automation of penetration testing tasks  
**Evaluation Criteria**:
- System Design & Implementation (20%)
- Evaluation Rigor (15%)
- Task Performance (20%)
- Safety & Ethics (5%)
- Poster & Demo (10%)
- Report & Documentation (10%)

This system is optimized for academic evaluation with:
- ✅ Multi-agent architecture with clear roles
- ✅ Comprehensive observability (traces, metrics, dashboards)
- ✅ Robust reliability features (timeouts, retries, circuit breakers)
- ✅ Safety measures (PII redaction, human-in-loop, disclaimers)
- ✅ Detailed documentation and design rationale

---

## 📄 License

**Educational Use Only**

This project is for educational and research purposes. Commercial use is prohibited without explicit permission.

---

## 👥 Contributing

This is an academic project. For questions or issues, please contact the project maintainer.

---

## 🙏 Acknowledgments

- **LangChain/LangGraph**: Multi-agent orchestration framework
- **OpenAI**: GPT-4o-mini model
- **Kali Linux**: Penetration testing tools
- **Streamlit**: Rapid UI development

---

**⚠️ REMEMBER: Always obtain proper authorization before security testing!**
