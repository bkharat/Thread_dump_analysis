# Quick Start Guide - 1 Hour Sprint

## 🚀 Getting Started (First 5 Minutes)

### 1. Clone and Setup
```bash
# Navigate to project directory
cd c:/Bobathon/Thread_dump_analysis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat

# Install dependencies
pip install langgraph langchain langchain-openai openai anthropic streamlit dash plotly requests slack-sdk apscheduler mcp python-dotenv pandas psutil pytest pytest-asyncio
```

### 2. Configure Environment
Create `.env` file in project root:
```bash
# webMethods Integration Server
WEBMETHODS_URL=http://localhost:5555
WEBMETHODS_USER=Administrator
WEBMETHODS_PASSWORD=your_password

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#alerts

# AI Models (use one)
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

MODEL_NAME=gpt-4

# Thresholds
HUNG_THREAD_THRESHOLD=300
CPU_THRESHOLD=80
MEMORY_THRESHOLD=85
POLL_INTERVAL=30

# MCP Server
MCP_SERVER_PORT=8080
```

### 3. Create Project Structure
```bash
# Create all directories
mkdir -p shared agents/monitor agents/collector agents/analyzer agents/gc_specialist agents/cpu_specialist agents/remediation mcp_server dashboard/components dashboard/utils dashboard/assets tests logs data/thread_dumps data/analysis_results data/alerts scripts
```

---

## 👥 Team Member Instructions

### 🔴 Tapaswini: Monitor Agent (Minutes 0-25)

#### Step 1: Create Shared Files (0-10 min)
Work with team to create:
- [`shared/config.py`](shared/config.py)
- [`shared/models.py`](shared/models.py)
- [`shared/utils.py`](shared/utils.py)

#### Step 2: Build Monitor Agent (10-20 min)
Create [`agents/monitor/monitor_agent.py`](agents/monitor/monitor_agent.py):

```python
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from shared.config import Config
from shared.models import ThreadInfo, AlertMessage
from slack_sdk.webhook import WebhookClient

class MonitorAgent:
    def __init__(self):
        self.config = Config()
        self.slack = WebhookClient(self.config.SLACK_WEBHOOK_URL)
        self.alert_cache = {}
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start monitoring"""
        self.scheduler.add_job(
            self.monitor_integration_server,
            'interval',
            seconds=self.config.POLL_INTERVAL
        )
        self.scheduler.start()
        print("Monitor agent started")
    
    def monitor_integration_server(self):
        """Poll webMethods server for thread statistics"""
        try:
            # Get thread statistics from webMethods
            response = requests.get(
                f"{self.config.WEBMETHODS_URL}/invoke/wm.server/getThreadPoolStats",
                auth=(self.config.WEBMETHODS_USER, self.config.WEBMETHODS_PASSWORD),
                timeout=10
            )
            
            if response.status_code == 200:
                threads = self._parse_threads(response.json())
                hung_threads = self.detect_hung_threads(threads)
                
                for thread in hung_threads:
                    self.send_slack_alert(thread)
        
        except Exception as e:
            print(f"Error monitoring server: {e}")
    
    def detect_hung_threads(self, threads, threshold=None):
        """Identify hung threads"""
        if threshold is None:
            threshold = self.config.HUNG_THREAD_THRESHOLD
        
        hung_threads = []
        for thread in threads:
            if thread.cpu_time > threshold:
                hung_threads.append(thread)
        
        return hung_threads
    
    def send_slack_alert(self, thread_info):
        """Send alert to Slack"""
        # Deduplicate alerts
        cache_key = f"{thread_info.thread_id}_{thread_info.state}"
        if cache_key in self.alert_cache:
            return
        
        self.alert_cache[cache_key] = time.time()
        
        # Format message
        message = {
            "text": f"🚨 Hung Thread Detected",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚨 Hung Thread Alert"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Thread ID:*\n{thread_info.thread_id}"},
                        {"type": "mrkdwn", "text": f"*Name:*\n{thread_info.name}"},
                        {"type": "mrkdwn", "text": f"*State:*\n{thread_info.state}"},
                        {"type": "mrkdwn", "text": f"*CPU Time:*\n{thread_info.cpu_time}s"}
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Analyze"},
                            "style": "primary",
                            "value": f"analyze_{thread_info.thread_id}"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Remediate"},
                            "style": "danger",
                            "value": f"remediate_{thread_info.thread_id}"
                        }
                    ]
                }
            ]
        }
        
        self.slack.send(text=message["text"], blocks=message["blocks"])
        print(f"Alert sent for thread {thread_info.thread_id}")
    
    def _parse_threads(self, data):
        """Parse thread data from API response"""
        # Implementation depends on webMethods API format
        threads = []
        # Parse and create ThreadInfo objects
        return threads

if __name__ == "__main__":
    agent = MonitorAgent()
    agent.start()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitor agent stopped")
```

#### Step 3: Test (20-25 min)
```bash
python agents/monitor/monitor_agent.py
```

---

### 🟢 Ranadeep: Collector & Analyzer (Minutes 0-30)

#### Step 1: Collector Agent (0-15 min)
Create [`agents/collector/collector_agent.py`](agents/collector/collector_agent.py):

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import requests
from shared.config import Config
from shared.models import ThreadDumpData, ThreadInfo

class CollectorState(TypedDict):
    server_url: str
    thread_dump: str
    parsed_threads: List[ThreadInfo]
    error: str

class CollectorAgent:
    def __init__(self):
        self.config = Config()
        self.graph = self._create_graph()
    
    def _create_graph(self):
        """Create LangGraph workflow"""
        workflow = StateGraph(CollectorState)
        
        workflow.add_node("connect", self.connect_to_server)
        workflow.add_node("collect", self.collect_thread_dump)
        workflow.add_node("parse", self.parse_threads)
        workflow.add_node("store", self.store_data)
        
        workflow.set_entry_point("connect")
        workflow.add_edge("connect", "collect")
        workflow.add_edge("collect", "parse")
        workflow.add_edge("parse", "store")
        workflow.add_edge("store", END)
        
        return workflow.compile()
    
    def connect_to_server(self, state: CollectorState):
        """Connect to webMethods server"""
        print(f"Connecting to {state['server_url']}")
        # Verify connection
        return state
    
    def collect_thread_dump(self, state: CollectorState):
        """Collect thread dump from server"""
        try:
            response = requests.get(
                f"{self.config.WEBMETHODS_URL}/invoke/wm.server/getThreadDump",
                auth=(self.config.WEBMETHODS_USER, self.config.WEBMETHODS_PASSWORD),
                timeout=30
            )
            state["thread_dump"] = response.text
            print("Thread dump collected")
        except Exception as e:
            state["error"] = str(e)
        return state
    
    def parse_threads(self, state: CollectorState):
        """Parse thread dump into structured data"""
        # Parse JStack format
        threads = []
        # Parsing logic here
        state["parsed_threads"] = threads
        print(f"Parsed {len(threads)} threads")
        return state
    
    def store_data(self, state: CollectorState):
        """Store thread dump data"""
        # Save to file or database
        print("Thread dump stored")
        return state
    
    def run(self, server_url: str):
        """Execute collection workflow"""
        initial_state = {
            "server_url": server_url,
            "thread_dump": "",
            "parsed_threads": [],
            "error": ""
        }
        result = self.graph.invoke(initial_state)
        return result

if __name__ == "__main__":
    agent = CollectorAgent()
    result = agent.run(Config().WEBMETHODS_URL)
    print(f"Collection complete: {len(result['parsed_threads'])} threads")
```

#### Step 2: Analyzer Agent (15-30 min)
Create [`agents/analyzer/analyzer_agent.py`](agents/analyzer/analyzer_agent.py):

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from shared.config import Config
from shared.models import AnalysisResult

class AnalyzerState(TypedDict):
    thread_dump: str
    patterns: List[str]
    issues: List[str]
    recommendations: List[str]
    analysis_result: AnalysisResult

class AnalyzerAgent:
    def __init__(self):
        self.config = Config()
        self.llm = ChatOpenAI(model=self.config.MODEL_NAME, temperature=0)
        self.graph = self._create_graph()
    
    def _create_graph(self):
        """Create LangGraph workflow"""
        workflow = StateGraph(AnalyzerState)
        
        workflow.add_node("load", self.load_thread_dump)
        workflow.add_node("analyze", self.analyze_patterns)
        workflow.add_node("detect", self.detect_issues)
        workflow.add_node("report", self.generate_report)
        
        workflow.set_entry_point("load")
        workflow.add_edge("load", "analyze")
        workflow.add_edge("analyze", "detect")
        workflow.add_edge("detect", "report")
        workflow.add_edge("report", END)
        
        return workflow.compile()
    
    def load_thread_dump(self, state: AnalyzerState):
        """Load thread dump data"""
        print("Loading thread dump")
        return state
    
    def analyze_patterns(self, state: AnalyzerState):
        """Analyze thread patterns using LLM"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in analyzing Java thread dumps. Identify patterns, bottlenecks, and issues."),
            ("user", "Analyze this thread dump:\n\n{thread_dump}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"thread_dump": state["thread_dump"]})
        
        state["patterns"] = [response.content]
        print("Patterns analyzed")
        return state
    
    def detect_issues(self, state: AnalyzerState):
        """Detect specific issues"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Identify deadlocks, hung threads, resource contention, and blocking operations."),
            ("user", "Thread dump analysis:\n\n{patterns}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"patterns": "\n".join(state["patterns"])})
        
        state["issues"] = [response.content]
        print("Issues detected")
        return state
    
    def generate_report(self, state: AnalyzerState):
        """Generate analysis report with recommendations"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Generate actionable recommendations to resolve the identified issues."),
            ("user", "Issues found:\n\n{issues}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"issues": "\n".join(state["issues"])})
        
        state["recommendations"] = [response.content]
        print("Report generated")
        return state
    
    def run(self, thread_dump: str):
        """Execute analysis workflow"""
        initial_state = {
            "thread_dump": thread_dump,
            "patterns": [],
            "issues": [],
            "recommendations": [],
            "analysis_result": None
        }
        result = self.graph.invoke(initial_state)
        return result

if __name__ == "__main__":
    agent = AnalyzerAgent()
    # Test with sample thread dump
    result = agent.run("Sample thread dump...")
    print("Analysis complete")
```

---

### 🔵 Vinay: GC & CPU Specialists (Minutes 0-30)

#### Step 1: GC Specialist (0-15 min)
Create [`agents/gc_specialist/gc_agent.py`](agents/gc_specialist/gc_agent.py):

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from langchain_openai import ChatOpenAI
from shared.config import Config

class GCState(TypedDict):
    gc_logs: str
    gc_metrics: Dict
    memory_issues: List[str]
    tuning_recommendations: List[str]

class GCSpecialistAgent:
    def __init__(self):
        self.config = Config()
        self.llm = ChatOpenAI(model=self.config.MODEL_NAME, temperature=0)
        self.graph = self._create_graph()
    
    def _create_graph(self):
        workflow = StateGraph(GCState)
        
        workflow.add_node("collect_gc", self.collect_gc_logs)
        workflow.add_node("analyze_gc", self.analyze_gc_patterns)
        workflow.add_node("detect_memory", self.detect_memory_issues)
        workflow.add_node("recommend", self.recommend_tuning)
        
        workflow.set_entry_point("collect_gc")
        workflow.add_edge("collect_gc", "analyze_gc")
        workflow.add_edge("analyze_gc", "detect_memory")
        workflow.add_edge("detect_memory", "recommend")
        workflow.add_edge("recommend", END)
        
        return workflow.compile()
    
    def collect_gc_logs(self, state: GCState):
        """Collect GC logs from webMethods"""
        # Collect GC logs
        print("Collecting GC logs")
        return state
    
    def analyze_gc_patterns(self, state: GCState):
        """Analyze GC patterns"""
        # Calculate metrics: pause times, heap usage, etc.
        state["gc_metrics"] = {
            "avg_pause_time": 0,
            "max_pause_time": 0,
            "full_gc_count": 0,
            "heap_usage": 0
        }
        print("GC patterns analyzed")
        return state
    
    def detect_memory_issues(self, state: GCState):
        """Detect memory leaks and issues"""
        issues = []
        if state["gc_metrics"]["full_gc_count"] > 10:
            issues.append("Excessive Full GC events detected")
        state["memory_issues"] = issues
        print(f"Detected {len(issues)} memory issues")
        return state
    
    def recommend_tuning(self, state: GCState):
        """Recommend JVM tuning parameters"""
        recommendations = [
            "Increase heap size: -Xmx4g",
            "Use G1GC: -XX:+UseG1GC",
            "Set max GC pause: -XX:MaxGCPauseMillis=200"
        ]
        state["tuning_recommendations"] = recommendations
        print("Tuning recommendations generated")
        return state
    
    def run(self, gc_logs: str):
        initial_state = {
            "gc_logs": gc_logs,
            "gc_metrics": {},
            "memory_issues": [],
            "tuning_recommendations": []
        }
        return self.graph.invoke(initial_state)
```

#### Step 2: CPU Specialist (15-30 min)
Create [`agents/cpu_specialist/cpu_agent.py`](agents/cpu_specialist/cpu_agent.py) - Similar structure to GC agent

---

### 🟡 Bhagwan: Dashboard (Minutes 0-40)

#### Create Streamlit Dashboard (0-40 min)
Create [`dashboard/app.py`](dashboard/app.py):

```python
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="Thread Dump Analysis", layout="wide")

st.title("🔍 webMethods Thread Dump Analysis Dashboard")

# Overview Section
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active Threads", "45", "+3")
with col2:
    st.metric("Hung Threads", "2", "+1", delta_color="inverse")
with col3:
    st.metric("CPU Usage", "75%", "+5%")
with col4:
    st.metric("Memory Usage", "82%", "+2%")

# Thread Analysis Section
st.header("Thread Analysis")
thread_data = pd.DataFrame({
    'Thread ID': ['Thread-1', 'Thread-2', 'Thread-3'],
    'Name': ['HTTP-Worker', 'DB-Connection', 'Cache-Manager'],
    'State': ['RUNNABLE', 'BLOCKED', 'WAITING'],
    'CPU Time': [350, 120, 45],
    'Status': ['🔴 Hung', '🟡 Blocked', '🟢 Normal']
})
st.dataframe(thread_data, use_container_width=True)

# Performance Metrics
st.header("Performance Metrics")
col1, col2 = st.columns(2)

with col1:
    # CPU Chart
    fig_cpu = go.Figure()
    fig_cpu.add_trace(go.Scatter(
        x=list(range(10)),
        y=[65, 70, 68, 75, 80, 78, 82, 79, 75, 77],
        mode='lines+markers',
        name='CPU %'
    ))
    fig_cpu.update_layout(title="CPU Usage Over Time", height=300)
    st.plotly_chart(fig_cpu, use_container_width=True)

with col2:
    # Memory Chart
    fig_mem = go.Figure()
    fig_mem.add_trace(go.Scatter(
        x=list(range(10)),
        y=[70, 72, 75, 78, 80, 82, 81, 83, 82, 84],
        mode='lines+markers',
        name='Memory %'
    ))
    fig_mem.update_layout(title="Memory Usage Over Time", height=300)
    st.plotly_chart(fig_mem, use_container_width=True)

# AI Insights
st.header("AI Insights")
st.info("🤖 Analysis: Detected 2 hung threads in HTTP worker pool. Recommendation: Increase thread pool size and investigate database query performance.")

# Alert History
st.header("Alert History")
alert_data = pd.DataFrame({
    'Time': ['12:30:45', '12:25:12', '12:20:33'],
    'Severity': ['🔴 Critical', '🟡 Warning', '🟢 Info'],
    'Message': ['Hung thread detected', 'High CPU usage', 'GC pause time increased'],
    'Status': ['Active', 'Resolved', 'Resolved']
})
st.dataframe(alert_data, use_container_width=True)

# Auto-refresh
if st.button("🔄 Refresh"):
    st.rerun()
```

Run with: `streamlit run dashboard/app.py`

---

### 🟣 Sai: MCP & Remediation (Minutes 0-35)

#### Step 1: MCP Server (0-15 min)
Create [`mcp_server/server.py`](mcp_server/server.py):

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio

server = Server("thread-dump-analysis")

@server.tool()
async def get_thread_dump(server_url: str) -> str:
    """Collect thread dump from webMethods server"""
    # Implementation
    return "Thread dump collected"

@server.tool()
async def analyze_thread(thread_id: str) -> str:
    """Analyze specific thread"""
    # Implementation
    return f"Analysis for {thread_id}"

@server.tool()
async def execute_remediation(action: str, thread_id: str) -> str:
    """Execute remediation action"""
    # Implementation
    return f"Executed {action} on {thread_id}"

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Step 2: Remediation Agent (15-35 min)
Create [`agents/remediation/remediation_agent.py`](agents/remediation/remediation_agent.py) - Similar LangGraph structure

---

## 🧪 Testing (Minutes 40-55)

### Integration Test Script
Create [`tests/test_integration.py`](tests/test_integration.py):

```python
import pytest
from agents.monitor.monitor_agent import MonitorAgent
from agents.collector.collector_agent import CollectorAgent
from agents.analyzer.analyzer_agent import AnalyzerAgent

def test_end_to_end():
    """Test complete workflow"""
    # 1. Monitor detects issue
    monitor = MonitorAgent()
    
    # 2. Collector gathers dump
    collector = CollectorAgent()
    
    # 3. Analyzer processes
    analyzer = AnalyzerAgent()
    
    # 4. Verify results
    assert True  # Add real assertions

if __name__ == "__main__":
    test_end_to_end()
    print("✅ Integration test passed")
```

Run: `python tests/test_integration.py`

---

## 📋 Final Checklist (Minutes 55-60)

- [ ] All agents running without errors
- [ ] Slack notifications working
- [ ] Dashboard displaying data
- [ ] MCP server responding
- [ ] End-to-end flow tested
- [ ] Documentation complete

---

## 🆘 Troubleshooting

### Common Issues:

**Import Errors:**
```bash
pip install --upgrade langgraph langchain langchain-openai
```

**Slack Webhook Not Working:**
- Verify webhook URL in `.env`
- Test with: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Test"}' YOUR_WEBHOOK_URL`

**webMethods Connection Failed:**
- Check server URL and credentials
- Verify server is running
- Test with: `curl -u user:pass http://server:5555/invoke/wm.server/ping`

**LangGraph Errors:**
- Ensure all state types match
- Check node connections
- Verify END node is reachable

---

*Good luck with your 1-hour sprint! 🚀*