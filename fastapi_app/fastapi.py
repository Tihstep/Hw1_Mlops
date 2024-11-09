from fastapi import FastAPI, HTTPException
from api.pydantic import TrainRequest, PredictRequest, DeleteRequest

app = FastAPI()

@app.get("/models")
def show_models():
    return list_models()

@app.post("/train")
def train_model_endpoint(request: TrainRequest):
    model_id = train_model(request.model_type, request.hyperparameters)
    return {"model_id": model_id}

@app.post("/predict")
def predict_endpoint(request: PredictRequest):
    predictions = predict(request.model_id, request.data)
    return {"predictions": predictions}

@app.delete("/delete")
def delete_model_endpoint(request: : DeleteRequest):
    pass

@app.get("/status")
def health_check():
    return {"status": "All is OK! Server fill himself good!"}