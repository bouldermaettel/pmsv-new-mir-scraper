# 🔍 PMSV Scraper Monitor - Streamlit App

A beautiful, real-time web interface to monitor and observe your PMSV scraper in action.

## 🚀 Quick Start

### Option 1: Using the provided script (Recommended)
```bash
./run_streamlit.sh
```

### Option 2: Using uv (if you prefer uv)
```bash
# Install dependencies
uv sync

# Run the Streamlit app
uv run streamlit run streamlit_app.py
```

### Option 3: Manual installation and run
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

The app will be available at: **http://localhost:8501**

### 🎭 Demo Version
If you want to see the interface without running actual web scraping, you can use the demo version:

```bash
./run_demo.sh
```

The demo will be available at: **http://localhost:8502**

## 🎯 Features

### 📊 Real-time Monitoring Dashboard
- **Current Status Cards**: Live display of current SB number, last update time, and total checks
- **Historical Timeline**: Interactive chart showing SB number changes over time
- **Data Table**: Complete historical records in a sortable table format

### 🎛️ Interactive Controls
- **Manual Scrape**: Trigger a single scrape operation on demand
- **Continuous Monitoring**: Start/stop automatic monitoring (checks every 5 minutes)
- **Auto-refresh**: Configurable dashboard refresh intervals

### 📝 Live Activity Log
- **Real-time Logging**: See exactly what the scraper is doing
- **Status Indicators**: Color-coded success, warning, and error messages
- **Recent Checks**: Quick overview of the last 10 scraping attempts

### 🎨 Modern UI
- **Responsive Design**: Works on desktop and mobile devices
- **Beautiful Styling**: Modern gradient cards and clean typography
- **Intuitive Layout**: Easy-to-navigate sidebar controls and main dashboard

## 🔧 How to Use

### 1. Initial Setup
1. Run the app using one of the methods above
2. Open your browser to `http://localhost:8501`
3. The app will automatically load any existing historical data

### 2. Manual Scraping
1. Click the **"🚀 Manual Scrape"** button in the sidebar
2. Watch the live activity log for real-time updates
3. View results in the status cards and historical chart

### 3. Continuous Monitoring
1. Click **"▶️ Start Monitoring"** to begin automatic checks
2. The app will check for updates every 5 minutes
3. Click **"⏹️ Stop Monitoring"** to stop automatic checks

### 4. Data Analysis
- **Timeline Chart**: Hover over points to see exact dates and SB numbers
- **Historical Table**: Sort and filter through all recorded data
- **Recent Checks**: Quick status overview of recent scraping attempts

## 📊 Understanding the Data

### SB Number
The SB number is extracted from the EU medical device incident report form. Changes in this number indicate updates to the form.

### Status Indicators
- **🟢 Updated**: New SB number detected
- **🟡 Unchanged**: No change from previous check
- **🔴 Error**: Failed to retrieve or process data

### Historical Data
The app maintains a complete history of all SB number changes, allowing you to:
- Track when updates occurred
- Analyze patterns in form updates
- Monitor the scraper's reliability

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Your existing PMSV scraper class
- **Data Storage**: JSON file (`sb_number_data.json`)
- **Real-time Updates**: Threading for continuous monitoring

### Dependencies
- `streamlit`: Web app framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive charts and visualizations
- `requests` & `beautifulsoup4`: Web scraping (from your existing scraper)

### File Structure
```
├── streamlit_app.py          # Main Streamlit application
├── scraper.py               # Your existing scraper logic
├── sb_number_data.json      # Historical data storage
├── requirements.txt         # Python dependencies
└── run_streamlit.sh        # Quick start script
```

## 🎨 Customization

### Styling
The app uses custom CSS for styling. You can modify the appearance by editing the CSS section in `streamlit_app.py`.

### Monitoring Interval
Change the monitoring interval by modifying the `time.sleep(300)` value in the `monitor_loop()` function (currently 5 minutes).

### Log Retention
Adjust the number of log entries kept in memory by changing the `max_logs` parameter in the `StreamlitLogger` class.

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

2. **Dependencies not found**
   ```bash
   pip install -r requirements.txt
   ```

3. **No historical data**
   - Run a manual scrape first
   - Check if `sb_number_data.json` exists

4. **Monitoring not working**
   - Ensure you have internet connectivity
   - Check the live activity log for error messages

### Debug Mode
For detailed debugging, you can run Streamlit in debug mode:
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 🚀 Next Steps

This Streamlit app provides a solid foundation for monitoring your PMSV scraper. You can extend it with:

- **Email Notifications**: Integrate with your existing email notifier
- **Database Storage**: Switch from JSON to a proper database
- **Advanced Analytics**: Add more charts and statistical analysis
- **User Authentication**: Add login functionality for team access
- **API Endpoints**: Expose data via REST API

---

**Happy Monitoring! 🎉**
