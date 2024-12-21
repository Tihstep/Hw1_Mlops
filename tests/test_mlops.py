import pytest
from mlops.model_framework import train_model
from mlops.minio_uploader import Minio_client

# Standard Test: Testing model training with valid data
def test_train_model_valid_data():
    # Prepare test data
    model_type = "logistic_regression"
    hyperparameters = {"C": 1.0, "max_iter": 100}
    data = {
        "train_data": [[0.1, 0.2], [0.2, 0.3], [0.4, 0.5]],
        "target": [0, 1, 1],
    }

    # Call train_model
    model_id = train_model(model_type, hyperparameters, data)

    # Assert model_id is returned
    assert model_id is not None, "Model ID should not be None"
    assert isinstance(model_id, int), "Model ID should be an integer"


def test_minio_upload_mock(monkeypatch):
    # Mock the MinIO client upload_to_minio method
    def mock_upload_to_minio(self, data, filename):
        return f"s3://mock_bucket/{filename}"

    # Apply the mock
    monkeypatch.setattr(Minio_client, "upload_to_minio", mock_upload_to_minio)

    # Simulate uploading data
    minio_client = Minio_client()
    test_data = {"key": "value"}
    filename = "test_file.json"
    upload_path = minio_client.upload_to_minio(test_data, filename)

    # Assert the mocked method is called correctly
    assert upload_path == "s3://mock_bucket/test_file.json", "Upload path should match the mocked return value"