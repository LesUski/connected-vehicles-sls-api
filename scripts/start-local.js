const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Ensure docker/dynamodb directory exists
const dynamoDbPath = path.join(__dirname, '..', 'docker', 'dynamodb');
if (!fs.existsSync(dynamoDbPath)) {
    fs.mkdirSync(dynamoDbPath, { recursive: true });
}

// Function to run a command and return a promise
function runCommand(command, args, options = {}) {
    return new Promise((resolve, reject) => {
        const proc = spawn(command, args, {
            ...options,
            stdio: 'inherit',
            shell: true
        });

        proc.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`Command failed with code ${code}`));
            }
        });

        proc.on('error', (err) => {
            reject(err);
        });
    });
}

// Main function to start all services
async function startLocal() {
    try {
        // Start DynamoDB in detached mode
        console.log('Starting DynamoDB...');
        const dynamoProcess = spawn('docker-compose', ['up', 'dynamodb'], {
            stdio: 'inherit',
            detached: true
        });

        // Wait for DynamoDB to be ready
        console.log('Waiting for DynamoDB to be ready...');
        let retries = 0;
        const maxRetries = 10;
        
        while (retries < maxRetries) {
            try {
                await runCommand('node', ['scripts/check-dynamodb.js']);
                console.log('DynamoDB is ready!');
                break;
            } catch (error) {
                retries++;
                if (retries === maxRetries) {
                    throw new Error('DynamoDB failed to start');
                }
                console.log(`Retrying... (${retries}/${maxRetries})`);
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }

        // Create tables and load seed data
        console.log('Creating tables and loading seed data...');
        await runCommand('node', ['scripts/create-tables.js']);

        // Start the Serverless Offline API
        console.log('Starting Serverless Offline API...');
        await runCommand('npm', ['run', 'start:api']);

    } catch (error) {
        console.error('Error starting local environment:', error);
        process.exit(1);
    }
}

// Handle cleanup on exit
process.on('SIGINT', async () => {
    console.log('\nShutting down...');
    try {
        await runCommand('docker-compose', ['down']);
    } catch (error) {
        console.error('Error shutting down:', error);
    }
    process.exit();
});

startLocal();
