from pydantic import BaseModel
from typing import Dict, Any, List

class TrainRequest(BaseModel):
    model_type: str
    hyperparameters: Dict[str, Any] = {}

class PredictRequest(BaseModel):
    model_id: str
    data: List[List[float]]

class DeleteRequest(BaseModel):
    model_id: str