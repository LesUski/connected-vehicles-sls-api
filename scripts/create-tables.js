const { DynamoDBClient, CreateTableCommand, BatchWriteItemCommand } = require('@aws-sdk/client-dynamodb');

// Configure DynamoDB client for local development
const client = new DynamoDBClient({
    region: 'eu-central-1',
    endpoint: 'http://localhost:8000',
    credentials: {
        accessKeyId: 'LOCAL',
        secretAccessKey: 'LOCAL'
    }
});

const TABLE_NAME = 'connected-vehicles-api-local';

async function createTable() {
    const params = {
        TableName: TABLE_NAME,
        AttributeDefinitions: [
            {
                AttributeName: 'PK',
                AttributeType: 'S'
            },
            {
                AttributeName: 'SK',
                AttributeType: 'S'
            }
        ],
        KeySchema: [
            {
                AttributeName: 'PK',
                KeyType: 'HASH'
            },
            {
                AttributeName: 'SK',
                KeyType: 'RANGE'
            }
        ],
        GlobalSecondaryIndexes: [
            {
                IndexName: 'SK-PK-index',
                KeySchema: [
                    {
                        AttributeName: 'SK',
                        KeyType: 'HASH'
                    },
                    {
                        AttributeName: 'PK',
                        KeyType: 'RANGE'
                    }
                ],
                Projection: {
                    ProjectionType: 'ALL'
                }
            }
        ],
        BillingMode: 'PAY_PER_REQUEST'
    };

    try {
        console.log('Creating DynamoDB table...');
        const createTableCommand = new CreateTableCommand(params);
        await client.send(createTableCommand);
        console.log(`Table ${TABLE_NAME} created successfully`);
        
        // Wait for table to be active
        console.log('Waiting for table to be active...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        // Load and insert seed data
        await insertSeedData();
        
    } catch (error) {
        if (error.name === 'ResourceInUseException') {
            console.log(`Table ${TABLE_NAME} already exists`);
            // Still try to insert seed data
            await insertSeedData();
        } else {
            console.error('Error creating table:', error);
            process.exit(1);
        }
    }
}

async function insertSeedData() {
    try {
        console.log('Inserting seed data...');
        const seedData = require('../seeds/connected_vehicles.json');
        
        // Split items into chunks of 25 (DynamoDB batch write limit)
        const chunks = chunkArray(seedData.Connected_Vehicle, 25);
        
        for (const chunk of chunks) {
            const batchParams = {
                RequestItems: {
                    [TABLE_NAME]: chunk
                }
            };
            
            const batchWriteCommand = new BatchWriteItemCommand(batchParams);
            await client.send(batchWriteCommand);
        }
        
        console.log('Seed data inserted successfully');
    } catch (error) {
        console.error('Error inserting seed data:', error);
        process.exit(1);
    }
}

function chunkArray(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
        chunks.push(array.slice(i, i + size));
    }
    return chunks;
}

// Add error handling for the main execution
(async () => {
    try {
        await createTable();
        console.log('Setup completed successfully');
        process.exit(0);
    } catch (error) {
        console.error('Unhandled error:', error);
        process.exit(1);
    }
})();