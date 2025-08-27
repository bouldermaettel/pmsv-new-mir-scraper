#!/bin/bash

echo "🔧 Setting up PMSV Monitor environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Create .env template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOF
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com

# SMTP Settings (optional, defaults to Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Monitoring Configuration
CHECK_INTERVAL_HOURS=24
EOF
    echo "⚠️  Please edit .env file with your email credentials"
fi

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Edit .env file with your email credentials"
echo "2. Run tests: python test_scraper.py"
echo "3. Start monitoring: python main.py"
echo "4. Or use Docker: docker-compose up -d"
