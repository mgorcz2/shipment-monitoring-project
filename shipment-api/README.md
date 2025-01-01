# Shipment monitoring

A project developed as part of the "Internet Service Programming" course.

A web-based application for tracking and managing courier shipments. This service allows users to monitor real-time status, track deliveries, and get detailed information about their shipments.
## Features
- Shipment list management
- Shipment status updates
- Nearest pickup location search
- Courier, sender and recipient management
## Technology stack
- Python 3.12.7
- PostgreSQL 17.0
- FastApi
- Docker

<img src="https://skillicons.dev/icons?i=python,postgres,fastapi,docker"/>


## Useful Commands
- Installing production dependencies: pip install -r requirements.txt
- Installing development dependencies: pip install -r requirements-dev.txt
- Starting the application server: uvicorn shipment-api.main:app --host 0.0.0.0 --port 8000
- API documentation (Swagger): http://localhost:8000/docs
- Building the project using Docker: docker compose build (to refresh the cache: docker compose build --no-cache)
- Running the project using Docker: docker compose up (to avoid cache issues: docker compose up --force-recreate)
 
## Setup
Before running the project, you need to create a `.env` file in the root directory of the project ("shipment_monitoring")

### Example of `.env` file
Create a `.env` file with the following variables:
MAIL_USERNAME=your_email@example.com 
MAIL_PASSWORD=your_email_password 
MAIL_FROM=your_email@example.com 
MAIL_PORT=587 
MAIL_SERVER=smtp.gmail.com