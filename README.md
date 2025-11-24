# Shipment monitoring
A web-based application for tracking and managing courier shipments. This service allows users to monitor real-time status, track deliveries, and get detailed information about their shipments.
## Features
- Shipment list management
- Shipment status updates
- Nearest pickup location search
- Courier, sender, manager and recipient management
## Technology stack
- Python 3.12.7
- PostgreSQL 17.0
- FastApi
- Docker
- React
<img src="https://skillicons.dev/icons?i=python,postgres,fastapi,docker,react"/>

## Useful Commands
- Installing production dependencies: pip install -r requirements.txt
- Installing development dependencies: pip install -r requirements-dev.txt
- Starting the application server: uvicorn shipment-api.main:app --host 0.0.0.0 --port 8000
- API documentation (Swagger): http://localhost:8000/docs
- Building the project using Docker: docker compose build (to refresh the cache: docker compose build --no-cache)
- Running the project using Docker: docker compose up (to avoid cache issues: docker compose up --force-recreate)
- Running backend unit tests: pytest shipment-api/tests/unit/ (docker-compose exec app pytest tests/unit/ -v)
- Running backend tests with coverage: coverage run -m pytest
- Running backend integration tests: pytest shipment-api/tests/integration/ (docker-compose exec app pytest tests/integration/ -v)
- Running end-to-end tests with selenium: pytest e2e-tests/
- Generating a coverage report in the terminal: coverage report
- Generating an HTML coverage report: coverage html

## Frontend (React)
- Installing dependencies: npm install
- Starting the development server: npm start
