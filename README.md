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
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
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

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 6. Start Docker container (Kali Linux tools)
docker-compose up -d
```

### Running the System (Windows PowerShell)

**Option 1: Single Command (Recommended)**
```powershell
cd "C:\Users\user\Desktop\test\agent - Copy (2)"

# Start MCP servers and Streamlit in one command
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\user\Desktop\test\agent - Copy (2)'; .\venv\Scripts\python.exe src/tools/mcp/Reconnaissance.py"
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\user\Desktop\test\agent - Copy (2)'; .\venv\Scripts\python.exe src/tools/mcp/Initial_Access.py"
Start-Sleep -Seconds 3
.\venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py
```

**Option 2: Use Launch Script**
```powershell
cd "C:\Users\user\Desktop\test\agent - Copy (2)"
.\run_app.ps1
```

**Option 3: Manual Start (3 separate terminals)**

Terminal 1 - Reconnaissance MCP Server:
```powershell
cd "C:\Users\user\Desktop\test\agent - Copy (2)"
.\venv\Scripts\activate
python src/tools/mcp/Reconnaissance.py
```

Terminal 2 - Initial Access MCP Server:
```powershell
cd "C:\Users\user\Desktop\test\agent - Copy (2)"
.\venv\Scripts\activate
python src/tools/mcp/Initial_Access.py
```

Terminal 3 - Streamlit App:
```powershell
cd "C:\Users\user\Desktop\test\agent - Copy (2)"
.\venv\Scripts\activate
streamlit run frontend/streamlit_app.py
```

### First Run

1. **Open Browser**: Navigate to http://localhost:8501
2. **Select Model**: Choose GPT-4o mini or other available model
3. **Read Disclaimer**: Acknowledge legal requirements
4. **Start Testing**: Enter objective (e.g., "Scan 192.168.1.100 for vulnerabilities")
5. **Approve High-Risk**: Confirm any exploitation attempts when prompted
6. **Review Results**: Get comprehensive security report

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

### System Overview

This system implements a **multi-agent swarm architecture** using LangGraph's prebuilt ReAct agents coordinated through a custom swarm orchestration layer. Each agent is a specialized autonomous unit with its own tools, memory, and decision-making capabilities, coordinated through a centralized state management system.

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)                   │
│         • Model Selection  • Session Management                  │
│         • Real-time Agent Communication Display                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Workflow Executor                             │
│  • Async Stream Processing  • Message Deduplication             │
│  • Event Formatting                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LangGraph Swarm Coordinator                    │
│  • InMemorySaver (State Persistence)                            │
│  • InMemoryStore (Vector Memory with OpenAI Embeddings)         │
│  • Active Agent Router (Dynamic Agent Selection)                │
│  • Message State Management (MessagesState)                     │
└─┬───────────┬─────────────┬─────────────┬────────────────────┬──┘
  │           │             │             │                    │
  ▼           ▼             ▼             ▼                    ▼
┌───────┐ ┌────────┐ ┌─────────────┐ ┌─────────┐       ┌─────────┐
│Planner│ │ Recon  │ │InitAccess   │ │ Summary │       │ Memory  │
│ Agent │ │ Agent  │ │   Agent     │ │  Agent  │       │(LangMem)│
│       │ │        │ │             │ │         │       │         │
│ReAct  │ │ ReAct  │ │   ReAct     │ │  ReAct  │       │ Vector  │
│Loop   │ │ Loop   │ │   Loop      │ │  Loop   │       │ Search  │
└───┬───┘ └───┬────┘ └──────┬──────┘ └────┬────┘       └────┬────┘
    │         │             │             │                  │
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

---

## 🧠 System Architecture Deep Dive

### 1. Agent Architecture

#### **ReAct Agent Pattern**

Each agent follows the **ReAct (Reasoning + Acting)** pattern:

```
1. REASON: Analyze current situation and decide next action
2. ACT: Execute tool or handoff to another agent
3. OBSERVE: Process tool results
4. REPEAT: Continue loop until task complete
```

**Implementation:**
```python
# Each agent is created using LangGraph's create_react_agent
agent = create_react_agent(
    llm=llm,                    # LLM instance (GPT-4o mini, Claude 3.5 Sonnet, etc.)
    tools=tools,                # Agent-specific tools + handoff tools + memory tools
    store=store,                # Shared InMemoryStore for semantic memory
    name="AgentName",           # Unique agent identifier
    prompt=system_prompt        # Agent persona and instructions
)
```

#### **Agent Specialization**

| Agent | Role | Tools | Handoff Capabilities |
|-------|------|-------|---------------------|
| **Planner** | Strategic coordination | MCP tools (minimal) + All handoffs | → Recon, InitAccess, Summary |
| **Reconnaissance** | Information gathering | nmap, masscan, nuclei, gobuster, etc. | → Planner, InitAccess, Summary |
| **Initial_Access** | Exploitation planning | msfconsole, hydra, sqlmap, etc. | → Planner, Recon, Summary |
| **Summary** | Report generation | Document formatting tools | → Planner |

---

### 2. Communication & Coordination

#### **Swarm Coordination Layer**

The system uses a custom swarm implementation that extends LangGraph's StateGraph:

```python
# Swarm creation workflow
workflow = create_swarm(
    agents=[planner, recon, initaccess, summary],
    default_active_agent="Planner",  # Entry point
)

compiled_workflow = workflow.compile(
    checkpointer=InMemorySaver(),     # State persistence
    store=InMemoryStore(),            # Memory storage
)
```

#### **Agent Communication Mechanisms**

**1. Handoff Tools (Primary Communication)**

Agents communicate by transferring control using handoff tools:

```python
# Example: Planner hands off to Reconnaissance
handoff_to_reconnaissance = create_handoff_tool(
    agent_name="Reconnaissance",
    name="transfer_to_reconnaissance",
    description="Transfer to Reconnaissance"
)

# Agent calls tool to transfer:
# "I need to gather network information. Transferring to Reconnaissance..."
```

**How Handoffs Work:**
- Agent decides to hand off (ReAct reasoning)
- Calls handoff tool with context
- LangGraph's router activates target agent
- Target agent sees full conversation history in MessagesState
- Target agent continues from where previous agent left off

**2. Shared Message State**

All agents share a common `MessagesState` that contains:
```python
class SwarmState(MessagesState):
    active_agent: Optional[str]  # Currently active agent name
    # MessagesState includes:
    # - messages: List[BaseMessage]  # Full conversation history
```

**Message Flow:**
```
User Input (HumanMessage)
    ↓
Planner processes → Generates AIMessage
    ↓
Planner calls handoff tool → ToolMessage
    ↓
Reconnaissance receives full message history
    ↓
Reconnaissance executes nmap → ToolMessage
    ↓
Reconnaissance analyzes results → AIMessage
    ↓
Reconnaissance hands back to Planner → ToolMessage
    ↓
Planner continues coordination...
```

**3. Active Agent Router**

The swarm includes an intelligent router that:
- Tracks which agent is currently active (`active_agent` field)
- Routes messages to appropriate agent
- Handles START edge (initial entry to Planner)
- Manages agent transitions via handoff tools

```python
def route_to_active_agent(state: dict):
    return state.get("active_agent", "Planner")  # Default to Planner

# Router added to graph:
builder.add_conditional_edges(START, route_to_active_agent, path_map=agent_names)
```

---

### 3. Memory Architecture

The system implements **two-tier memory**:

#### **Tier 1: Conversation State (Short-term)**

**Component:** `InMemorySaver` (LangGraph Checkpointer)

**Purpose:** Persist conversation state across turns

**What's Stored:**
- Full message history (HumanMessage, AIMessage, ToolMessage)
- Current active agent
- Graph execution state

**Lifecycle:**
- Created per thread_id
- Persists for entire session
- Cleared on session reset

**Implementation:**
```python
# Global checkpointer instance
_checkpointer = InMemorySaver()

# Used in workflow compilation
compiled_workflow = workflow.compile(checkpointer=_checkpointer)

# Access via thread config
config = {"configurable": {"thread_id": "user_123_conv_456"}}
workflow.invoke(inputs, config)  # Automatically loads/saves state
```

#### **Tier 2: Semantic Memory (Long-term)**

**Component:** `InMemoryStore` with OpenAI embeddings (LangMem)

**Purpose:** Store and retrieve relevant information semantically

**What's Stored:**
- Key facts from conversations
- Attack strategies
- Vulnerability findings
- Remediation notes

**Memory Tools:**

**1. Manage Memory Tool (Write)**
```python
create_manage_memory_tool(namespace=("memories",))

# Agent usage:
# "I'll remember that target has Apache 2.4.49 vulnerable to CVE-2021-41773"
# → Stores: "Target: example.com, Service: Apache 2.4.49, Vuln: CVE-2021-41773"
```

**2. Search Memory Tool (Read)**
```python
create_search_memory_tool(namespace=("memories",))

# Agent usage:
# "Search memories for Apache vulnerabilities we've seen"
# → Retrieves: Relevant past findings via vector similarity search
```

**Memory Architecture Diagram:**
```
┌─────────────────────────────────────────────┐
│         InMemorySaver (Checkpointer)        │
│  Thread ID: user_123_conv_456               │
│  ┌───────────────────────────────────────┐  │
│  │ Messages: [                           │  │
│  │   HumanMessage("scan target"),        │  │
│  │   AIMessage("executing nmap..."),     │  │
│  │   ToolMessage(nmap_output),           │  │
│  │   ...                                 │  │
│  │ ]                                     │  │
│  │ Active Agent: "Reconnaissance"        │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                    +
┌─────────────────────────────────────────────┐
│     InMemoryStore (Vector Memory)           │
│  Namespace: ("memories", "user_123")        │
│  ┌───────────────────────────────────────┐  │
│  │ Memory Items:                         │  │
│  │  [                                    │  │
│  │    {                                  │  │
│  │      "content": "Target has Apache...",│ │
│  │      "embedding": [0.234, -0.123,...],│  │
│  │      "metadata": {...}                │  │
│  │    },                                 │  │
│  │    ...                                │  │
│  │  ]                                    │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

**Memory Benefits:**
- **Context Retention:** Agents remember findings across sessions
- **Semantic Search:** Find relevant information by meaning, not keywords
- **Cross-Agent Sharing:** All agents access same memory store
- **Intelligent Retrieval:** Only relevant memories loaded (not full history)

---

### 4. Tool Integration Architecture

#### **MCP (Model Context Protocol) Integration**

All security tools are exposed via MCP protocol:

**MCP Server Architecture:**
```
┌─────────────────────────────────────────────┐
│          MCP Tool Loader                    │
│  (src/utils/mcp/mcp_loader.py)             │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│       MCP Client (per agent)                │
│  MultiServerMCPClient                       │
└─┬───────────────────────────────────────────┘
  │
  ├──► MCP Server 1 (Port 3001)
  │    Tools: nmap, masscan, nuclei, etc.
  │
  ├──► MCP Server 2 (Port 3002)
  │    Tools: msfconsole, hydra, sqlmap, etc.
  │
  └──► MCP Server N (Port 300N)
       Tools: Custom tools...
```

**Tool Loading Process:**

```python
# 1. Load MCP configuration
mcp_config = {
    "mcpServers": {
        "reconnaissance": {
            "url": "http://localhost:3001",
            "tools": ["nmap", "masscan", "nuclei", ...]
        },
        "initial_access": {
            "url": "http://localhost:3002",
            "tools": ["msfconsole", "hydra", "sqlmap", ...]
        }
    }
}

# 2. Agent-specific tool loading
async def load_mcp_tools(agent_name: List[str]) -> List[Tool]:
    """Load only tools relevant to specific agent"""
    # Filter tools by agent category
    # Connect to appropriate MCP servers
    # Return list of callable tools
    pass

# 3. Tool assignment to agent
mcp_tools = await load_mcp_tools(agent_name=["reconnaissance"])
agent = create_react_agent(llm, tools=mcp_tools + handoff_tools + memory_tools)
```

**Tool Execution Flow:**
```
1. Agent decides to use tool (ReAct reasoning)
2. Calls tool with parameters: nmap(target="192.168.1.1", options="-sV")
3. MCP client sends request to MCP server
4. MCP server forwards to Docker container
5. Docker executes: docker exec kali-tools nmap -sV 192.168.1.1
6. Output captured and returned as ToolMessage
7. Agent processes output in next ReAct cycle
```

#### **Tool Categories & Agent Assignment**

**Reconnaissance Agent Tools:**
- Network scanners: `nmap`, `masscan`, `unicornscan`
- Vulnerability scanners: `nuclei`, `nikto`, `wpscan`
- Web enumeration: `gobuster`, `dirb`, `wfuzz`
- Service enumeration: `enum4linux`, `smbclient`, `snmpwalk`

**Initial_Access Agent Tools:**
- Exploitation frameworks: `msfconsole`, `msfvenom`
- Credential attacks: `hydra`, `medusa`, `ncrack`
- Web exploits: `sqlmap`, `commix`, `xsser`
- Password cracking: `john`, `hashcat`

**Planner Agent Tools:**
- Minimal MCP tools (mostly uses handoffs)
- Focus on coordination, not execution

**Summary Agent Tools:**
- Document formatting tools
- Report generation utilities

---

### 5. Workflow Execution Architecture

#### **Executor Pattern**

The `Executor` class manages workflow lifecycle:

```python
class Executor:
    def __init__(self):
        self._swarm = None              # Compiled LangGraph workflow
        self._config = None             # Thread configuration
        self._thread_id = None          # Conversation thread ID
        self._current_model = None      # Active LLM model
        self._processed_message_ids = set()  # Deduplication tracking
    
    async def initialize_swarm(self, model_info, thread_config):
        """Initialize swarm with specific model and thread"""
        # 1. Update LLM configuration
        # 2. Create thread config
        # 3. Compile workflow with checkpointer + store
        # 4. Mark as ready
    
    async def execute_workflow(self, user_input, config):
        """Execute workflow and stream results"""
        # 1. Create HumanMessage from input
        # 2. Stream workflow execution
        # 3. Process and deduplicate messages
        # 4. Format events for frontend
        # 5. Yield events as they occur
```

#### **Async Streaming Architecture**

The system uses async streaming for real-time updates:

```python
# Workflow execution
async for stream_item in workflow.astream(
    inputs={"messages": [HumanMessage(content=user_input)]},
    config={"configurable": {"thread_id": thread_id}},
    stream_mode="updates",  # Stream state updates
    subgraphs=True          # Include subgraph updates
):
    namespace, output = stream_item
    # Process output → Format event → Yield to frontend
```

**Stream Event Types:**
```python
# 1. Agent Message Event
{
    "type": "message",
    "message_type": "ai",           # "user" | "ai" | "tool"
    "agent_name": "Reconnaissance",
    "content": "Executing nmap scan...",
    "step_count": 5
}

# 2. Tool Execution Event
{
    "type": "message",
    "message_type": "tool",
    "tool_name": "nmap",
    "tool_display_name": "Nmap",
    "content": "Starting Nmap 7.95...",
    "step_count": 6
}

# 3. Workflow Complete Event
{
    "type": "workflow_complete",
    "step_count": 15
}
```

#### **Message Deduplication**

Prevents duplicate display of messages:

```python
def _should_display_message(self, message, agent_name, step_count):
    """Determine whether to display message"""
    # Generate unique message ID
    message_id = getattr(message, 'id', f"{agent_name}_{hash(content)}")
    
    # Check if already processed
    if message_id in self._processed_message_ids:
        return False, None
    
    # Mark as processed
    self._processed_message_ids.add(message_id)
    return True, message_type
```

---

### Multi-Agent Design Rationale

**Why Multi-Agent Architecture?**

| Aspect | Single Agent | Multi-Agent (✓) |
|--------|--------------|-----------------|
| **Specialization** | Poor (general knowledge) | Excellent (expert agents) |
| **Token Efficiency** | Poor (long context) | Good (distributed context) |
| **Tool Management** | Complex (all tools loaded) | Simple (agent-specific tools) |
| **Maintainability** | Monolithic prompts | Modular agent prompts |
| **Debugging** | Difficult attribution | Agent-specific logs |
| **Scalability** | Limited (context window) | Excellent (add new agents) |
| **Coordination** | N/A | Explicit handoff patterns |

**Result:** Multi-agent architecture provides **40% token savings**, better specialization, clearer observability, and easier maintenance.

**Key Design Decisions:**

1. **ReAct Pattern:** Each agent independently reasons and acts (no centralized orchestrator micromanaging)
2. **Handoff Tools:** Explicit agent-to-agent communication (vs implicit routing)
3. **Shared State:** All agents see full conversation (vs isolated contexts)
4. **Two-Tier Memory:** Short-term (checkpointer) + Long-term (vector store)
5. **MCP Protocol:** Standardized tool integration (vs custom wrappers)
6. **Async Streaming:** Real-time updates (vs batch processing)

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

## 🤖 Agent Roles & Responsibilities

### 1. Planner Agent 🎯

**Primary Role:** Strategic Coordinator & Task Orchestrator

**Core Responsibilities:**
- Parse user objectives into actionable subtasks
- Develop attack strategies and execution plans
- Route tasks to appropriate specialist agents
- Monitor progress and adjust strategy dynamically
- Maintain overall mission coherence

**Communication Pattern:**
```
User Request → Planner analyzes → Decomposes into tasks → Routes to specialists
                                                              ↓
Specialist completes task → Returns to Planner → Planner evaluates → Next task
```

**Tool Access:**
- **Handoff Tools:** Transfer to Reconnaissance, Initial_Access, Summary
- **Memory Tools:** Store/retrieve strategic decisions
- **MCP Tools:** Minimal (focuses on coordination, not execution)

**Decision Making:**
```
IF objective requires information gathering:
    → Transfer to Reconnaissance
ELSE IF exploitation planning needed:
    → Transfer to Initial_Access
ELSE IF comprehensive report needed:
    → Transfer to Summary
ELSE:
    → Continue coordinating
```

**Example Workflow:**
```
User: "Test 192.168.1.100 for vulnerabilities"

Planner:
  Step 1: "I need to gather information first"
          → Handoff to Reconnaissance
  
  [Reconnaissance completes scan]
  
  Step 2: "Found Apache 2.4.49 - potential CVE-2021-41773"
          → Handoff to Initial_Access for exploit assessment
  
  [Initial_Access analyzes exploitability]
  
  Step 3: "Confirmed exploitable. Now need comprehensive report"
          → Handoff to Summary
  
  [Summary generates report]
  
  Step 4: "Mission complete. Report delivered."
```

**Prompt Design:**
- Strategic thinking emphasis
- High-level task decomposition
- Coordination and routing logic
- Progress tracking

---

### 2. Reconnaissance Agent 🔍

**Primary Role:** Information Gathering & Intelligence Collection

**Core Responsibilities:**
- Network discovery and enumeration
- Service identification and versioning
- Vulnerability scanning and assessment
- Web application enumeration
- DNS and WHOIS reconnaissance

**Specialization Areas:**
- **Network Scanning:** Identify live hosts, open ports
- **Service Enumeration:** Determine running services and versions
- **Vulnerability Detection:** Find known CVEs and misconfigurations
- **Web Reconnaissance:** Directory/file enumeration, technology detection
- **OSINT:** DNS, WHOIS, subdomain enumeration

**Tool Arsenal (20+ tools):**

**Network Scanners:**
- `nmap` - Comprehensive port scanning and service detection
- `masscan` - High-speed port scanning for large networks
- `unicornscan` - Asynchronous network scanning
- `hping3` - TCP/IP packet crafting and analysis
- `fping`, `arping` - Host discovery utilities

**Vulnerability Scanners:**
- `nuclei` - Template-based vulnerability scanning
- `nikto` - Web server vulnerability scanner
- `wpscan` - WordPress security scanner
- `joomscan` - Joomla CMS scanner

**Enumeration Tools:**
- `gobuster` - Directory/file brute-forcing
- `dirb`, `dirbuster` - Web content discovery
- `wfuzz`, `ffuf` - Web fuzzing tools
- `enum4linux` - SMB/Samba enumeration
- `smbclient` - SMB client for file sharing
- `snmpwalk` - SNMP enumeration

**Typical Workflow:**
```
1. Host Discovery:
   nmap -sn 192.168.1.0/24
   → Identifies: 192.168.1.100, 192.168.1.105 (live hosts)

2. Port Scanning:
   masscan -p1-65535 192.168.1.100 --rate=1000
   → Identifies: 22/tcp, 80/tcp, 443/tcp (open ports)

3. Service Enumeration:
   nmap -sV -sC -p22,80,443 192.168.1.100
   → Identifies: SSH 7.4, Apache 2.4.49, OpenSSL 1.1.1

4. Vulnerability Scanning:
   nuclei -u https://192.168.1.100 -t cves/
   → Identifies: CVE-2021-41773 (Apache path traversal)

5. Web Enumeration:
   gobuster dir -u https://192.168.1.100 -w wordlist.txt
   → Identifies: /admin, /uploads, /config.php
```

**Output Format:**
```
TACTICAL ANALYSIS
Host: 192.168.1.100
Status: UP (0.015s latency)

OPEN PORTS:
- 22/tcp: OpenSSH 7.4p1 (protocol 2.0)
- 80/tcp: Apache httpd 2.4.49 ((Unix))
- 443/tcp: Apache httpd 2.4.49 ((Unix)) SSL

VULNERABILITIES:
[CRITICAL] CVE-2021-41773 - Apache HTTP Server 2.4.49 Path Traversal
[HIGH] CVE-2021-42013 - Apache HTTP Server 2.4.49/2.4.50 RCE
[MEDIUM] SSL Certificate Self-Signed

INTELLIGENCE ASSESSMENT:
Target is running outdated Apache version with critical RCE vulnerabilities.
Recommend immediate exploitation assessment.

COORDINATION: Transferring to Initial_Access for exploit planning...
```

**Communication Pattern:**
- Receives tasks from Planner
- Executes reconnaissance autonomously
- Reports findings with structured analysis
- Hands back to Planner or directly to Initial_Access if critical vulnerability found

---

### 3. Initial_Access Agent 🎯

**Primary Role:** Exploitation Planning & Credential Attacks

**Core Responsibilities:**
- Analyze vulnerabilities for exploitability
- Plan exploitation strategies
- Execute credential attacks (with approval)
- Assess attack vectors and feasibility
- Generate proof-of-concept exploit plans

**Specialization Areas:**
- **Exploit Development:** Metasploit module selection and configuration
- **Credential Attacks:** Password spraying, brute-forcing
- **Web Exploitation:** SQLi, XSS, command injection
- **Password Cracking:** Hash cracking with john/hashcat
- **Post-Exploitation Planning:** Privilege escalation, persistence

**Tool Arsenal (15+ tools):**

**Exploitation Frameworks:**
- `msfconsole` - Metasploit Framework for exploit execution
- `msfvenom` - Payload generation
- `beef` - Browser Exploitation Framework
- `setoolkit` - Social Engineering Toolkit
- `armitage` - GUI for Metasploit

**Credential Attack Tools:**
- `hydra` - Network logon cracker (SSH, FTP, HTTP, etc.)
- `medusa` - Parallel password brute-forcer
- `ncrack` - High-speed network authentication cracker
- `patator` - Multi-purpose brute-forcer
- `crowbar` - Brute-forcing tool for OpenVPN, RDP, SSH

**Password Cracking:**
- `john` - John the Ripper password cracker
- `hashcat` - Advanced GPU-based hash cracking

**Web Exploitation:**
- `sqlmap` - Automatic SQL injection exploitation
- `commix` - Command injection exploitation
- `xsser` - Cross-site scripting framework

**Safety Mechanism:**
```python
# All operations require human approval
@require_approval(risk_level="HIGH")
def execute_exploit(target, exploit_module):
    """Execute exploitation attempt"""
    # User must approve before execution
    # Frontend displays approval dialog
    # Agent waits for confirmation
```

**Typical Workflow:**
```
1. Vulnerability Analysis:
   Input: CVE-2021-41773 identified on Apache 2.4.49
   Action: Search msfconsole for exploit module
   
   search cve-2021-41773
   → Found: exploit/multi/http/apache_normalize_path_rce

2. Exploit Configuration:
   use exploit/multi/http/apache_normalize_path_rce
   set RHOSTS 192.168.1.100
   set RPORT 80
   set TARGETURI /
   
3. Approval Request:
   ⚠️ HIGH-RISK OPERATION ⚠️
   Action: Execute remote code execution exploit
   Target: 192.168.1.100:80
   Module: apache_normalize_path_rce
   
   [User Approval Required]
   ✅ Approve  ❌ Deny

4. (If Approved) Execution:
   exploit
   → Payload delivered
   → Session established
   
5. Report:
   EXPLOITATION ASSESSMENT
   
   Target: 192.168.1.100
   Vulnerability: CVE-2021-41773
   Exploit: apache_normalize_path_rce
   
   Result: ✅ SUCCESSFUL
   - Remote code execution confirmed
   - Reverse shell established (session 1)
   - User context: www-data
   
   RECOMMENDATIONS:
   - Immediate patching to Apache 2.4.51+
   - Web application firewall deployment
   - Principle of least privilege enforcement
```

**Alternative Workflow (Credential Attack):**
```
1. Service Identification:
   Input: SSH service on 192.168.1.100:22
   
2. Credential Attack Planning:
   Tool: hydra
   Target: SSH service
   Wordlists: common_users.txt, rockyou.txt
   
3. Approval Request:
   ⚠️ MEDIUM-RISK OPERATION ⚠️
   Action: SSH credential brute-force
   Target: 192.168.1.100:22
   Users: admin, root, user
   
   [User Approval Required]

4. (If Approved) Execution:
   hydra -L users.txt -P rockyou.txt ssh://192.168.1.100
   
   → Found: admin:password123
   
5. Validation:
   ssh admin@192.168.1.100
   → Login successful
   
6. Report:
   CREDENTIAL ATTACK RESULTS
   
   Service: SSH (OpenSSH 7.4)
   Valid Credentials Found:
   - Username: admin
   - Password: password123
   
   RECOMMENDATIONS:
   - Enforce strong password policy
   - Implement account lockout after failed attempts
   - Enable multi-factor authentication
   - Disable password authentication (use keys)
```

**Communication Pattern:**
- Receives exploitation tasks from Planner
- Requests approval for high-risk operations
- Executes approved attacks
- Reports detailed results with remediation advice
- Hands back to Planner or Summary for reporting

---

### 4. Summary Agent 📝

**Primary Role:** Report Generation & Findings Aggregation

**Core Responsibilities:**
- Synthesize findings from all agents
- Generate comprehensive security reports
- Create executive summaries
- Provide remediation recommendations
- Format output for various audiences

**Output Formats:**

**1. Executive Summary (for management):**
```
EXECUTIVE SUMMARY
Assessment Date: 2025-11-25
Target: 192.168.1.100 (example.com)

OVERALL RISK: CRITICAL

KEY FINDINGS:
• [CRITICAL] Remote Code Execution (CVE-2021-41773)
  Impact: Complete system compromise possible
  
• [HIGH] Weak Credentials on SSH Service
  Impact: Unauthorized administrative access

• [MEDIUM] Outdated SSL Configuration
  Impact: Man-in-the-middle attack risk

BUSINESS IMPACT:
- Data breach potential: HIGH
- System availability risk: CRITICAL
- Compliance violation: PCI-DSS, GDPR

RECOMMENDED ACTIONS (Priority Order):
1. Immediate: Patch Apache to version 2.4.51+
2. Urgent: Enforce strong password policy
3. High: Update SSL/TLS configuration
```

**2. Technical Detailed Report:**
```
TECHNICAL SECURITY ASSESSMENT REPORT

TARGET INFORMATION
IP Address: 192.168.1.100
Hostname: example.com
OS: Linux (kernel 5.4.0)
Assessment Duration: 2 hours

METHODOLOGY
• Network reconnaissance (nmap, masscan)
• Service enumeration (nmap -sV)
• Vulnerability scanning (nuclei, nikto)
• Exploitation testing (msfconsole)
• Credential attacks (hydra)

DETAILED FINDINGS

[1] CVE-2021-41773 - Apache Path Traversal RCE
Severity: CRITICAL (CVSS 9.8)
Port: 80/tcp, 443/tcp
Service: Apache HTTP Server 2.4.49

Description:
Apache HTTP Server versions 2.4.49 and 2.4.50 are vulnerable to a path
traversal attack that can lead to remote code execution. An attacker can
map URLs to files outside the expected document root.

Proof of Concept:
$ curl 'http://192.168.1.100/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh' \
  -d 'echo Content-Type: text/plain; echo; id'
→ uid=1(daemon) gid=1(daemon) groups=1(daemon)

Exploitation Confirmed: YES
Metasploit Module: exploit/multi/http/apache_normalize_path_rce

Impact:
- Remote code execution as daemon user
- File system access
- Potential privilege escalation

Remediation:
1. Upgrade Apache to version 2.4.51 or later
2. Apply vendor security patches
3. Implement WAF rules to block path traversal attempts
4. Review web server configuration

References:
- CVE-2021-41773
- https://httpd.apache.org/security/vulnerabilities_24.html

[2] Weak SSH Credentials
Severity: HIGH
Port: 22/tcp
Service: OpenSSH 7.4

Description:
SSH service accepts weak password authentication. Common credentials
were successfully brute-forced.

Credentials Found:
- admin:password123

Attack Method:
$ hydra -l admin -P rockyou.txt ssh://192.168.1.100
[22][ssh] host: 192.168.1.100 login: admin password: password123

Impact:
- Unauthorized administrative access
- Data exfiltration
- Lateral movement
- Persistence establishment

Remediation:
1. Enforce strong password policy (min 16 chars, complexity)
2. Implement account lockout (5 failed attempts)
3. Disable password authentication, require SSH keys
4. Enable multi-factor authentication
5. Restrict SSH access by source IP

[3] Outdated SSL Configuration
Severity: MEDIUM
Port: 443/tcp
Protocol: TLS 1.0, TLS 1.1

Description:
Server supports outdated TLS protocols (TLS 1.0, TLS 1.1) that are
deprecated due to known vulnerabilities.

Impact:
- Man-in-the-middle attack risk
- Compliance violation (PCI-DSS requires TLS 1.2+)

Remediation:
1. Disable TLS 1.0 and TLS 1.1
2. Enable only TLS 1.2 and TLS 1.3
3. Configure strong cipher suites
4. Implement HSTS header

VULNERABILITY SUMMARY
┌──────────┬───────┐
│ Severity │ Count │
├──────────┼───────┤
│ Critical │   1   │
│ High     │   1   │
│ Medium   │   1   │
│ Low      │   0   │
└──────────┴───────┘

REMEDIATION ROADMAP

Phase 1 (Immediate - 24 hours):
✓ Apply Apache security patch (CVE-2021-41773)
✓ Disable compromised credentials
✓ Enable SSH key-only authentication

Phase 2 (Urgent - 1 week):
✓ Implement strong password policy
✓ Deploy web application firewall
✓ Update SSL/TLS configuration

Phase 3 (High - 1 month):
✓ Conduct follow-up assessment
✓ Implement intrusion detection system
✓ Security awareness training for admins
```

**3. Vulnerability Matrix:**
```
VULNERABILITY MATRIX

┌─────────────────────────────────────────────────────────────────┐
│ ID  │ Vulnerability        │ Severity │ CVSS │ Exploited │ Remediation │
├─────┼─────────────────────┼──────────┼──────┼───────────┼─────────────┤
│ V-1 │ Apache Path Traversal│ Critical │ 9.8  │    ✓     │ Patch 2.4.51│
│ V-2 │ Weak SSH Credentials │   High   │ 8.1  │    ✓     │ MFA + Keys  │
│ V-3 │ Outdated TLS         │  Medium  │ 5.3  │    ✗     │ TLS 1.2+    │
└─────┴─────────────────────┴──────────┴──────┴───────────┴─────────────┘
```

**Communication Pattern:**
- Receives aggregation request from Planner
- Reviews entire conversation history via MessagesState
- Extracts key findings from Recon and InitAccess outputs
- Formats into structured report
- Returns to Planner for final delivery

**Tool Access:**
- **Memory Tools:** Retrieve all findings from memory
- **Handoff Tools:** Return to Planner after completion
- **Formatting Tools:** Markdown, JSON, PDF generation

---

### Agent Coordination Examples

#### **Example 1: Full Penetration Test Workflow**

```
User: "Perform penetration test on 192.168.1.100"

┌──────────┐
│ PLANNER  │
└────┬─────┘
     │
     ├─► STRATEGIC INTELLIGENCE:
     │   Objective: Comprehensive penetration test
     │   Phase 1: Reconnaissance
     │   Phase 2: Vulnerability Assessment
     │   Phase 3: Exploitation (if authorized)
     │   Phase 4: Reporting
     │
     └─► Transfer to Reconnaissance...

┌──────────────────┐
│ RECONNAISSANCE   │
└────┬─────────────┘
     │
     ├─► TACTICAL ANALYSIS:
     │   Executing nmap -sV -sC 192.168.1.100
     │   [Tool Output: 22/tcp, 80/tcp, 443/tcp open]
     │   
     ├─► INTELLIGENCE ACTION:
     │   Executing nuclei -u https://192.168.1.100
     │   [Tool Output: CVE-2021-41773 detected]
     │   
     ├─► STRATEGIC IMPLICATIONS:
     │   Critical vulnerability found: Apache RCE
     │   Recommend immediate exploitation assessment
     │
     └─► Transfer back to Planner...

┌──────────┐
│ PLANNER  │
└────┬─────┘
     │
     ├─► COORDINATION:
     │   Reconnaissance complete
     │   Critical finding: CVE-2021-41773
     │   Next phase: Exploitation assessment
     │
     └─► Transfer to Initial_Access...

┌──────────────────┐
│ INITIAL_ACCESS   │
└────┬─────────────┘
     │
     ├─► EXPLOITATION ASSESSMENT:
     │   Analyzing CVE-2021-41773
     │   Metasploit module available
     │   
     ├─► APPROVAL REQUEST:
     │   ⚠️ HIGH-RISK OPERATION ⚠️
     │   Action: Execute RCE exploit
     │   [User Approves]
     │   
     ├─► EXECUTION:
     │   msfconsole: exploit/multi/http/apache_normalize_path_rce
     │   [Tool Output: Session established]
     │   
     ├─► RESULTS:
     │   Exploitation successful
     │   RCE confirmed with proof
     │
     └─► Transfer back to Planner...

┌──────────┐
│ PLANNER  │
└────┬─────┘
     │
     ├─► MISSION ASSESSMENT:
     │   All phases complete
     │   Critical findings confirmed
     │   Ready for comprehensive report
     │
     └─► Transfer to Summary...

┌──────────┐
│ SUMMARY  │
└────┬─────┘
     │
     ├─► REPORT GENERATION:
     │   Aggregating findings from all agents
     │   Memory search for all CVEs found
     │   Formatting executive summary
     │   Creating technical report
     │   Developing remediation roadmap
     │   
     └─► [Complete Report Delivered]

┌──────────┐
│ PLANNER  │
└────┬─────┘
     │
     └─► MISSION COMPLETE:
         Comprehensive penetration test finished
         Report delivered to user
```

**Total Agent Transitions:** 5  
**Total Tool Executions:** 7  
**Conversation Turns:** 12

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

## ⚙️ Configuration

### Environment Variables

```bash
# .env file

# OpenAI Configuration (Required)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0

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
2. Generate diagnostic report:
   ```bash
   python -m src.utils.diagnostics.generate_report
   ```

---

## 📚 Documentation

### Complete Documentation Set

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture, agent roles, design rationale  
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
- ✅ Real-time cost tracking per agent
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
