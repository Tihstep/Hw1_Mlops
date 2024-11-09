from sklearn.linear_model import LogisticRegression

models = {}

def train_model(model_type, hyperparameters, data):
    if model_type == "logreg_with_regularization":
        model = LogisticRegression(**hyperparameters)
    elif model_type == "logreg_without_regularization":
        model = LogisticRegression(**hyperparameters)

    model.fit(X, y)
    models[model_type] = model
    return model_type

def predict(model_type, data):
    model = models.get(model_type)
    return model.predict(data).tolist()

def delete_model(model_type):
    if model_type in models:
        del models[model_type]
        return True
    return False

def list_models():
    return ["logreg_with_regularization", 
            "logreg_without_regularization"]
