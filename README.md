# Similarity Check API

A Flask REST API for comparing text similarity using spaCy's NLP models and MongoDB for user management.

## Features

- **User Registration**: Create accounts with username and password authentication
- **Text Similarity Detection**: Compare two texts and get a similarity score (0-1)
- **Token-Based Usage**: Each user gets 6 tokens; each operation costs 1 token
- **Token Refill**: Admin endpoint to refill user tokens
- **MongoDB Integration**: Persistent storage of users and authentication data
- **bcrypt Security**: Password hashing for secure storage

## Architecture

- **Framework**: Flask + Flask-RESTful
- **Database**: MongoDB
- **NLP**: spaCy (en_core_web_sm model)
- **Security**: bcrypt for password hashing
- **Containerization**: Docker + Docker Compose

## Prerequisites

- Docker & Docker Compose
- MongoDB running (included in docker-compose.yml)
- Python 3.12+ (if running locally)

## Installation & Setup

### Using Docker Compose (Recommended)

```bash
cd SimilarityCheckProj
docker compose build
docker compose up -d
```

The API will be available at `http://localhost:5000`

### Local Setup

```bash
pip install -r web/requirements.txt
python web/app.py
```

MongoDB must be running on `mongodb://localhost:27017/`

## API Endpoints

### 1. Register User

**POST** `/register`

```json
{
  "username": "bhn",
  "password": "112233"
}
```

**Response** (Status 200):
```json
{
  "message": "User registered successfully",
  "status": 200
}
```

### 2. Detect Text Similarity

**POST** `/detect`

```json
{
  "username": "bhn",
  "password": "112233",
  "text1": "I love programming",
  "text2": "I enjoy coding"
}
```

**Response** (Status 200):
```json
{
  "similarity": 0.85,
  "msg": "Similarity score calculated",
  "status": 200
}
```

**Error Responses**:
- `status: 301` - User not found
- `status: 302` - Incorrect password
- `status: 303` - Not enough tokens

### 3. Refill Tokens

**POST** `/refill`

```json
{
  "username": "bhn",
  "admin_pw": "admin",
  "refill": 10
}
```

**Response** (Status 200):
```json
{
  "message": "Tokens refilled successfully",
  "status": 200
}
```

## Usage Examples

### Using curl

Register a user:
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"bhn","password":"112233"}'
```

Compare texts:
```bash
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{
    "username":"bhn",
    "password":"112233",
    "text1":"I love programming",
    "text2":"I enjoy coding"
  }'
```

Refill tokens:
```bash
curl -X POST http://localhost:5000/refill \
  -H "Content-Type: application/json" \
  -d '{"username":"bhn","admin_pw":"admin","refill":20}'
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:5000"

# Register
response = requests.post(f"{BASE_URL}/register", json={
    "username": "bhn",
    "password": "112233"
})
print(response.json())

# Detect similarity
response = requests.post(f"{BASE_URL}/detect", json={
    "username": "bhn",
    "password": "112233",
    "text1": "Hello world",
    "text2": "Hi world"
})
print(response.json())
```

## Project Structure

```
SimilarityCheckProj/
├── docker-compose.yml          # Docker services definition
├── web/
│   ├── app.py                  # Flask application
│   ├── Dockerfile              # Python 3.12 image
│   ├── requirements.txt         # Python dependencies
│   └── en_core_web_sm-3.8.0.tar.gz  # spaCy model (local)
├── db/
│   └── Dockerfile              # MongoDB image
└── README.md                   # This file
```

## Dependencies

- **Flask**: Web framework
- **flask-restful**: REST API toolkit
- **pymongo**: MongoDB driver
- **bcrypt**: Password hashing
- **spacy**: NLP library
- **en_core_web_sm**: English language model

See `web/requirements.txt` for exact versions.

## Security Notes

⚠️ **Production Considerations**:
- Change admin password (`"admin"` in `/refill` endpoint)
- Use environment variables for sensitive data
- Enable MongoDB authentication
- Use HTTPS in production
- Implement rate limiting
- Add input validation for text lengths

## Database

MongoDB collections:
- `Users` - Stores username, hashed password, sentence, tokens
  ```json
  {
    "Username": "string",
    "Password": "bytes (hashed)",
    "Sentence": "string",
    "Tokens": "integer"
  }
  ```

## Development

### Run Tests

```bash
# Test endpoints using Postman or curl (examples above)
```

### View Logs

```bash
docker compose logs -f web
docker compose logs -f db
```

### Stop Services

```bash
docker compose down
```

### Clean Up

```bash
docker compose down -v  # Remove volumes too
```

## Troubleshooting

**"User not found" (status 301)**
- Ensure the user is registered first via `/register`

**"Incorrect password" (status 302)**
- Check username and password match the registered credentials

**"Not enough tokens" (status 303)**
- Use `/refill` endpoint to add more tokens

**MongoDB connection error**
- Ensure `docker compose up -d` is running
- Check MongoDB is listening on port 27017

## License

This project is for educational purposes.

## Author

Bhanu Rathore (bcoolrathore@gmail.com)
