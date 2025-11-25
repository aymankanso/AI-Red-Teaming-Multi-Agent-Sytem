"""
Metrics tracking module for cost and performance monitoring
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class LLMCall:
    """Single LLM call record"""
    model: str
    input_tokens: int
    output_tokens: int
    timestamp: float
    cost: float = 0.0


@dataclass
class TaskMetrics:
    """Metrics for a task"""
    task_id: str
    start_time: float
    end_time: Optional[float] = None
    llm_calls: List[LLMCall] = field(default_factory=list)
    
    @property
    def total_input_tokens(self) -> int:
        return sum(call.input_tokens for call in self.llm_calls)
    
    @property
    def total_output_tokens(self) -> int:
        return sum(call.output_tokens for call in self.llm_calls)
    
    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens
    
    @property
    def total_cost(self) -> float:
        return sum(call.cost for call in self.llm_calls)
    
    @property
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time


class CostTracker:
    """Cost tracker for LLM API calls"""
    
    # Simple pricing (USD per 1M tokens)
    PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
        "default": {"input": 0.15, "output": 0.60}
    }
    
    def __init__(self):
        self.tasks: Dict[str, TaskMetrics] = {}
        self.current_task_id: Optional[str] = None
        
    def start_task(self, task_id: str):
        """Start tracking a new task"""
        self.tasks[task_id] = TaskMetrics(
            task_id=task_id,
            start_time=time.time()
        )
        self.current_task_id = task_id
        return task_id
        
    def log_llm_call(self, model: str, input_tokens: int, output_tokens: int):
        """Log an LLM API call"""
        if not self.current_task_id or self.current_task_id not in self.tasks:
            return
            
        # Calculate cost
        pricing = self.PRICING.get(model.lower(), self.PRICING["default"])
        cost = (
            (input_tokens / 1_000_000) * pricing["input"] +
            (output_tokens / 1_000_000) * pricing["output"]
        )
        
        call = LLMCall(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            timestamp=time.time(),
            cost=cost
        )
        
        self.tasks[self.current_task_id].llm_calls.append(call)
        
    def end_task(self, task_id: str) -> TaskMetrics:
        """End task tracking and return metrics"""
        if task_id in self.tasks:
            self.tasks[task_id].end_time = time.time()
            if self.current_task_id == task_id:
                self.current_task_id = None
            return self.tasks[task_id]
        
        # Return empty metrics if task not found
        return TaskMetrics(task_id=task_id, start_time=time.time(), end_time=time.time())
        
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        total_input = sum(t.total_input_tokens for t in self.tasks.values())
        total_output = sum(t.total_output_tokens for t in self.tasks.values())
        total_cost = sum(t.total_cost for t in self.tasks.values())
        
        return {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output,
            "total_cost": total_cost,
            "num_tasks": len(self.tasks),
            "num_calls": sum(len(t.llm_calls) for t in self.tasks.values())
        }
        
    def reset(self):
        """Reset all tracking"""
        self.tasks = {}
        self.current_task_id = None


# Global instance
_cost_tracker: Optional[CostTracker] = None


def get_cost_tracker() -> CostTracker:
    """Get or create the global cost tracker instance"""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker


def reset_cost_tracker():
    """Reset the global cost tracker"""
    global _cost_tracker
    _cost_tracker = CostTracker()


__all__ = ['CostTracker', 'get_cost_tracker', 'reset_cost_tracker']
