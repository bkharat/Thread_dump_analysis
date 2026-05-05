"""
Utility functions for Thread Dump Analysis system
"""
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import re

try:
    from .config import config
    from .models import ThreadInfo, AlertMessage
except ImportError:
    # Fallback for direct execution
    from config import config
    from models import ThreadInfo, AlertMessage


def call_webmethods_api(
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict] = None,
    timeout: int = 30
) -> Dict[Any, Any]:
    """
    Make API call to webMethods Integration Server
    
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        data: Request data for POST/PUT
        timeout: Request timeout in seconds
    
    Returns:
        Response data as dictionary
    """
    url = f"{config.WEBMETHODS_URL}{endpoint}"
    auth = (config.WEBMETHODS_USER, config.WEBMETHODS_PASSWORD)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, auth=auth, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, auth=auth, json=data, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json() if response.content else {}
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling webMethods API: {e}")
        raise


def parse_thread_dump(raw_dump: str) -> List[ThreadInfo]:
    """
    Parse thread dump text into structured ThreadInfo objects
    
    Args:
        raw_dump: Raw thread dump text in JStack format
    
    Returns:
        List of ThreadInfo objects
    """
    threads = []
    current_thread = None
    stack_trace = []
    
    # Split by thread entries (lines starting with ")
    lines = raw_dump.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Thread header line
        if line.startswith('"') and 'prio=' in line:
            # Save previous thread if exists
            if current_thread:
                current_thread.stack_trace = stack_trace
                threads.append(current_thread)
                stack_trace = []
            
            # Parse thread info
            thread_name_match = re.search(r'"([^"]+)"', line)
            thread_id_match = re.search(r'#(\d+)', line)
            state_match = re.search(r'java.lang.Thread.State: (\w+)', line)
            
            if thread_name_match and thread_id_match:
                current_thread = ThreadInfo(
                    thread_id=thread_id_match.group(1),
                    name=thread_name_match.group(1),
                    state=state_match.group(1) if state_match else "UNKNOWN",
                    cpu_time=0.0,  # Will be populated from metrics
                    blocked_time=0.0,
                    timestamp=datetime.now()
                )
        
        # Stack trace lines
        elif line.startswith('at ') and current_thread:
            stack_trace.append(line)
        
        # Lock info
        elif 'locked' in line.lower() or 'waiting' in line.lower():
            if current_thread:
                if 'locked' in line.lower():
                    current_thread.lock_info = line
                elif 'waiting' in line.lower():
                    current_thread.waiting_on = line
    
    # Add last thread
    if current_thread:
        current_thread.stack_trace = stack_trace
        threads.append(current_thread)
    
    return threads


def format_slack_message(alert: AlertMessage) -> Dict:
    """
    Format alert message for Slack
    
    Args:
        alert: AlertMessage object
    
    Returns:
        Slack message payload
    """
    return {
        "text": alert.title,
        "blocks": alert.to_slack_blocks()
    }


def calculate_thread_metrics(threads: List[ThreadInfo]) -> Dict[str, Any]:
    """
    Calculate aggregate metrics from thread list
    
    Args:
        threads: List of ThreadInfo objects
    
    Returns:
        Dictionary of metrics
    """
    total_threads = len(threads)
    hung_threads = sum(1 for t in threads if t.is_hung(config.HUNG_THREAD_THRESHOLD))
    blocked_threads = sum(1 for t in threads if t.is_blocked())
    
    # Calculate state distribution
    state_distribution = {}
    for thread in threads:
        state_distribution[thread.state] = state_distribution.get(thread.state, 0) + 1
    
    # Find top CPU consuming threads
    sorted_threads = sorted(threads, key=lambda t: t.cpu_time, reverse=True)
    top_cpu_threads = [
        {"thread_id": t.thread_id, "name": t.name, "cpu_time": t.cpu_time}
        for t in sorted_threads[:5]
    ]
    
    return {
        "total_threads": total_threads,
        "hung_threads": hung_threads,
        "blocked_threads": blocked_threads,
        "state_distribution": state_distribution,
        "top_cpu_threads": top_cpu_threads,
        "timestamp": datetime.now().isoformat()
    }


def detect_deadlock(threads: List[ThreadInfo]) -> List[List[str]]:
    """
    Detect deadlocks in thread list
    
    Args:
        threads: List of ThreadInfo objects
    
    Returns:
        List of deadlock cycles (each cycle is a list of thread IDs)
    """
    deadlocks = []
    
    # Build wait-for graph
    wait_graph = {}
    for thread in threads:
        if thread.waiting_on and thread.lock_info:
            # Extract lock identifiers
            waiting_lock = re.search(r'<([^>]+)>', thread.waiting_on)
            held_lock = re.search(r'<([^>]+)>', thread.lock_info)
            
            if waiting_lock:
                wait_graph[thread.thread_id] = waiting_lock.group(1)
    
    # Detect cycles using DFS
    visited = set()
    rec_stack = set()
    
    def has_cycle(thread_id: str, path: List[str]) -> Optional[List[str]]:
        visited.add(thread_id)
        rec_stack.add(thread_id)
        path.append(thread_id)
        
        if thread_id in wait_graph:
            next_lock = wait_graph[thread_id]
            # Find thread holding this lock
            for t in threads:
                if t.lock_info and next_lock in t.lock_info:
                    if t.thread_id in rec_stack:
                        # Found cycle
                        cycle_start = path.index(t.thread_id)
                        return path[cycle_start:]
                    elif t.thread_id not in visited:
                        result = has_cycle(t.thread_id, path[:])
                        if result:
                            return result
        
        rec_stack.remove(thread_id)
        return None
    
    for thread in threads:
        if thread.thread_id not in visited:
            cycle = has_cycle(thread.thread_id, [])
            if cycle:
                deadlocks.append(cycle)
    
    return deadlocks


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted string (e.g., "5m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def sanitize_thread_name(name: str) -> str:
    """
    Sanitize thread name for safe display
    
    Args:
        name: Thread name
    
    Returns:
        Sanitized name
    """
    # Remove special characters, keep alphanumeric and common separators
    return re.sub(r'[^\w\s\-_.]', '', name)

# Made with Bob
