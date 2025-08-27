# PMSV Monitor - SB Number Change Detector

A Python application that monitors the PMSV (Post-Market Surveillance) reporting forms webpage for changes in the SB number and sends email notifications when updates are detected.

## Features

- **Web Scraping**: Monitors the EU Health PMSV reporting forms page
- **Change Detection**: Tracks SB number changes in MIR 7.3.1 forms
- **Email Notifications**: Sends alerts when SB numbers are updated
- **Scheduled Monitoring**: Configurable check intervals
- **Docker Support**: Containerized for easy deployment
- **Azure Container Apps**: Ready for cloud deployment
- **Fast Dependency Management**: Uses `uv` for lightning-fast package management

## Target Website

The application monitors: [PMSV Reporting Forms](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance/pmsv-reporting-forms_en)

Specifically, it looks for changes in the SB number on the line:
> "New manufacturer incident report (MIR 7.3.1. PDF form - SB 10573)"

## Prerequisites

- Python 3.11+
- `uv` (Python package manager) - will be installed automatically
- Docker (for containerized deployment)
- Azure CLI (for Azure deployment)
- SMTP email credentials (Gmail, Outlook, etc.)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pmsv-new-mir-scraper
```

### 2. Setup with uv (Recommended)

```bash
# Make setup script executable
chmod +x setup-uv.sh

# Run the setup script
./setup-uv.sh
```

The setup script will:
- Install `uv` if not already installed
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Generate a `.env` template

### 3. Configure Environment Variables

Edit the `.env` file created by the setup script:

```env
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com

# SMTP Settings (optional, defaults to Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Monitoring Configuration
CHECK_INTERVAL_HOURS=24
```

**Note**: For Gmail, you'll need to use an App Password instead of your regular password.

### 4. Run the Application

```bash
# Using uv (recommended)
uv run python main.py

# Or activate the virtual environment manually
source .venv/bin/activate
python main.py
```

## Docker Deployment

### Local Docker

```bash
# Build the image
docker build -t pmsv-monitor .

# Run the container
docker run -d \
  --name pmsv-monitor \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  pmsv-monitor
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## Azure Container Apps Deployment

### 1. Prerequisites

- Azure CLI installed and logged in
- Azure Container Registry (optional, for production)
- Bicep CLI installed

### 2. Deploy to Azure

#### Option A: Using PowerShell Script

```powershell
# Deploy with local image (for testing)
.\deploy.ps1

# Deploy with Azure Container Registry
.\deploy.ps1 -ContainerRegistry "yourregistry.azurecr.io"
```

#### Option B: Using Bash Script

```bash
# Deploy with Azure Container Registry
./deploy-acr.sh
```

#### Option C: Manual Deployment

```bash
# Create resource group
az group create --name pmsv-monitor-rg --location "West Europe"

# Build and push image (if using ACR)
docker build -t yourregistry.azurecr.io/pmsv-monitor:latest .
docker push yourregistry.azurecr.io/pmsv-monitor:latest

# Deploy using Bicep
az deployment group create \
  --resource-group pmsv-monitor-rg \
  --template-file azure-container-app.bicep \
  --parameters containerImage="yourregistry.azurecr.io/pmsv-monitor:latest"
```

### 3. Configure Secrets in Azure

After deployment, configure the email secrets in the Azure Container App:

```bash
# Set email secrets
az containerapp secret set \
  --name pmsv-monitor \
  --resource-group pmsv-monitor-rg \
  --secrets sender-email="your-email@gmail.com" \
             sender-password="your-app-password" \
             recipient-email="recipient@example.com"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHECK_INTERVAL_HOURS` | How often to check for updates (hours) | 24 |
| `SENDER_EMAIL` | Email address to send notifications from | Required |
| `SENDER_PASSWORD` | Email password/app password | Required |
| `RECIPIENT_EMAIL` | Email address to receive notifications | Required |
| `SMTP_SERVER` | SMTP server address | smtp.gmail.com |
| `SMTP_PORT` | SMTP server port | 587 |

### Data Storage

The application stores the current SB number in a JSON file (`sb_number_data.json`) with the following structure:

```json
{
  "sb_number": "10573",
  "last_updated": "2024-01-15T10:30:00",
  "timestamp": 1705315800.0
}
```

## Development with uv

### Useful uv Commands

```bash
# Run the application
uv run python main.py

# Run tests
uv run python test_scraper.py

# Add a new dependency
uv add requests

# Add a development dependency
uv add --dev pytest

# Remove a dependency
uv remove requests

# Sync dependencies
uv sync

# Show dependency tree
uv tree
```

### Adding New Dependencies

```bash
# Add a production dependency
uv add requests

# Add a development dependency
uv add --dev pytest black

# The dependency will be automatically added to pyproject.toml
```

## Monitoring and Logs

### Log Files

- `pmsv_monitor.log` - Main application logs
- `scraper.log` - Web scraping specific logs

### Azure Monitoring

When deployed to Azure Container Apps, logs are automatically sent to Log Analytics Workspace for monitoring and alerting.

## Troubleshooting

### Common Issues

1. **Email Notifications Not Working**
   - Verify SMTP credentials
   - Check if using App Password for Gmail
   - Ensure firewall allows SMTP traffic

2. **Web Scraping Fails**
   - Check internet connectivity
   - Verify the target website is accessible
   - Review logs for specific error messages

3. **Container Won't Start**
   - Check environment variables are set correctly
   - Verify Docker image builds successfully
   - Review container logs

4. **uv Installation Issues**
   - Ensure you have curl installed
   - Check your shell configuration file (~/.bashrc or ~/.zshrc)
   - Restart your terminal after installation

### Debug Mode

To run in debug mode with more verbose logging:

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG
uv run python main.py
```

## Security Considerations

- Store sensitive credentials as Azure Key Vault secrets in production
- Use managed identities for Azure services when possible
- Regularly rotate email app passwords
- Monitor application logs for suspicious activity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue in the repository
