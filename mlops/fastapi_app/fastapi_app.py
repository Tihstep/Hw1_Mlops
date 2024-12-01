from fastapi import FastAPI, HTTPException, Depends
from mlops.model_framework import train_model, predict, delete_model, list_models
from mlops.fastapi_app.pydantic import TrainRequest, PredictRequest, DeleteRequest, TokenRequest
from mlops.auth import create_access_token, verify_token, oauth2_scheme

import logging
from datetime import timedelta
import psutil

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = {  "vertica" : {
        "username": "vertica", # os.environ.get("USERNAME"),
        "password": "vertica" #os.environ.get("PASSWORD")}
        }
}

def authenticate_user(username: str, password: str):
    user = db.get(username)
    if not user or user["password"] != password:
        return False
    return user

@app.post("/token")
def login(request: TokenRequest):
    user = authenticate_user(request.username, request.password)
    print(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/models")
def show_models():
    logger.info("Запрос на получение списка доступных моделей")
    return list_models()

@app.post("/train")
def train_model_endpoint(request: TrainRequest, token: str = Depends(oauth2_scheme)):
    """
    API триггерит обучение определенной модели на переданных данных
    с определенными гиперпараметрами. Возвращает id модели.
    """
    verify_token(token)
    logger.info("Получен запрос на обучение модели: %s", request.model_type)
    try:
        model_id = train_model(request.model_type,
                               request.hyperparameters,
                               request.data
                               )
        logger.info("Модель %s успешно обучена с гиперпараметрами: %s", model_id, request.hyperparameters)
        return {"model_id": model_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict")
def predict_endpoint(request: PredictRequest, token: str = Depends(oauth2_scheme)):
    """API триггерит инференс определенной модели на переданных данных."""
    logger.info("Получен запрос на предсказание для модели: %s", request.model_id)
    try:
        predictions = predict(request.model_id, request.data)
        logger.info("Предсказание для модели %s успешно выполнено", request.model_id)
        return {"predictions": predictions}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/delete")
def delete_model_endpoint(request: DeleteRequest, token: str = Depends(oauth2_scheme)):
    """API удаляет модель из model registry(dict)"""
    logger.info("Получен запрос на удаление модели: %s", request.model_id)
    if delete_model(request.model_id):
        logger.info("Модель %s успешно удалена", request.model_id)
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Sorry, model not found!")

@app.get("/status")
def health_check():
    """API check if servise is available."""
    logger.info("Запрос проверки статуса сервиса")

    cpu_usage = psutil.cpu_percent(interval=1)
    
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    return {"status": f"""All is OK! Server fill himself good! 
                        CPU Usage: {cpu_usage}% 
                        Memory Usage: {memory_usage}% 
                        Disk Usage: {disk_usage}%
                        """
                }

