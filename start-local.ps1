# Create necessary directories
New-Item -ItemType Directory -Force -Path "docker/dynamodb"

# Start DynamoDB in Docker
Start-Process powershell -ArgumentList "docker-compose up dynamodb" -NoNewWindow

# Wait for DynamoDB to start
Start-Sleep -Seconds 5

# Create tables and load seed data
npm run dynamodb:create-tables

# Start the Serverless Offline API
npm run start:api
