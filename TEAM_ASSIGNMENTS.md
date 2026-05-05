# Team Member Assignments - Quick Reference

## 🔴 Tapaswini: Monitor Agent & Slack Notifications

### Time: 10-25 minutes (15 min total)

### Deliverables:
1. **Monitor Agent** ([`agents/monitor/monitor_agent.py`](agents/monitor/monitor_agent.py))
   - Poll webMethods Integration Server every 30 seconds
   - Detect hung threads (running > 5 minutes)
   - Identify blocked threads and deadlocks

2. **Slack Integration** ([`agents/monitor/slack_notifier.py`](agents/monitor/slack_notifier.py))
   - Send formatted alerts with thread details
   - Include action buttons: "Analyze" and "Remediate"
   - Implement alert deduplication

### Key Code Structure:
```python
class MonitorAgent:
    def __init__(self, server_url, slack_webhook):
        self.server_url = server_url
        self.slack_webhook = slack_webhook
        self.alert_cache = {}
    
    def monitor_integration_server(self):
        # Poll server statistics
        pass
    
    def detect_hung_threads(self, threads, threshold=300):
        # Identify problematic threads
        pass
    
    def send_slack_alert(self, thread_info):
        # Send notification to Slack
        pass
```

### Dependencies:
- `requests` - API calls to webMethods
- `slack-sdk` - Slack notifications
- `apscheduler` - Periodic monitoring

---

## 🟢 Ranadeep: Thread Dump Collection & Analysis

### Time: 10-30 minutes (20 min total)

### Deliverables:
1. **Collector Agent** ([`agents/collector/collector_agent.py`](agents/collector/collector_agent.py))
   - LangGraph workflow for thread dump collection
   - Connect to webMethods API
   - Parse JStack format thread dumps

2. **Analyzer Agent** ([`agents/analyzer/analyzer_agent.py`](agents/analyzer/analyzer_agent.py))
   - LangGraph workflow for AI analysis
   - Use LLM to identify patterns and issues
   - Generate recommendations

### LangGraph Workflow:
```python
from langgraph.graph import StateGraph

# Collector Workflow
collector_graph = StateGraph()
collector_graph.add_node("connect", connect_to_server)
collector_graph.add_node("collect", collect_thread_dump)
collector_graph.add_node("parse", parse_threads)
collector_graph.add_node("store", store_data)

# Analyzer Workflow
analyzer_graph = StateGraph()
analyzer_graph.add_node("load", load_thread_dump)
analyzer_graph.add_node("analyze", analyze_patterns)
analyzer_graph.add_node("detect", detect_issues)
analyzer_graph.add_node("report", generate_report)
```

### Dependencies:
- `langgraph` - Agent orchestration
- `langchain` - LLM integration
- `openai` or `anthropic` - AI models

---

## 🔵 Vinay: GC & CPU Specialist Agents

### Time: 10-30 minutes (20 min total)

### Deliverables:
1. **GC Specialist Agent** ([`agents/gc_specialist/gc_agent.py`](agents/gc_specialist/gc_agent.py))
   - Analyze GC logs from webMethods
   - Identify memory leaks and excessive pauses
   - Recommend JVM tuning parameters

2. **CPU Specialist Agent** ([`agents/cpu_specialist/cpu_agent.py`](agents/cpu_specialist/cpu_agent.py))
   - Correlate CPU spikes with thread activity
   - Identify CPU-intensive threads
   - Suggest optimization strategies

### LangGraph Workflows:
```python
# GC Specialist
gc_graph = StateGraph()
gc_graph.add_node("collect_gc", collect_gc_logs)
gc_graph.add_node("analyze_gc", analyze_gc_patterns)
gc_graph.add_node("detect_memory", detect_memory_issues)
gc_graph.add_node("recommend", recommend_tuning)

# CPU Specialist
cpu_graph = StateGraph()
cpu_graph.add_node("collect_cpu", collect_cpu_metrics)
cpu_graph.add_node("correlate", correlate_with_threads)
cpu_graph.add_node("identify", identify_hotspots)
cpu_graph.add_node("optimize", suggest_optimizations)
```

### Analysis Focus:
- **GC:** Pause times, heap usage, old gen growth, Full GC frequency
- **CPU:** Thread CPU usage, hotspots, blocking operations

### Dependencies:
- `langgraph` - Agent orchestration
- `langchain` - LLM integration
- `psutil` - System metrics

---

## 🟡 Bhagwan: Monitoring Dashboard

### Time: 10-40 minutes (30 min total)

### Deliverables:
1. **Dashboard Application** ([`dashboard/app.py`](dashboard/app.py))
   - Real-time monitoring interface
   - Multiple visualization panels
   - Alert management

### Dashboard Sections:
1. **Overview Panel**
   - Server health status
   - Active thread count
   - Current alerts

2. **Thread Analysis Panel**
   - Thread list with status
   - Stack trace viewer
   - Thread timeline

3. **Performance Metrics Panel**
   - CPU usage graph
   - Memory usage graph
   - GC statistics

4. **AI Insights Panel**
   - Analysis results
   - Recommendations
   - Specialist insights

5. **Alert History Panel**
   - Past alerts table
   - Resolution status
   - Time to resolution

### Technology Choice:
**Option 1: Streamlit** (Recommended for speed)
```python
import streamlit as st

st.title("webMethods Thread Dump Analysis")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Threads", thread_count)
with col2:
    st.metric("Hung Threads", hung_count)
with col3:
    st.metric("CPU Usage", cpu_percent)
```

**Option 2: Dash** (More customizable)
```python
import dash
from dash import dcc, html

app = dash.Dash(__name__)
app.layout = html.Div([...])
```

### Dependencies:
- `streamlit` or `dash` - Dashboard framework
- `plotly` - Interactive charts
- `pandas` - Data manipulation

---

## 🟣 Sai: MCP Server & Remediation Agent

### Time: 10-35 minutes (25 min total)

### Deliverables:
1. **MCP Server** ([`mcp_server/server.py`](mcp_server/server.py))
   - Expose tools for thread operations
   - Provide resource endpoints
   - Handle concurrent requests

2. **Remediation Agent** ([`agents/remediation/remediation_agent.py`](agents/remediation/remediation_agent.py))
   - LangGraph workflow for automated fixes
   - Safe execution with rollback
   - Action logging

### MCP Server Structure:
```python
from mcp.server import Server
from mcp.types import Tool, Resource

server = Server("thread-dump-analysis")

@server.tool()
async def get_thread_dump(server_url: str) -> dict:
    """Collect thread dump from webMethods server"""
    pass

@server.tool()
async def analyze_thread(thread_id: str) -> dict:
    """Analyze specific thread"""
    pass

@server.tool()
async def execute_remediation(action: str, thread_id: str) -> dict:
    """Execute remediation action"""
    pass

@server.resource("thread://current")
async def current_threads() -> str:
    """Get current thread state"""
    pass
```

### Remediation Workflow:
```python
remediation_graph = StateGraph()
remediation_graph.add_node("assess", assess_issue)
remediation_graph.add_node("select", select_remediation)
remediation_graph.add_node("execute", execute_action)
remediation_graph.add_node("verify", verify_resolution)
remediation_graph.add_node("rollback", rollback_if_needed)
```

### Remediation Actions:
- Kill hung thread
- Restart service
- Clear connection pool
- Increase thread pool size
- Trigger garbage collection
- Reset cache

### Dependencies:
- `mcp` - Model Context Protocol
- `langgraph` - Agent orchestration
- `requests` - webMethods API calls

---

## Shared Components (All Team Members - First 10 min)

### 1. Configuration File ([`shared/config.py`](shared/config.py))
```python
import os

class Config:
    # webMethods Integration Server
    WEBMETHODS_URL = os.getenv("WEBMETHODS_URL", "http://localhost:5555")
    WEBMETHODS_USER = os.getenv("WEBMETHODS_USER", "Administrator")
    WEBMETHODS_PASSWORD = os.getenv("WEBMETHODS_PASSWORD")
    
    # Slack
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#alerts")
    
    # AI Models
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
    
    # Thresholds
    HUNG_THREAD_THRESHOLD = 300  # 5 minutes
    CPU_THRESHOLD = 80  # 80%
    MEMORY_THRESHOLD = 85  # 85%
    
    # Monitoring
    POLL_INTERVAL = 30  # seconds
```

### 2. Data Models ([`shared/models.py`](shared/models.py))
```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class ThreadInfo:
    thread_id: str
    name: str
    state: str
    cpu_time: float
    blocked_time: float
    stack_trace: List[str]
    timestamp: datetime

@dataclass
class ThreadDumpData:
    server_url: str
    timestamp: datetime
    threads: List[ThreadInfo]
    total_threads: int
    hung_threads: int

@dataclass
class AlertMessage:
    severity: str  # critical, warning, info
    title: str
    description: str
    thread_id: Optional[str]
    timestamp: datetime
    actions: List[str]

@dataclass
class AnalysisResult:
    thread_id: str
    issue_type: str  # deadlock, hung, cpu_intensive, memory_leak
    root_cause: str
    recommendations: List[str]
    confidence: float
    timestamp: datetime
```

### 3. Utility Functions ([`shared/utils.py`](shared/utils.py))
```python
import requests
from typing import Dict, Any

def call_webmethods_api(endpoint: str, method: str = "GET", 
                        data: Dict = None) -> Dict[Any, Any]:
    """Make API call to webMethods Integration Server"""
    pass

def parse_thread_dump(raw_dump: str) -> List[ThreadInfo]:
    """Parse thread dump text into structured data"""
    pass

def format_slack_message(alert: AlertMessage) -> Dict:
    """Format alert for Slack"""
    pass

def calculate_thread_metrics(threads: List[ThreadInfo]) -> Dict:
    """Calculate aggregate metrics"""
    pass
```

---

## Integration Points

### Data Flow:
1. **Monitor Agent** → Detects issue → Triggers **Collector Agent**
2. **Collector Agent** → Gathers dump → Sends to **Analyzer Agent**
3. **Analyzer Agent** → Analyzes → Invokes **Specialist Agents** (GC/CPU)
4. **Specialist Agents** → Generate insights → Send to **Remediation Agent**
5. **Remediation Agent** → Executes fix → Updates **Dashboard**
6. **All Agents** → Log events → Update **Dashboard** → Notify **Slack**

### Communication:
- Use shared message queue (Redis) or direct function calls
- All agents expose async interfaces
- Dashboard polls for updates every 5 seconds

---

## Quick Start Commands

### Setup (All team members):
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install langgraph langchain openai slack-sdk streamlit requests apscheduler mcp

# Set environment variables
export WEBMETHODS_URL="http://your-server:5555"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export OPENAI_API_KEY="your-api-key"
```

### Run Components:
```bash
# Terminal 1: MCP Server (Sai)
python mcp_server/server.py

# Terminal 2: Monitor Agent (Tapaswini)
python agents/monitor/monitor_agent.py

# Terminal 3: Dashboard (Bhagwan)
streamlit run dashboard/app.py
```

---

## Testing Checklist

- [ ] Monitor detects simulated hung thread
- [ ] Slack notification received
- [ ] Thread dump collected successfully
- [ ] Analysis identifies root cause
- [ ] GC specialist provides insights
- [ ] CPU specialist provides insights
- [ ] Remediation action executes safely
- [ ] Dashboard shows real-time updates
- [ ] MCP server responds to tool calls
- [ ] End-to-end flow completes in < 2 minutes

---

## Emergency Contacts

**Blockers?** Post in Slack immediately!

**Need Help?**
- Tapaswini ↔ Sai (Monitor + Remediation integration)
- Ranadeep ↔ Vinay (Analysis + Specialists integration)
- Bhagwan ↔ All (Dashboard data sources)

---

*Let's make this happen! 🚀*