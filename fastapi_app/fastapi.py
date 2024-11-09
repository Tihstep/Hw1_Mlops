from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/models")
def get_model_types():
    pass

@app.post("/train")
def train_model_endpoint(request):
    pass

@app.post("/predict")
def predict_endpoint(request):
    pass

@app.get("/status")
def health_check():
    pass

