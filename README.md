# SWIFT Codes API

A REST API for managing and querying SWIFT/BIC (Bank Identifier Codes) information, including bank headquarters and their branches.

## Features

- **SWIFT Code Lookup**: Retrieve detailed information about any SWIFT code
- **Hierarchical Relationships**: Automatically identifies relationships between headquarters and branches
- **Country Filtering**: Get all SWIFT codes for a specific country
- **CRUD Operations**: Create, read, and delete SWIFT code records
- **Test Coverage**: Comprehensive unit tests for all endpoints

## Technologies

- Python 3.9+
- FastAPI (REST framework)
- SQLite (with option to upgrade to PostgreSQL/MySQL)
- Pydantic (data validation)
- Docker (containerization)

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip package manager
- Docker for containerized deployment

### Installation

1. Clone the repository:
   ```bash
   git https://github.com/illiadovhalenko/Remitly-Swift.git
   cd Remitly-Swift
   ```

2. Build the Docker Image:
   ```bash
   docker build -t swift-api . # On Windows: venv\Scripts\activate
   ```

3. Run the container:
   ```bash
   docker run -d -p 8080:8080 swift-api
   ```




The API will be available at `http://localhost:8080`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/swift-codes/{swift_code}` | GET | Get details for a specific SWIFT code |
| `/v1/swift-codes/country/{country_iso2}` | GET | Get all SWIFT codes for a country |
| `/v1/swift-codes/` | POST | Create a new SWIFT code record |
| `/v1/swift-codes/{swift_code}` | DELETE | Delete a SWIFT code record |

## Testing

### Running Tests

Execute the test suite with:
```bash
pytest
```

### Test Coverage

The test suite covers:
- SWIFT code lookup (headquarters and branches)
- Country filtering
- CRUD operations
- Error handling


## Example Requests

### Get SWIFT Code Details
```bash
curl -X 'GET' 'http://localhost:8080/v1/swift-codes/BCHICLRMXXX'
```

### Get SWIFT Codes by Country
```bash
curl -X 'GET' 'http://localhost:8080/v1/swift-codes/country/CL'
```

### Create New SWIFT Code
```bash
curl -X 'POST' 'http://localhost:8080/v1/swift-codes/' \
-H 'Content-Type: application/json' \
-d '{
  "swiftCode": "TEST1234XXX",
  "bankName": "Test Bank",
  "address": "123 Test Street",
  "countryISO2": "US",
  "countryName": "United States",
  "isHeadquarter": true
}'
```

## Data Structure

SWIFT codes ending with "XXX" are considered headquarters. Other codes are branches that belong to the headquarter with matching first 8 characters plus "XXX".

Example:
- `BCHICLRMXXX` (Headquarter)
- `BCHICLRMIMP` (Branch of BCHICLRMXXX)
