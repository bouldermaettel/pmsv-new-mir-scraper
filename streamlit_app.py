import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import time
import threading
from scraper import PMSVScraper
import logging
from io import StringIO
import sys

# Configure page
st.set_page_config(
    page_title="PMSV Scraper Monitor",
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

class StreamlitLogger:
    def __init__(self):
        self.log_buffer = []
        self.max_logs = 100
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.log_buffer.append(log_entry)
        
        # Keep only the last max_logs entries
        if len(self.log_buffer) > self.max_logs:
            self.log_buffer = self.log_buffer[-self.max_logs:]
    
    def get_logs(self):
        return "\n".join(self.log_buffer)

# Initialize session state
if 'logger' not in st.session_state:
    st.session_state.logger = StreamlitLogger()
if 'scraper' not in st.session_state:
    st.session_state.scraper = PMSVScraper()
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'last_check' not in st.session_state:
    st.session_state.last_check = None
if 'check_history' not in st.session_state:
    st.session_state.check_history = []

def load_historical_data():
    """Load historical data from the JSON file and create a DataFrame."""
    try:
        if os.path.exists('sb_number_data.json'):
            with open('sb_number_data.json', 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Single entry format
                    return pd.DataFrame([{
                        'sb_number': data.get('sb_number'),
                        'timestamp': pd.to_datetime(data.get('last_updated')),
                        'unix_timestamp': data.get('timestamp')
                    }])
                else:
                    # Multiple entries format
                    return pd.DataFrame(data)
    except Exception as e:
        st.session_state.logger.log(f"Error loading historical data: {e}", "ERROR")
    return pd.DataFrame()

def perform_scrape():
    """Perform a single scrape operation with detailed logging."""
    st.session_state.logger.log("Starting manual scrape operation...", "INFO")
    
    try:
        # Scrape the webpage
        st.session_state.logger.log("Fetching webpage content...", "INFO")
        current_sb = st.session_state.scraper.scrape_webpage()
        
        if current_sb:
            st.session_state.logger.log(f"Successfully extracted SB number: {current_sb}", "SUCCESS")
            
            # Load previous data
            previous_sb = st.session_state.scraper.load_previous_sb_number()
            
            if previous_sb:
                if current_sb != previous_sb:
                    st.session_state.logger.log(f"UPDATE DETECTED! Previous: {previous_sb}, Current: {current_sb}", "WARNING")
                    st.session_state.scraper.save_sb_number(current_sb)
                    st.session_state.logger.log("New SB number saved to database", "INFO")
                else:
                    st.session_state.logger.log(f"No change detected. Current SB number: {current_sb}", "INFO")
            else:
                st.session_state.logger.log(f"First run - saving initial SB number: {current_sb}", "INFO")
                st.session_state.scraper.save_sb_number(current_sb)
            
            # Update check history
            check_result = {
                'timestamp': datetime.now(),
                'sb_number': current_sb,
                'previous_sb': previous_sb,
                'status': 'updated' if previous_sb and current_sb != previous_sb else 'unchanged'
            }
            st.session_state.check_history.append(check_result)
            
            # Keep only last 50 entries
            if len(st.session_state.check_history) > 50:
                st.session_state.check_history = st.session_state.check_history[-50:]
            
            st.session_state.last_check = datetime.now()
            return True, current_sb, previous_sb
        else:
            st.session_state.logger.log("Failed to extract SB number from webpage", "ERROR")
            return False, None, None
            
    except Exception as e:
        st.session_state.logger.log(f"Error during scraping: {str(e)}", "ERROR")
        return False, None, None

def start_monitoring():
    """Start continuous monitoring in a separate thread."""
    st.session_state.monitoring = True
    st.session_state.logger.log("Starting continuous monitoring...", "INFO")
    
    def monitor_loop():
        while st.session_state.monitoring:
            perform_scrape()
            time.sleep(300)  # Check every 5 minutes
    
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()

def stop_monitoring():
    """Stop continuous monitoring."""
    st.session_state.monitoring = False
    st.session_state.logger.log("Stopping continuous monitoring...", "INFO")

# Main app layout
st.markdown('<h1 class="main-header">🔍 PMSV Scraper Monitor</h1>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header("🎛️ Controls")
    
    # Manual scrape button
    if st.button("🚀 Manual Scrape", type="primary", use_container_width=True):
        success, current, previous = perform_scrape()
        if success:
            st.success("Scrape completed successfully!")
        else:
            st.error("Scrape failed!")
    
    st.divider()
    
    # Monitoring controls
    st.subheader("📡 Monitoring")
    
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.monitoring:
            if st.button("▶️ Start Monitoring", use_container_width=True):
                start_monitoring()
    with col2:
        if st.session_state.monitoring:
            if st.button("⏹️ Stop Monitoring", use_container_width=True):
                stop_monitoring()
    
    # Monitoring status
    if st.session_state.monitoring:
        st.success("🟢 Monitoring Active")
    else:
        st.info("⚪ Monitoring Inactive")
    
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
    
    # Load current data
    current_data = load_historical_data()
    
    if not current_data.empty:
        latest_data = current_data.iloc[-1]
        
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
            time_diff = datetime.now() - last_update.replace(tzinfo=None)
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
    
    if not current_data.empty:
        # Create timeline chart
        fig = px.line(
            current_data, 
            x='timestamp', 
            y='sb_number',
            title="SB Number Timeline",
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
        display_data = current_data.copy()
        display_data['timestamp'] = display_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(display_data, use_container_width=True)
    else:
        st.info("No historical data available. Run a manual scrape to get started!")

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
    "🔍 **PMSV Scraper Monitor** - Real-time monitoring of EU medical device incident report forms | "
    "Built with Streamlit"
)
