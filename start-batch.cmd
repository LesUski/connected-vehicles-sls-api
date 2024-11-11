@echo off
echo Creating directories...
mkdir docker\dynamodb 2>nul

echo Starting DynamoDB in Docker...
start "DynamoDB Local" docker-compose up dynamodb

echo Waiting for DynamoDB to start...
timeout /t 5 /nobreak

echo Checking DynamoDB connection...
node scripts/check-dynamodb.js
if errorlevel 1 (
    echo Failed to connect to DynamoDB
    exit /b 1
)

echo Creating tables and loading seed data...
call npm run dynamodb:create-tables
if errorlevel 1 (
    echo Failed to create tables and load seed data
    exit /b 1
)

echo Starting Serverless Offline API...
call npm run start:api
