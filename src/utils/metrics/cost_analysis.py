"""
Cost Analysis CLI Tool

View and analyze cost tracking data from cost_log.csv

Usage:
    python -m src.utils.metrics.cost_analysis
    python -m src.utils.metrics.cost_analysis --session SESSION_ID
    python -m src.utils.metrics.cost_analysis --summary
"""

import argparse
import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

def load_cost_log(log_file: str = "logs/metrics/cost_log.csv") -> List[Dict]:
    """Load cost log from CSV"""
    if not Path(log_file).exists():
        print(f"❌ Cost log not found: {log_file}")
        return []
    
    rows = []
    with open(log_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            row['input_tokens'] = int(row['input_tokens'])
            row['output_tokens'] = int(row['output_tokens'])
            row['total_tokens'] = int(row['total_tokens'])
            row['input_cost'] = float(row['input_cost'])
            row['output_cost'] = float(row['output_cost'])
            row['total_cost'] = float(row['total_cost'])
            row['latency_ms'] = float(row['latency_ms'])
            rows.append(row)
    
    return rows

def analyze_by_session(rows: List[Dict]) -> Dict:
    """Analyze costs grouped by session"""
    sessions = defaultdict(lambda: {
        "calls": 0,
        "tokens": 0,
        "cost": 0.0,
        "agents": defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0}),
        "models": defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0})
    })
    
    for row in rows:
        session_id = row['session_id']
        agent = row['agent_name']
        model = row['model']
        
        sessions[session_id]["calls"] += 1
        sessions[session_id]["tokens"] += row['total_tokens']
        sessions[session_id]["cost"] += row['total_cost']
        
        sessions[session_id]["agents"][agent]["calls"] += 1
        sessions[session_id]["agents"][agent]["tokens"] += row['total_tokens']
        sessions[session_id]["agents"][agent]["cost"] += row['total_cost']
        
        sessions[session_id]["models"][model]["calls"] += 1
        sessions[session_id]["models"][model]["tokens"] += row['total_tokens']
        sessions[session_id]["models"][model]["cost"] += row['total_cost']
    
    return dict(sessions)

def analyze_by_agent(rows: List[Dict]) -> Dict:
    """Analyze costs grouped by agent"""
    agents = defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0})
    
    for row in rows:
        agent = row['agent_name']
        agents[agent]["calls"] += 1
        agents[agent]["tokens"] += row['total_tokens']
        agents[agent]["cost"] += row['total_cost']
    
    return dict(agents)

def analyze_by_model(rows: List[Dict]) -> Dict:
    """Analyze costs grouped by model"""
    models = defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0})
    
    for row in rows:
        model = row['model']
        models[model]["calls"] += 1
        models[model]["tokens"] += row['total_tokens']
        models[model]["cost"] += row['total_cost']
    
    return dict(models)

def print_summary(rows: List[Dict]):
    """Print overall cost summary"""
    if not rows:
        print("No cost data available.")
        return
    
    total_calls = len(rows)
    total_tokens = sum(r['total_tokens'] for r in rows)
    total_cost = sum(r['total_cost'] for r in rows)
    
    sessions = analyze_by_session(rows)
    agents = analyze_by_agent(rows)
    models = analyze_by_model(rows)
    
    print("\n" + "="*60)
    print("📊 COST TRACKING SUMMARY")
    print("="*60)
    
    print(f"\n📈 Overall Statistics:")
    print(f"  Total Sessions:  {len(sessions)}")
    print(f"  Total LLM Calls: {total_calls:,}")
    print(f"  Total Tokens:    {total_tokens:,}")
    print(f"  Total Cost:      ${total_cost:.4f}")
    
    print(f"\n🤖 By Agent:")
    for agent, stats in sorted(agents.items(), key=lambda x: x[1]['cost'], reverse=True):
        print(f"  {agent:20} | Calls: {stats['calls']:3} | Tokens: {stats['tokens']:7,} | Cost: ${stats['cost']:.4f}")
    
    print(f"\n🔧 By Model:")
    for model, stats in sorted(models.items(), key=lambda x: x[1]['cost'], reverse=True):
        print(f"  {model:30} | Calls: {stats['calls']:3} | Tokens: {stats['tokens']:7,} | Cost: ${stats['cost']:.4f}")
    
    print("\n" + "="*60 + "\n")

def print_session_detail(rows: List[Dict], session_id: str):
    """Print detailed breakdown for a specific session"""
    session_rows = [r for r in rows if r['session_id'] == session_id]
    
    if not session_rows:
        print(f"❌ No data found for session: {session_id}")
        return
    
    total_cost = sum(r['total_cost'] for r in session_rows)
    total_tokens = sum(r['total_tokens'] for r in session_rows)
    
    agents = defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0})
    for row in session_rows:
        agent = row['agent_name']
        agents[agent]["calls"] += 1
        agents[agent]["tokens"] += row['total_tokens']
        agents[agent]["cost"] += row['total_cost']
    
    print("\n" + "="*60)
    print(f"📋 SESSION DETAIL: {session_id}")
    print("="*60)
    
    print(f"\n📊 Session Statistics:")
    print(f"  Total LLM Calls: {len(session_rows)}")
    print(f"  Total Tokens:    {total_tokens:,}")
    print(f"  Total Cost:      ${total_cost:.4f}")
    
    print(f"\n🤖 By Agent:")
    for agent, stats in sorted(agents.items(), key=lambda x: x[1]['cost'], reverse=True):
        print(f"  {agent:20} | Calls: {stats['calls']:3} | Tokens: {stats['tokens']:7,} | Cost: ${stats['cost']:.4f}")
    
    print(f"\n📝 Call History:")
    for i, row in enumerate(session_rows, 1):
        print(f"  [{i:2}] {row['timestamp'][:19]} | {row['agent_name']:15} | "
              f"{row['model']:25} | "
              f"Tokens: {row['input_tokens']:4}+{row['output_tokens']:4} | "
              f"Cost: ${row['total_cost']:.6f}")
    
    print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Cost Tracking Analysis Tool")
    parser.add_argument('--log-file', default='logs/metrics/cost_log.csv', help='Path to cost log CSV file')
    parser.add_argument('--session', help='Show detailed breakdown for specific session ID')
    parser.add_argument('--summary', action='store_true', help='Show overall summary (default)')
    parser.add_argument('--list-sessions', action='store_true', help='List all session IDs')
    
    args = parser.parse_args()
    
    rows = load_cost_log(args.log_file)
    
    if not rows:
        return
    
    if args.list_sessions:
        sessions = set(r['session_id'] for r in rows)
        print("\n📁 Available Sessions:")
        for session_id in sorted(sessions):
            session_rows = [r for r in rows if r['session_id'] == session_id]
            cost = sum(r['total_cost'] for r in session_rows)
            calls = len(session_rows)
            print(f"  {session_id} ({calls} calls, ${cost:.4f})")
        print()
    elif args.session:
        print_session_detail(rows, args.session)
    else:
        print_summary(rows)

if __name__ == "__main__":
    main()
