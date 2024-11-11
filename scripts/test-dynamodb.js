const { DynamoDBClient, QueryCommand } = require('@aws-sdk/client-dynamodb');

const client = new DynamoDBClient({
    region: 'eu-central-1',
    endpoint: 'http://localhost:8000',
    credentials: {
        accessKeyId: 'LOCAL',
        secretAccessKey: 'LOCAL'
    }
});

async function testQuery() {
    try {
        const params = {
            TableName: 'connected-vehicles-api-local',
            KeyConditionExpression: 'PK = :pk',
            ExpressionAttributeValues: {
                ':pk': { S: 'VIN#WDDJK7DA4FF954840' }
            }
        };

        const command = new QueryCommand(params);
        const result = await client.send(command);
        
        console.log('Query successful!');
        console.log('Items found:', result.Items.length);
        console.log('First item:', JSON.stringify(result.Items[0], null, 2));
        
        return true;
    } catch (error) {
        console.error('Error querying DynamoDB:', error);
        return false;
    }
}

(async () => {
    const success = await testQuery();
    process.exit(success ? 0 : 1);
})();
