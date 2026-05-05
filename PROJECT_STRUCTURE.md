# Project Structure & File Organization

## Directory Layout

```
thread_dump_analysis/
│
├── README.md                          # Project overview
├── IMPLEMENTATION_PLAN.md             # Detailed 1-hour plan
├── TEAM_ASSIGNMENTS.md                # Individual assignments
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
│
├── shared/                            # Shared utilities (All team members)
│   ├── __init__.py
│   ├── config.py                      # Configuration management
│   ├── models.py                      # Data models
│   └── utils.py                       # Utility functions
│
├── agents/                            # AI Agents
│   │
│   ├── monitor/                       # 🔴 Tapaswini
│   │   ├── __init__.py
│   │   ├── monitor_agent.py           # Main monitoring logic
│   │   ├── slack_notifier.py          # Slack integration
│   │   └── scheduler.py               # Periodic task scheduling
│   │
│   ├── collector/                     # 🟢 Ranadeep (Part 1)
│   │   ├── __init__.py
│   │   ├── collector_agent.py         # Thread dump collection
│   │   ├── webmethods_client.py       # API client
│   │   └── parser.py                  # Thread dump parser
│   │
│   ├── analyzer/                      # 🟢 Ranadeep (Part 2)
│   │   ├── __init__.py
│   │   ├── analyzer_agent.py          # AI-powered analysis
│   │   ├── prompts.py                 # LLM prompts
│   │   └── patterns.py                # Pattern detection
│   │
│   ├── gc_specialist/                 # 🔵 Vinay (Part 1)
│   │   ├── __init__.py
│   │   ├── gc_agent.py                # GC analysis agent
│   │   ├── gc_parser.py               # GC log parser
│   │   └── tuning_recommendations.py  # JVM tuning advice
│   │
│   ├── cpu_specialist/                # 🔵 Vinay (Part 2)
│   │   ├── __init__.py
│   │   ├── cpu_agent.py               # CPU analysis agent
│   │   ├── profiler.py                # CPU profiling
│   │   └── optimization_tips.py       # Optimization suggestions
│   │
│   └── remediation/                   # 🟣 Sai (Part 2)
│       ├── __init__.py
│       ├── remediation_agent.py       # Automated remediation
│       ├── actions.py                 # Remediation actions
│       └── safety_checks.py           # Safety validations
│
├── mcp_server/                        # 🟣 Sai (Part 1)
│   ├── __init__.py
│   ├── server.py                      # MCP server implementation
│   ├── tools.py                       # MCP tools
│   └── resources.py                   # MCP resources
│
├── dashboard/                         # 🟡 Bhagwan
│   ├── __init__.py
│   ├── app.py                         # Main dashboard app
│   ├── components/
│   │   ├── __init__.py
│   │   ├── overview.py                # Overview panel
│   │   ├── thread_analysis.py         # Thread analysis panel
│   │   ├── performance_metrics.py     # Performance panel
│   │   ├── ai_insights.py             # AI insights panel
│   │   └── alert_history.py           # Alert history panel
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py            # Data retrieval
│   │   └── visualizations.py          # Chart helpers
│   └── assets/
│       ├── styles.css                 # Custom styles
│       └── logo.png                   # Logo image
│
├── tests/                             # Unit tests
│   ├── __init__.py
│   ├── test_monitor.py
│   ├── test_collector.py
│   ├── test_analyzer.py
│   ├── test_specialists.py
│   ├── test_remediation.py
│   └── test_integration.py
│
├── logs/                              # Application logs
│   ├── monitor.log
│   ├── agents.log
│   └── remediation.log
│
├── data/                              # Data storage
│   ├── thread_dumps/                  # Collected thread dumps
│   ├── analysis_results/              # Analysis outputs
│   └── alerts/                        # Alert history
│
└── scripts/                           # Utility scripts
    ├── setup.sh                       # Setup script
    ├── start_all.sh                   # Start all components
    └── simulate_hung_thread.py        # Testing script
```

---

## File Responsibilities

### Shared Components (First 10 minutes - All team members)

#### [`shared/config.py`](shared/config.py)
- Environment variable management
- Configuration constants
- Threshold definitions

#### [`shared/models.py`](shared/models.py)
- `ThreadInfo` - Individual thread data
- `ThreadDumpData` - Complete dump data
- `AlertMessage` - Alert structure
- `AnalysisResult` - Analysis output
- `RemediationAction` - Remediation details

#### [`shared/utils.py`](shared/utils.py)
- `call_webmethods_api()` - API wrapper
- `parse_thread_dump()` - Dump parser
- `format_slack_message()` - Slack formatter
- `calculate_thread_metrics()` - Metrics calculator

---

### 🔴 Tapaswini's Files

#### [`agents/monitor/monitor_agent.py`](agents/monitor/monitor_agent.py)
**Purpose:** Main monitoring logic
**Key Classes/Functions:**
- `MonitorAgent` class
- `monitor_integration_server()` - Poll server
- `detect_hung_threads()` - Identify issues
- `check_deadlocks()` - Detect deadlocks
- `trigger_collection()` - Start collection

#### [`agents/monitor/slack_notifier.py`](agents/monitor/slack_notifier.py)
**Purpose:** Slack notification handling
**Key Classes/Functions:**
- `SlackNotifier` class
- `send_alert()` - Send notification
- `format_alert_message()` - Format message
- `add_action_buttons()` - Add buttons
- `deduplicate_alerts()` - Prevent spam

#### [`agents/monitor/scheduler.py`](agents/monitor/scheduler.py)
**Purpose:** Periodic task scheduling
**Key Classes/Functions:**
- `MonitorScheduler` class
- `start_monitoring()` - Begin polling
- `stop_monitoring()` - Stop polling
- `adjust_interval()` - Change frequency

---

### 🟢 Ranadeep's Files

#### [`agents/collector/collector_agent.py`](agents/collector/collector_agent.py)
**Purpose:** Thread dump collection with LangGraph
**Key Classes/Functions:**
- `CollectorAgent` class
- `create_collector_graph()` - Build workflow
- `connect_to_server()` - Server connection
- `collect_thread_dump()` - Dump collection
- `parse_threads()` - Parse dump
- `store_data()` - Save results

#### [`agents/collector/webmethods_client.py`](agents/collector/webmethods_client.py)
**Purpose:** webMethods API client
**Key Classes/Functions:**
- `WebMethodsClient` class
- `get_thread_dump()` - Fetch dump
- `get_server_stats()` - Get statistics
- `authenticate()` - Handle auth

#### [`agents/analyzer/analyzer_agent.py`](agents/analyzer/analyzer_agent.py)
**Purpose:** AI-powered thread analysis with LangGraph
**Key Classes/Functions:**
- `AnalyzerAgent` class
- `create_analyzer_graph()` - Build workflow
- `load_thread_dump()` - Load data
- `analyze_patterns()` - Pattern analysis
- `detect_issues()` - Issue detection
- `generate_report()` - Create report

#### [`agents/analyzer/prompts.py`](agents/analyzer/prompts.py)
**Purpose:** LLM prompts for analysis
**Key Constants:**
- `ANALYSIS_PROMPT` - Main analysis prompt
- `DEADLOCK_DETECTION_PROMPT` - Deadlock prompt
- `RECOMMENDATION_PROMPT` - Recommendation prompt

---

### 🔵 Vinay's Files

#### [`agents/gc_specialist/gc_agent.py`](agents/gc_specialist/gc_agent.py)
**Purpose:** GC analysis with LangGraph
**Key Classes/Functions:**
- `GCSpecialistAgent` class
- `create_gc_graph()` - Build workflow
- `collect_gc_logs()` - Gather GC data
- `analyze_gc_patterns()` - Analyze patterns
- `detect_memory_issues()` - Find issues
- `recommend_tuning()` - JVM tuning

#### [`agents/gc_specialist/gc_parser.py`](agents/gc_specialist/gc_parser.py)
**Purpose:** Parse GC logs
**Key Classes/Functions:**
- `GCLogParser` class
- `parse_gc_log()` - Parse log
- `extract_pause_times()` - Get pauses
- `calculate_gc_metrics()` - Metrics

#### [`agents/cpu_specialist/cpu_agent.py`](agents/cpu_specialist/cpu_agent.py)
**Purpose:** CPU analysis with LangGraph
**Key Classes/Functions:**
- `CPUSpecialistAgent` class
- `create_cpu_graph()` - Build workflow
- `collect_cpu_metrics()` - Gather CPU data
- `correlate_with_threads()` - Correlate data
- `identify_hotspots()` - Find hotspots
- `suggest_optimizations()` - Optimize

#### [`agents/cpu_specialist/profiler.py`](agents/cpu_specialist/profiler.py)
**Purpose:** CPU profiling utilities
**Key Classes/Functions:**
- `CPUProfiler` class
- `profile_thread()` - Profile thread
- `get_cpu_usage()` - Get usage
- `identify_blocking_calls()` - Find blocks

---

### 🟡 Bhagwan's Files

#### [`dashboard/app.py`](dashboard/app.py)
**Purpose:** Main dashboard application
**Key Functions:**
- `main()` - Entry point
- `setup_layout()` - Create layout
- `refresh_data()` - Update data
- `handle_user_actions()` - Handle clicks

#### [`dashboard/components/overview.py`](dashboard/components/overview.py)
**Purpose:** Overview panel
**Key Functions:**
- `render_overview()` - Render panel
- `show_server_health()` - Health status
- `show_thread_count()` - Thread metrics
- `show_active_alerts()` - Alert count

#### [`dashboard/components/thread_analysis.py`](dashboard/components/thread_analysis.py)
**Purpose:** Thread analysis panel
**Key Functions:**
- `render_thread_analysis()` - Render panel
- `show_thread_list()` - List threads
- `show_stack_trace()` - Display trace
- `show_thread_timeline()` - Timeline chart

#### [`dashboard/components/performance_metrics.py`](dashboard/components/performance_metrics.py)
**Purpose:** Performance metrics panel
**Key Functions:**
- `render_performance_metrics()` - Render panel
- `show_cpu_graph()` - CPU chart
- `show_memory_graph()` - Memory chart
- `show_gc_stats()` - GC statistics

#### [`dashboard/components/ai_insights.py`](dashboard/components/ai_insights.py)
**Purpose:** AI insights panel
**Key Functions:**
- `render_ai_insights()` - Render panel
- `show_analysis_results()` - Analysis
- `show_recommendations()` - Recommendations
- `show_specialist_insights()` - Specialist views

#### [`dashboard/components/alert_history.py`](dashboard/components/alert_history.py)
**Purpose:** Alert history panel
**Key Functions:**
- `render_alert_history()` - Render panel
- `show_alert_table()` - Alert table
- `show_resolution_status()` - Status
- `show_time_to_resolution()` - Metrics

---

### 🟣 Sai's Files

#### [`mcp_server/server.py`](mcp_server/server.py)
**Purpose:** MCP server implementation
**Key Classes/Functions:**
- `ThreadDumpMCPServer` class
- `setup_tools()` - Register tools
- `setup_resources()` - Register resources
- `start_server()` - Start server

#### [`mcp_server/tools.py`](mcp_server/tools.py)
**Purpose:** MCP tool definitions
**Key Functions:**
- `get_thread_dump()` - Tool: Get dump
- `analyze_thread()` - Tool: Analyze
- `execute_remediation()` - Tool: Remediate
- `get_server_stats()` - Tool: Stats

#### [`mcp_server/resources.py`](mcp_server/resources.py)
**Purpose:** MCP resource endpoints
**Key Functions:**
- `current_threads()` - Resource: Current state
- `latest_analysis()` - Resource: Analysis
- `active_alerts()` - Resource: Alerts

#### [`agents/remediation/remediation_agent.py`](agents/remediation/remediation_agent.py)
**Purpose:** Automated remediation with LangGraph
**Key Classes/Functions:**
- `RemediationAgent` class
- `create_remediation_graph()` - Build workflow
- `assess_issue()` - Assess problem
- `select_remediation()` - Choose action
- `execute_action()` - Execute fix
- `verify_resolution()` - Verify fix
- `rollback_if_needed()` - Rollback

#### [`agents/remediation/actions.py`](agents/remediation/actions.py)
**Purpose:** Remediation action implementations
**Key Functions:**
- `kill_thread()` - Kill thread
- `restart_service()` - Restart service
- `clear_connection_pool()` - Clear pool
- `increase_thread_pool()` - Increase pool
- `trigger_gc()` - Force GC
- `reset_cache()` - Reset cache

#### [`agents/remediation/safety_checks.py`](agents/remediation/safety_checks.py)
**Purpose:** Safety validations
**Key Functions:**
- `validate_action()` - Validate safety
- `check_dependencies()` - Check deps
- `can_rollback()` - Check rollback
- `log_action()` - Log action

---

## Dependencies File

### [`requirements.txt`](requirements.txt)
```
# Core dependencies
langgraph>=0.0.20
langchain>=0.1.0
langchain-openai>=0.0.5

# AI Models
openai>=1.0.0
anthropic>=0.8.0

# Web frameworks
streamlit>=1.28.0
dash>=2.14.0
plotly>=5.17.0

# API clients
requests>=2.31.0
slack-sdk>=3.23.0

# Scheduling
apscheduler>=3.10.4

# MCP
mcp>=0.1.0

# Utilities
python-dotenv>=1.0.0
pandas>=2.1.0
psutil>=5.9.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

---

## Environment Variables

### [`.env.example`](.env.example)
```bash
# webMethods Integration Server
WEBMETHODS_URL=http://localhost:5555
WEBMETHODS_USER=Administrator
WEBMETHODS_PASSWORD=manage

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#alerts

# AI Models
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MODEL_NAME=gpt-4

# Thresholds
HUNG_THREAD_THRESHOLD=300
CPU_THRESHOLD=80
MEMORY_THRESHOLD=85

# Monitoring
POLL_INTERVAL=30

# MCP Server
MCP_SERVER_PORT=8080
```

---

## Quick Commands

### Setup
```bash
# Clone and setup
git clone <repo-url>
cd thread_dump_analysis
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

### Run Individual Components
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

### Run All Components
```bash
# Use the start script
./scripts/start_all.sh
```

---

## Git Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/monitor` - Tapaswini's work
- `feature/collector-analyzer` - Ranadeep's work
- `feature/specialists` - Vinay's work
- `feature/dashboard` - Bhagwan's work
- `feature/mcp-remediation` - Sai's work

### Commit Messages
```
feat(monitor): Add hung thread detection
fix(analyzer): Correct deadlock detection logic
docs(readme): Update setup instructions
test(remediation): Add safety check tests
```

---

*This structure ensures clear separation of concerns and enables parallel development!*