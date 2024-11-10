from fastapi import FastAPI, HTTPException
from .models import train_model, predict, delete_model, list_models
from .pydantic import TrainRequest, PredictRequest, DeleteRequest

app = FastAPI()

@app.get("/models")
def show_models():
    return list_models()

@app.post("/train")
def train_model_endpoint(request: TrainRequest):
    """
    API trigger model training for specified model type on
    transferred data with given hyperparametes. Return id of model.
    """
    try:
        model_id = train_model(request.model_type,
                               request.hyperparameters,
                               request.data
                               )
        return {"model_id": model_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict")
def predict_endpoint(request: PredictRequest):
    """API trigger inference for specified model type transferred data."""
    try:
        predictions = predict(request.model_id, request.data)
        return {"predictions": predictions}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/delete")
def delete_model_endpoint(request: : DeleteRequest):
    """API delete model from model registry(dict)"""
    if delete_model(request.model_id):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Sorry, model not found!")

@app.get("/status")
"""API check if servise is available."""
def health_check():
    return {"status": "All is OK! Server fill himself good!"}

