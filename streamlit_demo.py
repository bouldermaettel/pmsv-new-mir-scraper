import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
import time
import random

# Configure page
st.set_page_config(
    page_title="PMSV Scraper Monitor - Demo",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .log-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        max-height: 400px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    .success-status {
        color: #28a745;
        font-weight: bold;
    }
    .warning-status {
        color: #ffc107;
        font-weight: bold;
    }
    .error-status {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class DemoLogger:
    def __init__(self):
        self.log_buffer = []
        self.max_logs = 100
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.log_buffer.append(log_entry)
        
        if len(self.log_buffer) > self.max_logs:
            self.log_buffer = self.log_buffer[-self.max_logs:]
    
    def get_logs(self):
        return "\n".join(self.log_buffer)

# Initialize session state
if 'logger' not in st.session_state:
    st.session_state.logger = DemoLogger()
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'last_check' not in st.session_state:
    st.session_state.last_check = None
if 'check_history' not in st.session_state:
    st.session_state.check_history = []
if 'demo_data' not in st.session_state:
    # Create demo historical data
    demo_data = []
    base_date = datetime.now() - timedelta(days=30)
    current_sb = 10573
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        # Simulate some SB number changes
        if i in [5, 12, 20, 25]:
            current_sb += 1
        demo_data.append({
            'sb_number': current_sb,
            'timestamp': date,
            'unix_timestamp': date.timestamp()
        })
    st.session_state.demo_data = demo_data

def generate_demo_scrape():
    """Simulate a scrape operation for demo purposes."""
    st.session_state.logger.log("Starting demo scrape operation...", "INFO")
    
    # Simulate network delay
    time.sleep(0.5)
    
    # Simulate finding a new SB number (occasionally)
    current_sb = 10573 + random.randint(0, 3)
    previous_sb = 10573 + random.randint(0, 2)
    
    if current_sb != previous_sb:
        st.session_state.logger.log(f"UPDATE DETECTED! Previous: {previous_sb}, Current: {current_sb}", "WARNING")
        status = 'updated'
    else:
        st.session_state.logger.log(f"No change detected. Current SB number: {current_sb}", "INFO")
        status = 'unchanged'
    
    # Update demo data
    new_entry = {
        'sb_number': current_sb,
        'timestamp': datetime.now(),
        'unix_timestamp': datetime.now().timestamp()
    }
    st.session_state.demo_data.append(new_entry)
    
    # Update check history
    check_result = {
        'timestamp': datetime.now(),
        'sb_number': current_sb,
        'previous_sb': previous_sb,
        'status': status
    }
    st.session_state.check_history.append(check_result)
    
    if len(st.session_state.check_history) > 50:
        st.session_state.check_history = st.session_state.check_history[-50:]
    
    st.session_state.last_check = datetime.now()
    return True, current_sb, previous_sb

def start_demo_monitoring():
    """Start continuous monitoring simulation."""
    st.session_state.monitoring = True
    st.session_state.logger.log("Starting demo monitoring...", "INFO")

def stop_demo_monitoring():
    """Stop continuous monitoring."""
    st.session_state.monitoring = False
    st.session_state.logger.log("Stopping demo monitoring...", "INFO")

# Main app layout
st.markdown('<h1 class="main-header">🔍 PMSV Scraper Monitor - Demo</h1>', unsafe_allow_html=True)

# Demo notice
st.warning("🎭 This is a **DEMO VERSION** showing the UI and functionality. It uses simulated data and doesn't perform actual web scraping.")

# Sidebar controls
with st.sidebar:
    st.header("🎛️ Controls")
    
    # Manual scrape button
    if st.button("🚀 Demo Scrape", type="primary", use_container_width=True):
        success, current, previous = generate_demo_scrape()
        if success:
            st.success("Demo scrape completed!")
        else:
            st.error("Demo scrape failed!")
    
    st.divider()
    
    # Monitoring controls
    st.subheader("📡 Monitoring")
    
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.monitoring:
            if st.button("▶️ Start Demo Monitoring", use_container_width=True):
                start_demo_monitoring()
    with col2:
        if st.session_state.monitoring:
            if st.button("⏹️ Stop Demo Monitoring", use_container_width=True):
                stop_demo_monitoring()
    
    # Monitoring status
    if st.session_state.monitoring:
        st.success("🟢 Demo Monitoring Active")
    else:
        st.info("⚪ Demo Monitoring Inactive")
    
    st.divider()
    
    # Settings
    st.subheader("⚙️ Settings")
    auto_refresh = st.checkbox("Auto-refresh dashboard", value=True)
    refresh_interval = st.slider("Refresh interval (seconds)", 5, 60, 30)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Current Status
    st.header("📊 Current Status")
    
    if st.session_state.demo_data:
        latest_data = st.session_state.demo_data[-1]
        
        # Status cards
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Current SB Number</h3>
                <h2>{latest_data['sb_number']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col1_2:
            last_update = latest_data['timestamp']
            time_diff = datetime.now() - last_update
            hours_ago = time_diff.total_seconds() / 3600
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>Last Updated</h3>
                <h2>{hours_ago:.1f}h ago</h2>
                <p>{last_update.strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col1_3:
            total_checks = len(st.session_state.check_history)
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Checks</h3>
                <h2>{total_checks}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Historical Chart
    st.header("📈 Historical Data")
    
    if st.session_state.demo_data:
        # Create DataFrame for plotting
        df = pd.DataFrame(st.session_state.demo_data)
        
        # Create timeline chart
        fig = px.line(
            df, 
            x='timestamp', 
            y='sb_number',
            title="SB Number Timeline (Demo Data)",
            labels={'sb_number': 'SB Number', 'timestamp': 'Date'},
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="SB Number",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("📋 Historical Records")
        display_data = df.copy()
        display_data['timestamp'] = display_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(display_data, use_container_width=True)
    else:
        st.info("No demo data available. Run a demo scrape to get started!")

with col2:
    # Live Activity Log
    st.header("📝 Live Activity Log")
    
    # Log display
    st.markdown(f"""
    <div class="log-container">
        {st.session_state.logger.get_logs()}
    </div>
    """, unsafe_allow_html=True)
    
    # Clear logs button
    if st.button("🗑️ Clear Logs", use_container_width=True):
        st.session_state.logger.log_buffer = []
        st.rerun()
    
    st.divider()
    
    # Recent Checks
    st.header("🕒 Recent Checks")
    
    if st.session_state.check_history:
        recent_checks = pd.DataFrame(st.session_state.check_history[-10:])
        recent_checks['timestamp'] = recent_checks['timestamp'].dt.strftime('%H:%M:%S')
        
        for _, check in recent_checks.iterrows():
            status_color = "success-status" if check['status'] == 'updated' else "warning-status"
            st.markdown(f"""
            <div class="status-card">
                <strong>{check['timestamp']}</strong><br>
                SB: {check['sb_number']}<br>
                <span class="{status_color}">{check['status'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent checks available")

# Auto-refresh functionality
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "🔍 **PMSV Scraper Monitor - Demo** - Real-time monitoring of EU medical device incident report forms | "
    "Built with Streamlit"
)

# Add some initial demo logs
if not st.session_state.logger.log_buffer:
    st.session_state.logger.log("Demo app initialized", "INFO")
    st.session_state.logger.log("Ready to simulate scraping operations", "INFO")
    st.session_state.logger.log("Click 'Demo Scrape' to see the interface in action", "INFO")
