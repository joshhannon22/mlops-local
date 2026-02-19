# scripts/train.py
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"

mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("iris-classifier")

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

params = {"n_estimators": 100, "max_depth": 3}

with mlflow.start_run():
    mlflow.log_params(params)
    
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Accuracy: {accuracy:.4f}")
    print("Check MLflow UI at http://localhost:5001")