
from fastapi import FastAPI, HTTPException
from mlops.fastapi_app.model_framework import train_model, predict, delete_model, list_models
from mlops.fastapi_app.pydantic import TrainRequest, PredictRequest, DeleteRequest
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.get("/models")
def show_models():
    logger.info("Запрос на получение списка доступных моделей")
    return list_models()

@app.post("/train")
def train_model_endpoint(request: TrainRequest):
    """
    API trigger model training for specified model type on
    transferred data with given hyperparametes. Return id of model.
    """
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
def predict_endpoint(request: PredictRequest):
    """API trigger inference for specified model type transferred data."""
    logger.info("Получен запрос на предсказание для модели: %s", request.model_id)
    try:
        predictions = predict(request.model_id, request.data)
        logger.info("Предсказание для модели %s успешно выполнено", request.model_id)
        return {"predictions": predictions}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/delete")
def delete_model_endpoint(request: DeleteRequest):
    """API delete model from model registry(dict)"""
    logger.info("Получен запрос на удаление модели: %s", request.model_id)
    if delete_model(request.model_id):
        logger.info("Модель %s успешно удалена", request.model_id)
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Sorry, model not found!")

@app.get("/status")
def health_check():
    """API check if servise is available."""
    logger.info("Запрос проверки статуса сервиса")
    return {"status": "All is OK! Server fill himself good!"}

