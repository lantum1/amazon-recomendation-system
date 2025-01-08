import grpc
from concurrent import futures
import ml_core_pb2
import ml_core_pb2_grpc
import pickle

class MLCoreService(ml_core_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        with open("/app/model/model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def Predict(self, request, context):
        user_id = request.user_id
        item_id = request.item_id
        
        prediction = self.model.predict(uid = user_id, iid = item_id, r_ui = None).est
        return ml_core_pb2.InferenceResponse(prediction=float(prediction))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ml_core_pb2_grpc.add_ModelServiceServicer_to_server(MLCoreService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("ML Core Service started on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
