#!/bin/bash

echo "🔧 Setting up PMSV Monitor environment with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    
    # Install uv using the official installer
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell configuration to make uv available
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
    
    echo "✅ uv installed successfully!"
else
    echo "✅ uv is already installed"
fi

# Check Python version
echo "🐍 Checking Python version..."
uv python list

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv sync

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
echo "2. Run tests: uv run python test_scraper.py"
echo "3. Start monitoring: uv run python main.py"
echo "4. Or use Docker: docker-compose up -d"
echo ""
echo "💡 Useful uv commands:"
echo "   uv run python main.py          # Run the application"
echo "   uv run python test_scraper.py  # Run tests"
echo "   uv add <package>               # Add a new dependency"
echo "   uv remove <package>            # Remove a dependency"
echo "   uv sync                        # Sync dependencies"
