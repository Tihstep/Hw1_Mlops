import grpc
from concurrent import futures
from mlops.fastapi_app.model_framework import train_model, predict, delete_model
from mlops.grpc_app import message_interface_pb2 as pb2
from mlops.grpc_app import message_interface_pb2_grpc as pb2_grpc


class ModelService(pb2_grpc.ModelServiceServicer):
    def TrainModel(self, request, context):
        data = {
            "target": list(request.target),
            "train_data": [list(sample.features) for sample in request.train_data]
        }
        model_id = train_model(request.model_type, request.hyperparameters, data)
        print(model_id)
        return pb2.TrainResponse(model_id=str(model_id))

    def Predict(self, request, context):
        predictions = predict(request.model_id, [request.data])
        return pb2.PredictResponse(predictions=predictions)

    def DeleteModel(self, request, context):
        success = delete_model(request.model_id)
        return pb2.DeleteResponse(success=success)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ModelServiceServicer_to_server(ModelService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
