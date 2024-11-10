from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any

models = {}


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
    model_id = hash(model_type + str(hyperparameters.items()))
    if model_type == "logistic_regression":
        model = LogisticRegression(**hyperparameters)
    elif model_type == "random_forest":
        model = RandomForestClassifier(**hyperparameters)
    else:
        raise ValueError("Wrong unsupported model type")

    target = data['target']
    train_data = data['train_data']


    model.fit(train_data, target)
    models[model_id] = model
    return model_id

def predict(model_id: str, data: list):
    """
    Make a prediction using a model_id model
    
        Parameters
        ----------
        model_id : `str`
            Which type of model will be used for prediction.
        data: `Dict[str, Any]`
            Train_data and target_data for training of model.

        Returns
        -------
        prediction : `list`
            Result of model usage for data.
    """
    model = models.get(model_id)
    if not model:
        raise ValueError("Model not found")
    return model.predict(data).tolist()

def delete_model(model_id: str):
    """Delete a model_id model."""
    if model_id in models:
        del models[model_id]
        return True
    return False

def list_models():
    """List all available models"""
    return ["logreg_with_regularization", 
            "logreg_without_regularization"]

