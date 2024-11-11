const { execSync } = require('child_process');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function setupLocal() {
    try {
        // Wait for DynamoDB to start
        console.log('Waiting for DynamoDB to start...');
        await sleep(5000);

        // Check DynamoDB connection
        console.log('Checking DynamoDB connection...');
        let retries = 0;
        const maxRetries = 10;

        while (retries < maxRetries) {
            try {
                require('./check-dynamodb.js');
                break;
            } catch (error) {
                retries++;
                console.log(`Attempt ${retries}/${maxRetries}`);
                await sleep(1000);
            }
        }

        if (retries === maxRetries) {
            throw new Error('Failed to connect to DynamoDB');
        }

        // Create tables and load data
        console.log('Creating tables and loading seed data...');
        execSync('npm run dynamodb:create-tables', { stdio: 'inherit' });

        // Start the API
        console.log('Starting the API...');
        execSync('npm run start:api', { stdio: 'inherit' });

    } catch (error) {
        console.error('Setup failed:', error);
        process.exit(1);
    }
}

setupLocal();
