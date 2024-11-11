const AWS = require('aws-sdk');
const fs = require('fs');
const path = require('path');

// Configure AWS SDK for local DynamoDB
const dynamodb = new AWS.DynamoDB({
    region: 'us-east-1',
    endpoint: 'http://localhost:8000',
    credentials: {
        accessKeyId: 'LOCAL',
        secretAccessKey: 'LOCAL'
    }
});

async function createTable() {
    const params = {
        TableName: 'connected-vehicles-api-local',
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
        await dynamodb.createTable(params).promise();
        console.log(`Table ${params.TableName} created successfully`);
        
        // Load and insert seed data
        const seedData = require('../seeds/connected_vehicles.json');
        const batchParams = {
            RequestItems: {
                'connected-vehicles-api-local': seedData.Connected_Vehicle
            }
        };
        
        await dynamodb.batchWriteItem(batchParams).promise();
        console.log('Seed data inserted successfully');
        
    } catch (error) {
        if (error.code === 'ResourceInUseException') {
            console.log(`Table already exists`);
        } else {
            console.error('Error creating table:', error);
        }
    }
}

createTable();
