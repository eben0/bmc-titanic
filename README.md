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

## Deploy
1. To deploy to Kubernetes cluster, you may use helm
```
 helm install bmc-titanic titanic-chart --namespace bmc
```
2. Check logs
```
~ kubectl -n bmc get pods
NAME                           READY   STATUS    RESTARTS   AGE
bmc-titanic-7565d87fcf-td572   1/1     Running   0          2m32s

~ kubectl -n bmc logs -f deploy/bmc-titanic
[2023-09-20 19:48:10 +0000] [7] [INFO] Starting gunicorn 21.2.0
[2023-09-20 19:48:10 +0000] [7] [INFO] Listening at: http://0.0.0.0:8080 (7)
[2023-09-20 19:48:10 +0000] [7] [INFO] Using worker: sync
[2023-09-20 19:48:10 +0000] [8] [INFO] Booting worker with pid: 8
20-09-2023 19:48:10 [INFO] importing into Sqlite from CSV /app/assets/titanic.csv
20-09-2023 19:48:10 [INFO] import finished
20-09-2023 19:48:10 [INFO] Titanic Leaving the dock...
20-09-2023 19:48:10 [INFO] Titanic is cruising now. Have fun.
10.1.0.1 - - [20/Sep/2023:19:48:10 +0000] "GET / HTTP/1.1" 200 56 "-" "kube-probe/1.27"
```

## APIs

| Endpoint             | Description      | Parameters  |
|----------------------|------------------|-------------|
| /                    | Home             |             |
| /api/swagger         | Swagger config   |             |
| /api/docs            | Swagger UI       |             |
| /api/prices          | Prices quantiles | quantiles   |
| /api/passengers      | List passengers  | limit, cols |
| /api/passengers/{id} | List a passenger | cols        |
