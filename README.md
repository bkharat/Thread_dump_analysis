# Thread Dump Analysis - AI Agent System

Agentic AI system for analyzing thread dumps from webMethods Integration Server with automated monitoring, analysis, and remediation.

## 🎯 Project Overview

This project implements an AI-powered thread dump analysis system with the following capabilities:
- **Real-time Monitoring**: Detect hung threads and performance issues
- **AI Analysis**: Use LangGraph and LLMs to analyze thread dumps
- **Specialist Agents**: Dedicated agents for GC and CPU analysis
- **Automated Remediation**: Safe, automated fixes for common issues
- **Dashboard**: Real-time visualization of server health
- **Slack Integration**: Instant alerts for critical issues

## 📋 Team Assignments

### 🔴 Tapaswini - Monitor Agent & Slack Notifications
**Directory**: `agents/monitor/`
**Tasks**:
- Create monitoring agent to poll webMethods Integration Server
- Detect hung threads, deadlocks, and blocked threads
- Send formatted alerts to Slack with action buttons
- Implement alert deduplication

### 🟢 Ranadeep - Collector & Analyzer Agents (LangGraph)
**Directories**: `agents/collector/`, `agents/analyzer/`
**Tasks**:
- Build LangGraph workflow for thread dump collection
- Create LangGraph workflow for AI-powered analysis
- Parse thread dumps and identify patterns
- Generate recommendations using LLM

### 🔵 Vinay - GC & CPU Specialist Agents (LangGraph)
**Directories**: `agents/gc_specialist/`, `agents/cpu_specialist/`
**Tasks**:
- Create GC specialist agent with LangGraph
- Analyze garbage collection logs and patterns
- Create CPU specialist agent with LangGraph
- Identify CPU hotspots and optimization opportunities

### 🟡 Bhagwan - Monitoring Dashboard
**Directory**: `dashboard/`
**Tasks**:
- Build Streamlit/Dash dashboard
- Create overview, thread analysis, and performance panels
- Display AI insights and recommendations
- Show alert history and metrics

### 🟣 Sai - MCP Server & Remediation Agent
**Directories**: `mcp_server/`, `agents/remediation/`
**Tasks**:
- Implement MCP server with tools and resources
- Create remediation agent with LangGraph
- Implement safe remediation actions with rollback
- Log all remediation activities

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# - webMethods server URL and credentials
# - Slack webhook URL
# - OpenAI or Anthropic API key
```

### 3. Implement Your Component

Each team member should:
1. Navigate to your assigned directory
2. Create your agent/component files
3. Follow the implementation plan in `IMPLEMENTATION_PLAN.md`
4. Refer to `TEAM_ASSIGNMENTS.md` for detailed instructions
5. Use `QUICK_START_GUIDE.md` for code examples

## 📁 Project Structure

```
thread_dump_analysis/
├── README.md                          # This file
├── IMPLEMENTATION_PLAN.md             # Detailed 1-hour implementation plan
├── TEAM_ASSIGNMENTS.md                # Individual team member assignments
├── PROJECT_STRUCTURE.md               # Complete file organization guide
├── QUICK_START_GUIDE.md               # Step-by-step implementation guide
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
│
├── shared/                            # Shared utilities (All team members)
│   └── __init__.py
│
├── agents/                            # AI Agents
│   ├── monitor/                       # 🔴 Tapaswini
│   ├── collector/                     # 🟢 Ranadeep
│   ├── analyzer/                      # 🟢 Ranadeep
│   ├── gc_specialist/                 # 🔵 Vinay
│   ├── cpu_specialist/                # 🔵 Vinay
│   └── remediation/                   # 🟣 Sai
│
├── mcp_server/                        # 🟣 Sai
├── dashboard/                         # 🟡 Bhagwan
├── tests/                             # Unit tests
├── logs/                              # Application logs
├── data/                              # Data storage
└── scripts/                           # Utility scripts
```

## 📚 Documentation

- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)**: Complete 60-minute implementation timeline
- **[TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md)**: Detailed assignments for each team member
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**: File organization and responsibilities
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)**: Step-by-step implementation guide with code examples

## 🔧 Development Workflow

### For Each Team Member:

1. **Pull latest code**
   ```bash
   git pull origin main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-component-name
   ```

3. **Implement your component**
   - Follow your assignment in `TEAM_ASSIGNMENTS.md`
   - Use code examples from `QUICK_START_GUIDE.md`
   - Test your component independently

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat(component): description of changes"
   git push origin feature/your-component-name
   ```

5. **Create pull request**
   - Request review from team
   - Merge after approval

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_integration.py

# Run with coverage
pytest --cov=agents --cov=shared
```

## 🏃 Running Components

```bash
# Monitor Agent (Tapaswini)
python -m agents.monitor.monitor_agent

# Collector Agent (Ranadeep)
python -m agents.collector.collector_agent

# Analyzer Agent (Ranadeep)
python -m agents.analyzer.analyzer_agent

# GC Specialist (Vinay)
python -m agents.gc_specialist.gc_agent

# CPU Specialist (Vinay)
python -m agents.cpu_specialist.cpu_agent

# MCP Server (Sai)
python -m mcp_server.server

# Remediation Agent (Sai)
python -m agents.remediation.remediation_agent

# Dashboard (Bhagwan)
streamlit run dashboard/app.py
```

## 🎯 Success Criteria

At the end of the implementation:
- ✅ Monitor detects hung threads within 30 seconds
- ✅ Slack notifications sent for critical issues
- ✅ Thread dumps collected and parsed successfully
- ✅ AI analysis identifies root causes accurately
- ✅ GC and CPU specialists provide actionable insights
- ✅ Dashboard displays real-time data
- ✅ MCP server exposes tools for operations
- ✅ Remediation actions execute safely with rollback
- ✅ End-to-end workflow completes in < 2 minutes

## 🆘 Support

**Questions or Blockers?**
- Check the documentation files first
- Post in team Slack channel
- Coordinate with team members for integration points

## 📝 License

Internal project for webMethods Integration Server monitoring.

---

**Let's build something amazing! 🚀**
