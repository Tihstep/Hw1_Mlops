import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any, List
import logging
import json
import pickle
from mlops.model_collector import ModelCollector
from mlops.minio_uploader import Minio_client

minio_uploader = Minio_client()
model_collector = ModelCollector(minio_uploader.minio_client, 'models')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def train_model(model_type: str, hyperparameters: Dict[str, Any], data: Dict[str, Any]):
    """
    Train a model and store it in the models dictionary.

        Parameters
        ----------
        model_type : `str`
            Which type of model will be trained.
        hyperparameters: Dict[str, Any] : `Dict[str, Any]`
            Human setting parameters needed to learn model.
        data: `Dict[str, Any]`  
            Train_data and target_data for training of model.

        Returns
        -------
        model_type : `str`
            Name of model type
    """


    model_functions = {
        "logistic_regression": LogisticRegression,
        "decision_tree": RandomForestClassifier
    }

    if model_type in model_functions:
        model = model_functions[model_type](**hyperparameters)
    else:
        raise ValueError("Wrong unsupported model type")

    target = data['target']
    train_data = data['train_data']

    model.fit(train_data, target)

    # Определяем уникальный ключ
    model_spec = model_type + str(hyperparameters.items())
    serialized_data = json.dumps(data, sort_keys=True)
    model_id = hash(serialized_data + model_spec)

    # Версионируем данные в dvc
    minio_path = minio_uploader.upload_to_minio(data, f"{model_spec}_train_data.json")

    # Сохраняем модель в s3
    os.makedirs(f"./models/", exist_ok=True)
    with open(f'./models/model_{model_id}.pkl','wb') as f:
        pickle.dump(model,f)
    model_collector.add_model(model_id=str(model_id), model_path=f'./models/model_{model_id}.pkl')

    return model_id

def predict(model_id: str, data: List[List[float]]):
    """
    Make a prediction using a model_id model
    
        Parameters
        ----------
        model_id : `str`
            Which type of model will be used for prediction.
        data: `List[List[float]]`
            Train_data and target_data for training of model.

        Returns
        -------
        prediction : `list`
            Result of model usage for data.
    """
    os.makedirs(f"./models", exist_ok=True)

    # Берем модель из s3
    model_path = model_collector.get_model(
                                model_id=model_id, 
                                model_path=f'./models/model_{model_id}.pkl'
                                        )

    with open(model_path,'rb') as f:
        model = pickle.load(f)

    if not model:
        raise ValueError("Model not found")
    return model.predict(data).tolist()

def delete_model(model_id: str):
    """Delete a model_id model."""
    if model_id not in model_collector.models:
        raise ValueError(f"Model with ID {model_id} does not exist.")

    #model_collector.delete_model(model_id)
    local_model_path = f"./models/model_{model_id}.pkl"

    if os.path.exists(local_model_path):
        os.remove(local_model_path)
        logger.info(f"Local file {local_model_path} deleted.")
    del model_collector.models[model_id]
    logger.info(f"Model {model_id} removed from ModelCollector.")

def list_models():
    """List all available models"""
    if len(model_collector.models) == 0:
        return "System does not have any trained models"
    return list(map(str, list(model_collector.models.keys())))