from sklearn.linear_model import LogisticRegression
from typing import Dict, Any

models = {}

def train_model(model_type: str, hyperparameters: Dict[str, Any], data: list):
    if model_type == "logreg_with_regularization":
        model = LogisticRegression(**hyperparameters)
    elif model_type == "logreg_without_regularization":
        model = LogisticRegression(**hyperparameters)
    else:
        raise ValueError("Wrong unsupported model type")

    #train_data, target = split(data)

    model.fit(train_data, target)
    models[model_type] = model
    return model_type

def predict(model_id: str, data: list):
    model = models.get(model_type)
    return model.predict(data).tolist()

def delete_model(model_id: str):
    if model_type in models:
        del models[model_type]
        return True
    return False

def list_models():
    return ["logreg_with_regularization", 
            "logreg_without_regularization"]

            