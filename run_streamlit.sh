#!/bin/bash

# PMSV Scraper Streamlit App Runner
echo "🔍 Starting PMSV Scraper Monitor..."

# Run the Streamlit app using uv
echo "🚀 Launching Streamlit app..."
uv run streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
