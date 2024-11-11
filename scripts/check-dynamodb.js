const { DynamoDBClient, ListTablesCommand } = require('@aws-sdk/client-dynamodb');

const client = new DynamoDBClient({
    region: 'eu-central-1',
    endpoint: 'http://localhost:8000',
    credentials: {
        accessKeyId: 'LOCAL',
        secretAccessKey: 'LOCAL'
    }
});

async function checkDynamoDB() {
    let retries = 0;
    const maxRetries = 10;
    const delay = 1000; // 1 second

    while (retries < maxRetries) {
        try {
            console.log('Checking DynamoDB connection...');
            const command = new ListTablesCommand({});
            await client.send(command);
            console.log('DynamoDB is ready!');
            return true;
        } catch (error) {
            retries++;
            console.log(`Attempt ${retries}/${maxRetries} failed. Retrying in 1 second...`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
    
    console.error('Failed to connect to DynamoDB after maximum retries');
    return false;
}

(async () => {
    const isReady = await checkDynamoDB();
    process.exit(isReady ? 0 : 1);
})();
