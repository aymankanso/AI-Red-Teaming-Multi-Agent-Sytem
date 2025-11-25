"""
Observability module for tracing and monitoring
"""

from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class TraceEventType(Enum):
    """Types of trace events"""
    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    AGENT_RESPONSE = "agent_response"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    ERROR = "error"


class TraceLogger:
    """Trace logger for workflow execution"""
    
    def __init__(self):
        self.traces = []
        self.current_workflow = None
        self.current_trace_id = None
        
    def log_event(self, event_type: TraceEventType, data: Dict[str, Any]):
        """Log a trace event"""
        event = {
            "type": event_type.value,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.traces.append(event)
        logger.debug(f"Trace event: {event_type.value}")
        
    def start_workflow(self, workflow_name: str, user_input: str) -> str:
        """Log workflow start and return trace ID"""
        trace_id = str(uuid.uuid4())
        self.current_trace_id = trace_id
        self.current_workflow = workflow_name
        
        self.log_event(TraceEventType.WORKFLOW_START, {
            "trace_id": trace_id,
            "workflow_name": workflow_name,
            "user_input": user_input
        })
        
        return trace_id
        
    def end_workflow(self, status: str = "completed", error: Optional[str] = None) -> Dict[str, Any]:
        """Log workflow end and return trace summary"""
        trace_data = {
            "trace_id": self.current_trace_id,
            "workflow_name": self.current_workflow,
            "status": status
        }
        
        if error:
            trace_data["error"] = error
            
        self.log_event(TraceEventType.WORKFLOW_END, trace_data)
        
        result = {
            "trace_id": self.current_trace_id,
            "status": status,
            "num_events": len(self.traces)
        }
        
        self.current_workflow = None
        return result
        
    def log_agent_response(self, agent_name: str, response: str, metadata: Optional[Dict[str, Any]] = None):
        """Log agent response"""
        self.log_event(TraceEventType.AGENT_RESPONSE, {
            "agent_name": agent_name,
            "response": response[:200] if len(response) > 200 else response,  # Truncate long responses
            "metadata": metadata or {}
        })
        
    def log_agent_activity(self, agent_name: str, activity: str):
        """Log agent activity"""
        self.log_event(TraceEventType.AGENT_START, {
            "agent_name": agent_name,
            "activity": activity
        })
        
    def log_tool_execution(self, tool_name: str, args: Dict[str, Any]):
        """Log tool execution"""
        self.log_event(TraceEventType.TOOL_START, {
            "tool_name": tool_name,
            "args": args
        })
        
    def log_error(self, error_message: str, exception: Optional[Exception] = None, context: Dict[str, Any] = None):
        """Log error"""
        error_data = {
            "error": error_message,
            "context": context or {}
        }
        
        if exception:
            error_data["exception_type"] = type(exception).__name__
            
        self.log_event(TraceEventType.ERROR, error_data)
        
    def get_traces(self):
        """Get all traces"""
        return self.traces
        
    def clear_traces(self):
        """Clear all traces"""
        self.traces = []
        self.current_workflow = None
        self.current_trace_id = None


# Global instance
_trace_logger: Optional[TraceLogger] = None


def get_trace_logger() -> TraceLogger:
    """Get or create the global trace logger instance"""
    global _trace_logger
    if _trace_logger is None:
        _trace_logger = TraceLogger()
    return _trace_logger


__all__ = ['TraceLogger', 'TraceEventType', 'get_trace_logger']
