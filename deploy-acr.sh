#!/bin/bash

# Azure Container Registry deployment script for PMSV Monitor

set -e

# Configuration
RESOURCE_GROUP="pmsv-monitor-rg"
LOCATION="westeurope"
ACR_NAME="pmsvmonitoracr"
CONTAINER_APP_NAME="pmsv-monitor"
IMAGE_NAME="pmsv-monitor"
IMAGE_TAG="latest"

echo "🚀 Starting PMSV Monitor deployment to Azure..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo "🔐 Not logged in to Azure. Please run 'az login' first."
    az login
fi

# Create resource group
echo "📦 Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION --output none

# Create Azure Container Registry
echo "🏗️ Creating Azure Container Registry: $ACR_NAME"
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true \
    --output none

# Get ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)
echo "📋 ACR Login Server: $ACR_LOGIN_SERVER"

# Login to ACR
echo "🔑 Logging in to Azure Container Registry..."
az acr login --name $ACR_NAME

# Build and tag Docker image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Tag image for ACR
FULL_IMAGE_NAME="$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
echo "🏷️ Tagging image: $FULL_IMAGE_NAME"
docker tag $IMAGE_NAME:$IMAGE_TAG $FULL_IMAGE_NAME

# Push image to ACR
echo "⬆️ Pushing image to Azure Container Registry..."
docker push $FULL_IMAGE_NAME

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Deploy Container App using Bicep
echo "🚀 Deploying Container App..."
az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file azure-container-app.bicep \
    --parameters \
        containerAppName=$CONTAINER_APP_NAME \
        containerImage=$FULL_IMAGE_NAME \
        containerRegistryServer=$ACR_LOGIN_SERVER \
        containerRegistryUsername=$ACR_USERNAME \
        containerRegistryPassword=$ACR_PASSWORD \
        location=$LOCATION \
    --output table

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Container Registry: $ACR_NAME"
echo "   Container App: $CONTAINER_APP_NAME"
echo "   Image: $FULL_IMAGE_NAME"
echo ""
echo "🔧 Next steps:"
echo "1. Configure email secrets in the Container App:"
echo "   az containerapp secret set \\"
echo "     --name $CONTAINER_APP_NAME \\"
echo "     --resource-group $RESOURCE_GROUP \\"
echo "     --secrets sender-email=\"your-email@gmail.com\" \\"
echo "                sender-password=\"your-app-password\" \\"
echo "                recipient-email=\"recipient@example.com\""
echo ""
echo "2. Monitor the application:"
echo "   az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo ""
echo "3. View Container App details:"
echo "   az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP"
