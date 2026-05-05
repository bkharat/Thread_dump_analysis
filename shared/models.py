"""
Data models for Thread Dump Analysis system
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ThreadState(Enum):
    """Thread states"""
    RUNNABLE = "RUNNABLE"
    BLOCKED = "BLOCKED"
    WAITING = "WAITING"
    TIMED_WAITING = "TIMED_WAITING"
    NEW = "NEW"
    TERMINATED = "TERMINATED"


class Severity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class IssueType(Enum):
    """Types of issues detected"""
    DEADLOCK = "deadlock"
    HUNG_THREAD = "hung"
    CPU_INTENSIVE = "cpu_intensive"
    MEMORY_LEAK = "memory_leak"
    BLOCKED = "blocked"
    RESOURCE_CONTENTION = "resource_contention"


@dataclass
class ThreadInfo:
    """Information about a single thread"""
    thread_id: str
    name: str
    state: str
    cpu_time: float  # in seconds
    blocked_time: float  # in seconds
    stack_trace: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    lock_info: Optional[str] = None
    waiting_on: Optional[str] = None
    
    def is_hung(self, threshold: int = 300) -> bool:
        """Check if thread is hung based on CPU time threshold"""
        return self.cpu_time > threshold
    
    def is_blocked(self) -> bool:
        """Check if thread is blocked"""
        return self.state == ThreadState.BLOCKED.value


@dataclass
class ThreadDumpData:
    """Complete thread dump data"""
    server_url: str
    timestamp: datetime
    threads: List[ThreadInfo]
    total_threads: int
    hung_threads: int
    blocked_threads: int
    deadlocks: List[str] = field(default_factory=list)
    
    @property
    def has_issues(self) -> bool:
        """Check if dump has any issues"""
        return self.hung_threads > 0 or self.blocked_threads > 0 or len(self.deadlocks) > 0


@dataclass
class AlertMessage:
    """Alert message structure"""
    severity: str  # critical, warning, info
    title: str
    description: str
    thread_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_slack_blocks(self) -> List[Dict]:
        """Convert to Slack block format"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{'🚨' if self.severity == 'critical' else '⚠️'} {self.title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": self.description
                }
            }
        ]
        
        if self.thread_id:
            blocks.append({
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Thread ID:*\n{self.thread_id}"},
                    {"type": "mrkdwn", "text": f"*Time:*\n{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"}
                ]
            })
        
        if self.actions:
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": action},
                        "value": f"{action.lower()}_{self.thread_id}"
                    }
                    for action in self.actions
                ]
            })
        
        return blocks


@dataclass
class AnalysisResult:
    """Result of thread dump analysis"""
    thread_id: str
    issue_type: str  # deadlock, hung, cpu_intensive, memory_leak
    root_cause: str
    recommendations: List[str]
    confidence: float  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    affected_threads: List[str] = field(default_factory=list)
    stack_trace_summary: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "thread_id": self.thread_id,
            "issue_type": self.issue_type,
            "root_cause": self.root_cause,
            "recommendations": self.recommendations,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "affected_threads": self.affected_threads,
            "stack_trace_summary": self.stack_trace_summary
        }


@dataclass
class GCMetrics:
    """Garbage Collection metrics"""
    avg_pause_time: float  # milliseconds
    max_pause_time: float  # milliseconds
    full_gc_count: int
    young_gc_count: int
    heap_usage_percent: float
    old_gen_usage_percent: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def has_issues(self) -> bool:
        """Check if GC has issues"""
        return (
            self.max_pause_time > 1000 or  # > 1 second
            self.full_gc_count > 10 or
            self.heap_usage_percent > 85
        )


@dataclass
class CPUMetrics:
    """CPU usage metrics"""
    overall_cpu_percent: float
    thread_cpu_usage: Dict[str, float]  # thread_id -> cpu_percent
    top_cpu_threads: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def has_issues(self, threshold: float = 80.0) -> bool:
        """Check if CPU usage is high"""
        return self.overall_cpu_percent > threshold


@dataclass
class RemediationAction:
    """Remediation action details"""
    action_type: str  # kill_thread, restart_service, clear_pool, etc.
    target: str  # thread_id or service_name
    parameters: Dict[str, Any] = field(default_factory=dict)
    executed: bool = False
    success: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    error_message: Optional[str] = None
    rollback_available: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "action_type": self.action_type,
            "target": self.target,
            "parameters": self.parameters,
            "executed": self.executed,
            "success": self.success,
            "timestamp": self.timestamp.isoformat(),
            "error_message": self.error_message,
            "rollback_available": self.rollback_available
        }

# Made with Bob
