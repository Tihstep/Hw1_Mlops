from sklearn.linear_model import LogisticRegression
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
    if model_type == "logreg_with_regularization":
        model = LogisticRegression(**hyperparameters)
    elif model_type == "logreg_without_regularization":
        model = LogisticRegression(**hyperparameters)
    else:
        raise ValueError("Wrong unsupported model type")

    target = data['target']
    train_data = data['train_data']


    model.fit(train_data, target)
    models[model_type] = model
    return model_type

def predict(model_type: str, data: list):
    """
    Make a prediction using a model_type model
    
        Parameters
        ----------
        model_type : `str`
            Which type of model will be used for prediction.
        data: `Dict[str, Any]`
            Train_data and target_data for training of model.

        Returns
        -------
        prediction : `list`
            Result of model usage for data.
    """
    model = models.get(model_type)
    if not model:
        raise ValueError("Model not found")
    return model.predict(data).tolist()

def delete_model(model_type: str):
    """Delete a model_type model."""
    if model_type in models:
        del models[model_type]
        return True
    return False

def list_models():
    """List all available models"""
    return ["logreg_with_regularization", 
            "logreg_without_regularization"]

