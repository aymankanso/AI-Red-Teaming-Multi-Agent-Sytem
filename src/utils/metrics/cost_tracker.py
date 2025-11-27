"""
Cost Tracking System for LLM Usage

Tracks token usage and calculates costs per model, per agent, and per session.
Logs to CSV and provides real-time metrics.
"""

import csv
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class LLMCallMetrics:
    """Metrics for a single LLM call"""
    timestamp: str
    session_id: str
    agent_name: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float
    latency_ms: float

# Model pricing (cost per 1M tokens in USD)
MODEL_PRICING = {
    "gpt-4o-mini": {
        "input": 0.150,   # $0.15 per 1M input tokens
        "output": 0.600   # $0.60 per 1M output tokens
    },
    "gpt-4o": {
        "input": 5.00,
        "output": 15.00
    },
    "gpt-4": {
        "input": 30.00,
        "output": 60.00
    },
    "claude-3-5-sonnet-20241022": {
        "input": 3.00,
        "output": 15.00
    },
    "claude-3-opus-20240229": {
        "input": 15.00,
        "output": 75.00
    },
    "claude-3-haiku-20240307": {
        "input": 0.25,
        "output": 1.25
    }
}

class CostTracker:
    """Tracks LLM usage and costs"""
    
    def __init__(self, log_dir: str = "logs/metrics"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.csv_file = self.log_dir / "cost_log.csv"
        self.session_file = self.log_dir / "session_costs.json"
        
        # In-memory session tracking
        self.session_costs: Dict[str, Dict] = {}
        
        # Load existing session costs if available
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    self.session_costs = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load session costs: {e}")
                self.session_costs = {}
        
        # Initialize CSV if doesn't exist
        if not self.csv_file.exists():
            self._init_csv()
        
        logger.info(f"CostTracker initialized. Logging to {self.csv_file}")
    
    def _init_csv(self):
        """Initialize CSV file with headers"""
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'session_id',
                'agent_name',
                'model',
                'provider',
                'input_tokens',
                'output_tokens',
                'total_tokens',
                'input_cost',
                'output_cost',
                'total_cost',
                'latency_ms'
            ])
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> Dict[str, float]:
        """Calculate cost for a given model and token usage"""
        
        # Get pricing for model (default to gpt-4o-mini if unknown)
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4o-mini"])
        
        # Calculate costs (pricing is per 1M tokens)
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        return {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6)
        }
    
    def track_call(
        self,
        session_id: str,
        agent_name: str,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float = 0.0
    ) -> LLMCallMetrics:
        """
        Track a single LLM call
        
        Args:
            session_id: Unique session identifier
            agent_name: Name of agent making the call (Planner, Reconnaissance, etc.)
            model: Model name (gpt-4o-mini, claude-3-5-sonnet, etc.)
            provider: Provider name (openai, anthropic)
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            latency_ms: Call latency in milliseconds
        
        Returns:
            LLMCallMetrics with calculated costs
        """
        
        # Calculate costs
        costs = self.calculate_cost(model, input_tokens, output_tokens)
        
        # Create metrics object
        metrics = LLMCallMetrics(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            agent_name=agent_name,
            model=model,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            input_cost=costs["input_cost"],
            output_cost=costs["output_cost"],
            total_cost=costs["total_cost"],
            latency_ms=latency_ms
        )
        
        # Log to CSV
        self._log_to_csv(metrics)
        
        # Update session tracking
        self._update_session(metrics)
        
        logger.debug(f"Tracked LLM call: {agent_name} | {model} | "
                    f"Tokens: {input_tokens}+{output_tokens} | "
                    f"Cost: ${costs['total_cost']:.6f}")
        
        return metrics
    
    def _log_to_csv(self, metrics: LLMCallMetrics):
        """Append metrics to CSV log"""
        try:
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    metrics.timestamp,
                    metrics.session_id,
                    metrics.agent_name,
                    metrics.model,
                    metrics.provider,
                    metrics.input_tokens,
                    metrics.output_tokens,
                    metrics.total_tokens,
                    metrics.input_cost,
                    metrics.output_cost,
                    metrics.total_cost,
                    metrics.latency_ms
                ])
        except Exception as e:
            logger.error(f"Failed to log to CSV: {e}")
    
    def _update_session(self, metrics: LLMCallMetrics):
        """Update in-memory session tracking"""
        session_id = metrics.session_id
        
        if session_id not in self.session_costs:
            self.session_costs[session_id] = {
                "session_id": session_id,
                "start_time": metrics.timestamp,
                "last_update": metrics.timestamp,
                "total_calls": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "agents": {},
                "models": {}
            }
        
        session = self.session_costs[session_id]
        session["last_update"] = metrics.timestamp
        session["total_calls"] += 1
        session["total_tokens"] += metrics.total_tokens
        session["total_cost"] += metrics.total_cost
        
        # Track by agent
        agent = metrics.agent_name
        if agent not in session["agents"]:
            session["agents"][agent] = {
                "calls": 0,
                "tokens": 0,
                "cost": 0.0
            }
        session["agents"][agent]["calls"] += 1
        session["agents"][agent]["tokens"] += metrics.total_tokens
        session["agents"][agent]["cost"] += metrics.total_cost
        
        # Track by model
        model = metrics.model
        if model not in session["models"]:
            session["models"][model] = {
                "calls": 0,
                "tokens": 0,
                "cost": 0.0
            }
        session["models"][model]["calls"] += 1
        session["models"][model]["tokens"] += metrics.total_tokens
        session["models"][model]["cost"] += metrics.total_cost
        
        # Persist to disk
        self._save_session_costs()
    
    def _save_session_costs(self):
        """Save session costs to JSON file"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session_costs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save session costs: {e}")
    
    def get_session_cost(self, session_id: str) -> Optional[Dict]:
        """Get cost summary for a specific session"""
        return self.session_costs.get(session_id)
    
    def get_all_sessions(self) -> Dict[str, Dict]:
        """Get all session cost summaries"""
        return self.session_costs
    
    def get_total_cost(self) -> float:
        """Get total cost across all sessions"""
        return sum(s["total_cost"] for s in self.session_costs.values())
    
    def generate_summary(self) -> Dict:
        """Generate overall cost summary"""
        total_calls = sum(s["total_calls"] for s in self.session_costs.values())
        total_tokens = sum(s["total_tokens"] for s in self.session_costs.values())
        total_cost = self.get_total_cost()
        
        # Aggregate by agent across all sessions
        agent_totals = {}
        for session in self.session_costs.values():
            for agent, stats in session["agents"].items():
                if agent not in agent_totals:
                    agent_totals[agent] = {"calls": 0, "tokens": 0, "cost": 0.0}
                agent_totals[agent]["calls"] += stats["calls"]
                agent_totals[agent]["tokens"] += stats["tokens"]
                agent_totals[agent]["cost"] += stats["cost"]
        
        # Aggregate by model
        model_totals = {}
        for session in self.session_costs.values():
            for model, stats in session["models"].items():
                if model not in model_totals:
                    model_totals[model] = {"calls": 0, "tokens": 0, "cost": 0.0}
                model_totals[model]["calls"] += stats["calls"]
                model_totals[model]["tokens"] += stats["tokens"]
                model_totals[model]["cost"] += stats["cost"]
        
        return {
            "total_sessions": len(self.session_costs),
            "total_calls": total_calls,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 6),
            "by_agent": agent_totals,
            "by_model": model_totals
        }


# Global instance
_cost_tracker: Optional[CostTracker] = None

def get_cost_tracker() -> CostTracker:
    """Get or create global cost tracker instance"""
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker
