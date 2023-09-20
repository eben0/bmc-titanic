# BMC Titanic home assigment

This is Python Flask app that serves the Titanic api

## Prerequisites
1. Python3 (3.9+ is recommended)
2. Boarding ticket to the Titanic 
3. Docker (optional)

## Run the app locally
1. Create virtual env
```
python -m venv venv
source ./venv/bin/activate # (Linux & Mac)
```
1. Install dependencies
```
pip install -r src/requirements
```
2. Run the app
```
cd src/
python main.py
```
3. Open the browser at http://127.0.0.1:8080/api/docs

## Run with Docker Compose
1. Build and run
```
docker compose up --build
```
2. Open the browser at http://127.0.0.1:8080/api/docs

## APIs

| Endpoint             | Description      | Parameters  |
|----------------------|------------------|-------------|
| /                    | Home             |             |
| /api/swagger         | Swagger config   |             |
| /api/docs            | Swagger UI       |             |
| /api/prices          | Prices quantiles | quantiles   |
| /api/passengers      | List passengers  | limit, cols |
| /api/passengers/{id} | List a passenger | cols        |
