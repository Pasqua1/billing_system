# billing_system

## Deployment with Docker
You must have docker and docker-compose tools installed to work with material in this section. Then just run:
```
docker compose build
docker compose up
```

To generate migrations and update database run:
```
docker compose exec fastapi alembic revision --autogenerate -m "Added required tables"
docker compose exec fastapi alembic upgrade head
```

## Run tests
Tests for this project are defined in the tests/ folder.
To run all the tests of a project, simply run the pytest command:
```
docker compose exec fastapi pytest /usr/src/tests/
```
## Application will be available on localhost in your browser.

API port: 8808

PostgreSQL port: 5432

## Web routes
All routes are available on /docs.
