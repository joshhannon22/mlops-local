# mlops-local

A local MLOps development environment running on Kubernetes (kind) with MLflow for experiment tracking and MinIO for artifact storage.

## What This Does

This project sets up a complete local MLOps stack that lets you:

- **Run ML experiments** using MLflow for tracking parameters, metrics, and models
- **Store model artifacts** in MinIO (S3-compatible object storage)
- **Track experiments** through the MLflow UI
- **Train models locally** and log them to a centralized registry

### Current Architecture

- **Kubernetes Cluster**: Local cluster running via kind (Kubernetes in Docker)
- **MLflow**: Experiment tracking and model registry server (port 5001)
- **MinIO**: S3-compatible object storage for MLflow artifacts (port 9000)
- **Training Script**: Simple Iris classifier that demonstrates MLflow integration

## Prerequisites

- Docker Desktop (must be running)
- kubectl
- kind
- Python 3.12+
- pip

## Setup

### 1. Create the Kubernetes Cluster

kind create cluster --config cluster/kind-config.yaml --name mlops-local

### 2. Set Up Kubernetes Context

kubectl cluster-info --context kind-mlops-local

### 3. Deploy Infrastructure

# Create namespace
kubectl apply -f infra/namespace.yaml

# Deploy MinIO
kubectl apply -f infra/minio/deployment.yaml
kubectl apply -f infra/minio/service.yaml

# Deploy MLflow
kubectl apply -f infra/mlflow/deployment.yaml
kubectl apply -f infra/mlflow/service.yaml

### 4. Wait for Pods to be Ready

kubectl get pods -n mlops -w

### 5. Set Up Python Environment

python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

### 6. Port Forwarding (in separate terminals)

# Terminal 1: MLflow UI
kubectl port-forward -n mlops svc/mlflow 5001:5000

# Terminal 2: MinIO Console (optional, for browsing artifacts)
kubectl port-forward -n mlops svc/minio 9001:9001
```

**Note**: If port 5000 is in use (common on macOS due to AirPlay Receiver), either disable AirPlay Receiver in System Settings or the config uses port 5001 for MLflow.

## Usage

### Run Training Script

```bash
python scripts/train.py
```

This will:
1. Load the Iris dataset
2. Train a RandomForest classifier
3. Log parameters, metrics, and the model to MLflow
4. Store model artifacts in MinIO

### Access MLflow UI

Open your browser to: http://localhost:5001

You'll see:
- Experiments and runs
- Parameters and metrics
- Logged models
- Model artifacts stored in MinIO

### Access MinIO Console (Optional)

Open your browser to: http://localhost:9001

- Username: `minioadmin`
- Password: `minioadmin`

## Project Structure

```
mlops-local/
├── cluster/
│   └── kind-config.yaml      # Kind cluster configuration
├── infra/
│   ├── namespace.yaml        # Kubernetes namespace
│   ├── minio/
│   │   ├── deployment.yaml   # MinIO deployment
│   │   └── service.yaml      # MinIO service
│   └── mlflow/
│       ├── deployment.yaml   # MLflow deployment
│       └── service.yaml      # MLflow service
├── scripts/
│   └── train.py              # Training script with MLflow integration
├── requirements.txt          # Python dependencies
└── README.md
```

## Cleanup

To tear down the cluster:

```bash
kind delete cluster --name mlops-local
```

## What You're Building Next

Here's the progression, each phase building on the last:

### Phase 2 — Kubeflow Pipelines

Right now you run that training script manually from your terminal. The next step is turning it into a Kubeflow Pipeline so it runs inside the cluster as a proper workflow. You'll define each step — data prep, training, evaluation, model registration — as its own container. This teaches you pipeline orchestration, which is a core MLOps skill.

### Phase 3 — Automated Model Promotion

After Kubeflow is running your pipeline, you'll add logic that compares the new model's accuracy against the currently deployed model. Only if the new model beats the baseline does it get promoted to the model registry in MLflow. This is automated validation — removing humans from the go/no-go decision.

### Phase 4 — Model Serving with KServe

Once a model is promoted in the registry, KServe picks it up and exposes it as an HTTP prediction endpoint running inside your cluster. You'll be able to send it a request and get a prediction back. This is the "serving in production" part.

### Phase 5 — Drift Detection with Evidently

This is where it gets really interesting. You'll deploy Evidently AI alongside your model. It watches the data coming into your model and the predictions going out, and compares them against your original training data. When patterns shift, it flags drift. You'll write a small script that simulates drift so you can see it trigger.

### Phase 6 — The Closed Loop

The final piece connects everything. When Evidently detects drift above a threshold, Prometheus fires an alert that automatically triggers a new Kubeflow pipeline run to retrain the model on fresh data. The system heals itself. This is the project in its complete form.

Start on Phase 2 whenever you're ready and I'll walk you through it the same way — directory structure, manifests, and a clear explanation of what everything is doing.