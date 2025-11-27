"""
Cost Display Component

Shows real-time cost metrics in the Streamlit UI
"""

import streamlit as st
from typing import Dict, Optional

def display_session_cost(session_metrics: Optional[Dict]):
    """
    Display cost metrics for current session
    
    Args:
        session_metrics: Session cost data from CostTracker
    """
    if not session_metrics:
        return
    
    st.markdown("---")
    st.markdown("### 💰 Session Costs")
    
    total_cost = session_metrics.get("total_cost", 0)
    total_tokens = session_metrics.get("total_tokens", 0)
    total_calls = session_metrics.get("total_calls", 0)
    
    # Main metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Cost", f"${total_cost:.4f}")
    with col2:
        st.metric("Tokens", f"{total_tokens:,}")
    
    st.metric("LLM Calls", total_calls)
    
    # By agent breakdown
    agents = session_metrics.get("agents", {})
    if agents:
        st.markdown("**By Agent:**")
        for agent, stats in agents.items():
            st.markdown(f"**{agent}**")
            st.caption(f"Calls: {stats['calls']} | Tokens: {stats['tokens']:,} | Cost: ${stats['cost']:.4f}")


def display_cost_summary(summary: Dict):
    """
    Display overall cost summary across all sessions
    
    Args:
        summary: Cost summary from CostTracker.generate_summary()
    """
    st.markdown("---")
    st.markdown("### 📊 Overall Statistics")
    
    st.metric("Total Sessions", summary.get("total_sessions", 0))
    st.metric("Total Cost", f"${summary.get('total_cost', 0):.4f}")
    st.metric("Total Tokens", f"{summary.get('total_tokens', 0):,}")
    
    # By model breakdown
    models = summary.get("by_model", {})
    if models:
        st.markdown("**By Model:**")
        for model, stats in models.items():
            st.markdown(f"**{model}**")
            st.caption(f"Calls: {stats['calls']} | Tokens: {stats['tokens']:,} | Cost: ${stats['cost']:.4f}")


def show_cost_warning(cost: float, threshold: float = 0.10):
    """
    Show warning if session cost exceeds threshold
    
    Args:
        cost: Current session cost
        threshold: Warning threshold in USD
    """
    if cost > threshold:
        st.warning(
            f"⚠️ Session cost (${cost:.4f}) exceeds ${threshold:.2f} threshold!"
        )
