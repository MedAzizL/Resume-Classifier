# Azure Deployment Script for Resume Classifier Backend
# Requires: Azure CLI logged in with `az login`

Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOYING RESUME CLASSIFIER TO AZURE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Configuration
$RESOURCE_GROUP = "resume-classifier-rg"
$LOCATION = "francecentral"
$APP_NAME = "resume-classifier-backend"
$PLAN_NAME = "resume-classifier-plan"
$SUBSCRIPTION_NAME = "Azure for Students"

# Select subscription
Write-Host "Selecting subscription: $SUBSCRIPTION_NAME..." -ForegroundColor Cyan
az account set --subscription $SUBSCRIPTION_NAME

# Create Resource Group
Write-Host "Creating resource group: $RESOURCE_GROUP..." -ForegroundColor Cyan
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan (B1 Basic)
Write-Host "Creating App Service Plan: $PLAN_NAME..." -ForegroundColor Cyan
az appservice plan create `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --sku B1 `
    --is-linux

# Create Web App
Write-Host "Creating Web App: $APP_NAME..." -ForegroundColor Cyan
az webapp create `
    --name $APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --runtime "PYTHON:3.11"

# Configure Web App
Write-Host "Configuring Web App..." -ForegroundColor Cyan
az webapp config set `
    --name $APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

# Set environment variables
Write-Host "Setting environment variables..." -ForegroundColor Cyan
az webapp config appsettings set `
    --name $APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Deploy from local git
Write-Host "Preparing deployment..." -ForegroundColor Cyan
$publishUrl = az webapp deployment source config-local-git `
    --name $APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query url `
    --output tsv

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT PREPARED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "App URL: https://$APP_NAME.azurewebsites.net" -ForegroundColor Yellow
Write-Host ""
Write-Host "To complete deployment, run these commands in the backend folder:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  git init" -ForegroundColor White
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "  git remote add azure $publishUrl" -ForegroundColor White
Write-Host "  git push azure master" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Green

