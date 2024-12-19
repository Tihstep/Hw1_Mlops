import grpc
from mlops.grpc_app import message_interface_pb2 as pb2
from mlops.grpc_app import message_interface_pb2_grpc as pb2_grpc

def grpc_client():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.ModelServiceStub(channel)
        
        model_id = train_model(stub)
        
        make_prediction(stub, model_id)
        
        delete_model(stub, model_id)

def train_model(stub):
    hyperparameters = {"criterion": "gini"}

    # Define train data and target in the required format
    target = [3.0, 7.0, 11.0]
    train_data = [
        pb2.TrainData(features=[1.0, 2.0]),
        pb2.TrainData(features=[3.0, 4.0]),
        pb2.TrainData(features=[5.0, 6.0])
    ]

    request = pb2.TrainRequest(
        model_type="random_forest",
        hyperparameters=hyperparameters,
        target=target,
        train_data=train_data
    )
    
    response = stub.TrainModel(request)
    print(f"Trained model ID: {response.model_id}")
    return response.model_id

def make_prediction(stub, model_id):
    prediction_data = [7.0, 8.0]  # Modify this to match the expected float list format
    
    request = pb2.PredictRequest(
        model_id=model_id,
        data=prediction_data
    )
    
    response = stub.Predict(request)
    print(f"Prediction: {response.predictions}")

def delete_model(stub, model_id):
    request = pb2.DeleteRequest(
        model_id=model_id
    )
    
    response = stub.DeleteModel(request)
    print(f"Model deleted: {response.success}")

if __name__ == "__main__":
    grpc_client()
