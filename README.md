# Flask JWT API Application

This is a Flask-based API application that generates and validates JSON Web Tokens (JWTs). The application includes features like IP-based filtering, CORS (Cross-Origin Resource Sharing) configuration, and configurable JWT expiration. The application is containerized using Docker for easy deployment.

---

## Features

- Generate JWTs with configurable expiration time
- Validate JWTs to ensure security
- Restrict CORS to specific origins
- Restrict access based on IP addresses (if implemented)
- Configurable with environment variables
- Containerized with Docker for portability

---

## Requirements

- Python 3.9 or higher
- Flask
- Docker (optional, for containerized deployment)

---

## Deployment

Docker Compose Configuration
docker-compose.yml
Below is the docker-compose.yml file used to deploy this application:


```yaml
version: '3.9'

services:
  flask-app:
    image: adclab/flashjwt
    ports:
      - "5000:5000"
    env_file:
      - .env
    environment:
      FLASK_RUN_HOST: 0.0.0.0
      FLASK_RUN_PORT: 5000
'''

---

## API Endpoints

### 1. Generate JWT

**Endpoint**: `/generate-key`  
**Method**: `POST`

**Description**: Generates a new JWT with an expiration time.

**Example Request**:

```bash
curl -X POST http://127.0.0.1:5000/generate-key
```

**Example Response**:

```json
{
  "api_key": "<your_generated_jwt>",
  "expires_at": "2023-01-01T12:00:00Z"
}
```

---

### 2. Validate JWT

**Endpoint**: `/validate-key`  
**Method**: `POST`

**Description**: Validates a provided JWT.

**Example Request**:

```bash
curl -X POST http://127.0.0.1:5000/validate-key \
     -H "Content-Type: application/json" \
     -d '{"api_key": "<your_jwt_here>"}'
```

**Example Response** (Valid Token):

```json
{
  "status": "valid",
  "expires_at": 1672531200
}
```

**Example Response** (Expired Token):

```json
{
  "status": "expired"
}
```

**Example Response** (Invalid Token):

```json
{
  "status": "invalid"
}
```

---

## Running with Docker

### 1. Build the Docker Image

```bash
docker build -t flask-jwt-api .
```

### 2. Run the Docker Container

```bash
docker run -d -p 5000:5000 --env-file .env flask-jwt-api
```

The application will be accessible at `http://localhost:5000`.

---

## Environment Variables

| Variable Name          | Description                             | Default Value               |
|-------------------------|-----------------------------------------|-----------------------------|
| `CORS_ORIGINS`          | Comma-separated list of allowed origins | (None - CORS disabled)      |
| `SECRET_KEY`            | Secret key for signing JWTs            | `default_secret_key`        |
| `JWT_EXPIRATION_MINUTES`| Expiration time for JWTs in minutes     | `20`                        |

---

### Example cURL Commands

#### Generate JWT
```bash
curl -X POST http://127.0.0.1:5000/generate-key
```

#### Validate JWT
```bash
curl -X POST http://127.0.0.1:5000/validate-key \
     -H "Content-Type: application/json" \
     -d '{"api_key": "<your_jwt_here>"}'
```

