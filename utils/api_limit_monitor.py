"""
API Limit Monitor for GUARDIAN
Tracks OpenAI and Anthropic API usage and provides alerts when limits are reached
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Optional
import streamlit as st

class APILimitMonitor:
    def __init__(self, db_path="api_usage.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize API usage tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                endpoint TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tokens_used INTEGER DEFAULT 0,
                cost_estimate REAL DEFAULT 0.0,
                status TEXT,
                error_message TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_limits (
                provider TEXT PRIMARY KEY,
                daily_limit INTEGER,
                monthly_limit INTEGER,
                current_daily_usage INTEGER DEFAULT 0,
                current_monthly_usage INTEGER DEFAULT 0,
                last_reset_date TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Initialize default limits
        cursor.execute('''
            INSERT OR IGNORE INTO api_limits (provider, daily_limit, monthly_limit, last_reset_date)
            VALUES 
                ('openai', 10000, 200000, ?),
                ('anthropic', 5000, 100000, ?)
        ''', (datetime.now().date().isoformat(), datetime.now().date().isoformat()))
        
        conn.commit()
        conn.close()
    
    def log_api_call(self, provider: str, endpoint: str = "", tokens_used: int = 0, 
                     cost_estimate: float = 0.0, status: str = "success", error_message: str = ""):
        """Log an API call"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_usage (provider, endpoint, tokens_used, cost_estimate, status, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (provider, endpoint, tokens_used, cost_estimate, status, error_message))
        
        # Update daily usage
        today = datetime.now().date().isoformat()
        cursor.execute('''
            UPDATE api_limits 
            SET current_daily_usage = current_daily_usage + ?,
                current_monthly_usage = current_monthly_usage + ?
            WHERE provider = ?
        ''', (tokens_used, tokens_used, provider))
        
        conn.commit()
        conn.close()
    
    def check_limits(self, provider: str) -> Dict[str, any]:
        """Check current usage against limits"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT daily_limit, monthly_limit, current_daily_usage, current_monthly_usage, status
            FROM api_limits WHERE provider = ?
        ''', (provider,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {"status": "unknown", "daily_percent": 0, "monthly_percent": 0}
        
        daily_limit, monthly_limit, daily_usage, monthly_usage, status = result
        
        daily_percent = (daily_usage / daily_limit * 100) if daily_limit > 0 else 0
        monthly_percent = (monthly_usage / monthly_limit * 100) if monthly_limit > 0 else 0
        
        return {
            "status": status,
            "daily_usage": daily_usage,
            "daily_limit": daily_limit,
            "daily_percent": daily_percent,
            "monthly_usage": monthly_usage,
            "monthly_limit": monthly_limit,
            "monthly_percent": monthly_percent,
            "at_risk": daily_percent > 80 or monthly_percent > 80,
            "exceeded": daily_percent >= 100 or monthly_percent >= 100
        }
    
    def get_usage_summary(self) -> Dict[str, Dict]:
        """Get usage summary for all providers"""
        providers = ['openai', 'anthropic']
        summary = {}
        
        for provider in providers:
            summary[provider] = self.check_limits(provider)
        
        return summary
    
    def reset_daily_usage(self):
        """Reset daily usage counters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        cursor.execute('''
            UPDATE api_limits 
            SET current_daily_usage = 0, last_reset_date = ?
        ''', (today,))
        
        conn.commit()
        conn.close()
    
    def display_usage_alerts(self):
        """Display usage alerts in Streamlit interface"""
        summary = self.get_usage_summary()
        
        for provider, usage in summary.items():
            if usage.get("exceeded"):
                st.error(f"🚨 {provider.upper()} API LIMIT EXCEEDED")
                st.error(f"Daily: {usage['daily_usage']}/{usage['daily_limit']} ({usage['daily_percent']:.1f}%)")
                st.error(f"Monthly: {usage['monthly_usage']}/{usage['monthly_limit']} ({usage['monthly_percent']:.1f}%)")
                st.error("Scoring may be impacted. Consider using alternative providers or waiting for reset.")
                
            elif usage.get("at_risk"):
                st.warning(f"⚠️ {provider.upper()} API Usage High")
                st.warning(f"Daily: {usage['daily_usage']}/{usage['daily_limit']} ({usage['daily_percent']:.1f}%)")
                st.warning(f"Monthly: {usage['monthly_usage']}/{usage['monthly_limit']} ({usage['monthly_percent']:.1f}%)")
                st.warning("Approaching limits. System will automatically use alternative providers.")

def monitor_openai_call(func):
    """Decorator to monitor OpenAI API calls"""
    def wrapper(*args, **kwargs):
        monitor = APILimitMonitor()
        try:
            result = func(*args, **kwargs)
            monitor.log_api_call("openai", "chat", 1000, 0.002, "success")
            return result
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                monitor.log_api_call("openai", "chat", 0, 0, "quota_exceeded", error_msg)
            else:
                monitor.log_api_call("openai", "chat", 0, 0, "error", error_msg)
            raise e
    return wrapper

def monitor_anthropic_call(func):
    """Decorator to monitor Anthropic API calls"""
    def wrapper(*args, **kwargs):
        monitor = APILimitMonitor()
        try:
            result = func(*args, **kwargs)
            monitor.log_api_call("anthropic", "messages", 1000, 0.003, "success")
            return result
        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "quota" in error_msg.lower():
                monitor.log_api_call("anthropic", "messages", 0, 0, "quota_exceeded", error_msg)
            else:
                monitor.log_api_call("anthropic", "messages", 0, 0, "error", error_msg)
            raise e
    return wrapper

def get_api_status_indicator() -> str:
    """Get color-coded API status for UI display"""
    monitor = APILimitMonitor()
    summary = monitor.get_usage_summary()
    
    status_colors = []
    
    for provider, usage in summary.items():
        if usage.get("exceeded"):
            status_colors.append("🔴")
        elif usage.get("at_risk"):
            status_colors.append("🟡")
        else:
            status_colors.append("🟢")
    
    return " ".join(status_colors) + f" API Status"

def display_api_dashboard():
    """Display comprehensive API usage dashboard"""
    monitor = APILimitMonitor()
    summary = monitor.get_usage_summary()
    
    st.subheader("🔧 API Usage Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "OpenAI Usage",
            f"{summary['openai']['daily_percent']:.1f}%",
            f"Daily: {summary['openai']['daily_usage']}/{summary['openai']['daily_limit']}"
        )
    
    with col2:
        st.metric(
            "Anthropic Usage", 
            f"{summary['anthropic']['daily_percent']:.1f}%",
            f"Daily: {summary['anthropic']['daily_usage']}/{summary['anthropic']['daily_limit']}"
        )
    
    # Show alerts
    monitor.display_usage_alerts()
    
    # Usage recommendations
    if any(usage.get("at_risk") for usage in summary.values()):
        st.info("💡 **Optimization Tips:**")
        st.info("• Smart caching is active to reduce API calls")
        st.info("• System automatically uses free providers (Groq, Ollama) when available")
        st.info("• Enhanced pattern scoring provides fallback analysis")