from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, List

class TrainRequest(BaseModel):
    model_config  = ConfigDict(protected_namespaces=())
    model_type: str
    hyperparameters: Dict[str, Any] = {}
    data: Dict[str, Any]

class PredictRequest(BaseModel):
    model_config  = ConfigDict(protected_namespaces=())
    model_id: str
    data: List[List[float]]

class DeleteRequest(BaseModel):
    model_config  = ConfigDict(protected_namespaces=())
    model_id: str