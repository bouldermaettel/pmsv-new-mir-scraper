#!/usr/bin/env pwsh

param(
    [string]$ResourceGroupName = "pmsv-monitor-rg",
    [string]$Location = "West Europe",
    [string]$ContainerAppName = "pmsv-monitor",
    [string]$ContainerRegistry = "",
    [string]$ImageTag = "latest"
)

Write-Host "Starting PMSV Monitor deployment to Azure Container Apps..." -ForegroundColor Green

# Check if Azure CLI is installed and logged in
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "Azure CLI version: $($azVersion.'azure-cli')" -ForegroundColor Yellow
} catch {
    Write-Error "Azure CLI is not installed or not in PATH. Please install Azure CLI first."
    exit 1
}

# Check if logged in to Azure
$account = az account show --output json 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "Not logged in to Azure. Please run 'az login' first." -ForegroundColor Yellow
    az login
}

# Create resource group if it doesn't exist
Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location --output none

# Build and push Docker image if container registry is specified
if ($ContainerRegistry) {
    Write-Host "Building Docker image..." -ForegroundColor Yellow
    docker build -t $ContainerRegistry/$ContainerAppName:$ImageTag .
    
    Write-Host "Pushing Docker image to registry..." -ForegroundColor Yellow
    docker push $ContainerRegistry/$ContainerAppName:$ImageTag
    
    $fullImageName = "$ContainerRegistry/$ContainerAppName:$ImageTag"
} else {
    # Use local image for testing
    Write-Host "Building local Docker image..." -ForegroundColor Yellow
    docker build -t $ContainerAppName:$ImageTag .
    $fullImageName = "$ContainerAppName:$ImageTag"
}

# Deploy using Bicep template
Write-Host "Deploying Container App using Bicep..." -ForegroundColor Yellow
$deploymentName = "pmsv-monitor-deployment-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

$deploymentParams = @{
    containerAppName = $ContainerAppName
    containerImage = $fullImageName
    location = $Location
}

az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file "azure-container-app.bicep" `
    --parameters $deploymentParams `
    --name $deploymentName `
    --output table

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "Container App Name: $ContainerAppName" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Cyan

# Get the Container App URL
$containerApp = az containerapp show --name $ContainerAppName --resource-group $ResourceGroupName --output json | ConvertFrom-Json
Write-Host "Container App URL: $($containerApp.properties.configuration.ingress.fqdn)" -ForegroundColor Cyan

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Configure email settings in the Container App" -ForegroundColor White
Write-Host "2. Set up secrets for SMTP credentials" -ForegroundColor White
Write-Host "3. Monitor the application logs" -ForegroundColor White
