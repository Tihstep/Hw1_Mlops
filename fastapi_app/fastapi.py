from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/models")
def get_model_types():
    return list_models()

@app.post("/train")
def train_model_endpoint(request):
    model_id = train_model(request.model_type, request.hyperparameters)
    return {"model_id": model_id}

@app.post("/predict")
def predict_endpoint(request):
    predictions = predict(request.model_id, request.data)
    return {"predictions": predictions}

@app.get("/status")
def health_check():
    return {"status": "All is OK! Server fill himself good!"}
