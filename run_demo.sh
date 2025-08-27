#!/bin/bash

# PMSV Scraper Streamlit Demo Runner
echo "🎭 Starting PMSV Scraper Monitor - Demo..."

# Run the Streamlit demo app using uv
echo "🚀 Launching Streamlit demo app..."
uv run streamlit run streamlit_demo.py --server.port 8502 --server.address 0.0.0.0
