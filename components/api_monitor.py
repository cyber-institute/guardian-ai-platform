"""
API Monitoring Component for GUARDIAN
Provides real-time API usage alerts and status indicators
"""

import streamlit as st
from utils.api_limit_monitor import APILimitMonitor

def render_api_status_widget():
    """Render compact API status widget for sidebar or header"""
    try:
        monitor = APILimitMonitor()
        summary = monitor.get_usage_summary()
        
        # Check for any issues
        has_alerts = False
        alert_messages = []
        
        for provider, usage in summary.items():
            if usage.get("exceeded"):
                has_alerts = True
                alert_messages.append(f"{provider.upper()} API limit exceeded")
            elif usage.get("at_risk"):
                has_alerts = True
                alert_messages.append(f"{provider.upper()} usage: {usage['daily_percent']:.0f}%")
        
        if has_alerts:
            with st.container():
                st.warning("API Usage Alerts")
                for message in alert_messages:
                    st.caption(f"• {message}")
                st.caption("System using cached results and fallback scoring")
        else:
            st.success("API services operational")
            
    except Exception:
        # Fail silently if monitoring unavailable
        pass

def render_detailed_api_dashboard():
    """Render detailed API usage dashboard"""
    try:
        monitor = APILimitMonitor()
        summary = monitor.get_usage_summary()
        
        st.subheader("API Usage Monitor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            openai_data = summary.get('openai', {})
            daily_pct = openai_data.get('daily_percent', 0)
            
            if daily_pct >= 100:
                st.metric("OpenAI Status", "EXCEEDED", f"{daily_pct:.0f}%", delta_color="inverse")
            elif daily_pct >= 80:
                st.metric("OpenAI Status", "HIGH", f"{daily_pct:.0f}%", delta_color="inverse") 
            else:
                st.metric("OpenAI Status", "NORMAL", f"{daily_pct:.0f}%", delta_color="normal")
        
        with col2:
            anthropic_data = summary.get('anthropic', {})
            daily_pct = anthropic_data.get('daily_percent', 0)
            
            if daily_pct >= 100:
                st.metric("Anthropic Status", "EXCEEDED", f"{daily_pct:.0f}%", delta_color="inverse")
            elif daily_pct >= 80:
                st.metric("Anthropic Status", "HIGH", f"{daily_pct:.0f}%", delta_color="inverse")
            else:
                st.metric("Anthropic Status", "NORMAL", f"{daily_pct:.0f}%", delta_color="normal")
        
        # Show mitigation info if needed
        if any(data.get('at_risk', False) for data in summary.values()):
            st.info("Smart caching and alternative providers active to minimize API usage")
            
    except Exception:
        st.error("API monitoring unavailable")

def check_api_health() -> dict:
    """Check overall API health status"""
    try:
        monitor = APILimitMonitor()
        summary = monitor.get_usage_summary()
        
        status = "healthy"
        message = "All API services operational"
        
        for provider, usage in summary.items():
            if usage.get("exceeded"):
                status = "critical"
                message = f"{provider.upper()} API limit exceeded"
                break
            elif usage.get("at_risk"):
                status = "warning" 
                message = f"{provider.upper()} usage high"
                
        return {"status": status, "message": message, "details": summary}
        
    except Exception:
        return {"status": "unknown", "message": "Monitoring unavailable", "details": {}}