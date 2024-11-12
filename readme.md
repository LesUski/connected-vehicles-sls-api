# Connected Vehicles API

A boilerplate/starter project demonstrating serverless architecture using AWS services with local development capabilities. This project showcases the implementation of a simple API for managing connected vehicles data using modern serverless practices.

## Architecture Overview

The project utilizes several AWS services:
- **API Gateway**: HTTP API for RESTful endpoints
- **Lambda**: Serverless compute for request handling
- **Step Functions**: Orchestration of the validation and processing workflow
- **DynamoDB**: NoSQL database for vehicle and user data

### Key Features
- Single-table design with composite keys (PK/SK) for DynamoDB
- Asynchronous processing using Step Functions
- Validation layer for data integrity
- Local development environment
- Python-based Lambda functions with PynamoDB ORM
- Serverless Framework for infrastructure as code

## Prerequisites

- Node.js (v14 or later)
- Python 3.9
- AWS CLI configured for deployment
- Serverless Framework CLI
- Docker (for local DynamoDB)

## Project Structure

```
connected-vehicles-api/
├── serverless.yml              # Serverless Framework configuration
├── requirements.txt            # Python production dependencies
├── requirements-dev.txt        # Python development dependencies
├── src/
│   ├── handlers/              # Lambda function handlers
│   ├── models/                # PynamoDB models
│   ├── services/              # Business logic services
│   └── utils/                 # Utility functions
├── tests/                     # Test files
└── seeds/                     # DynamoDB seed data
```

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd connected-vehicles-api
```

2. Install dependencies:
```bash
# Install Node.js dependencies
npm install

# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements-dev.txt
```

3. Start local development environment:
```bash
npm run start:local
```

## Local Development

The project uses serverless-offline plugin for local development, which provides:
- Local API Gateway emulation
- Local Lambda function execution
- Local DynamoDB instance
- Hot reloading for development

### Running Locally

Start the local development environment:
```bash
npm run start:local
```

This will start:
- API Gateway at http://localhost:4000
- Lambda emulator at port 4002
- DynamoDB Local at port 8000

### Testing the API

Create a vehicle:
```bash
curl -X POST http://localhost:4000/vehicles \
-H "Content-Type: application/json" \
-d '{
  "vehicle_id": "WDDJK7DA4FF954840",
  "torque": "308",
  "drivetrain": "4WD",
  "engine": "gasoline",
  "horsepower": "406"
}'
```

Add a vehicle feature:
```bash
curl -X POST http://localhost:4000/vehicles/WDDJK7DA4FF954840/features \
-H "Content-Type: application/json" \
-d '{
  "feature_type": "cameras",
  "feature_data": {
    "cameras": {
      "front_camera_center": {
        "foo": "bar"
      }
    },
    "recording_is_active": true
  }
}'
```

## Testing

The project includes various types of tests:

1. Run unit tests:
```bash
pytest tests/unit
```

2. Run integration tests:
```bash
pytest tests/integration
```

3. Run local API tests:
```bash
pytest tests/test_local_api.py
```

## Deployment

Deploy to AWS:
```bash
# Deploy to development
npm run deploy:dev

# Deploy to production
npm run deploy:prod
```

## DynamoDB Data Model

The project uses a single-table design with the following key schema:
- Partition Key (PK): Entity identifier (e.g., "VIN#123", "ID#user1")
- Sort Key (SK): Entity type or metadata (e.g., "#META#", "FEATURE#CAMERAS")

Example item:
```json
{
  "PK": "VIN#WDDJK7DA4FF954840",
  "SK": "#META#",
  "vehicle_id": "WDDJK7DA4FF954840",
  "torque": "308",
  "drivetrain": "4WD",
  "engine": "gasoline",
  "horsepower": "406"
}
```

## Future Enhancements

This is a starter project that can be extended with:
- Authentication and authorization
- Additional vehicle features
- Real-time updates using WebSockets
- Enhanced monitoring and logging
- Additional data access patterns
- CI/CD pipeline
- Infrastructure testing

## Contributing

This is a boilerplate project - feel free to use it as a starting point for your own implementation. Contributions to improve the base functionality are welcome.

## License

MIT

