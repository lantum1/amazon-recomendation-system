import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from dto.ErrorResponse import ErrorResponse
from dto.ResponseApi import ResponseApi
from dto.GetProductRatingResponse import GetProductRatingResponse
import grpc
import ml_core_pb2
import ml_core_pb2_grpc

app = FastAPI()

@app.get("/recomendation-service/v1.0/get-product-rating/", response_model=ResponseApi[GetProductRatingResponse])
def get_product_rating(user_id: str, product_id: str) -> ResponseApi[GetProductRatingResponse]:
    try:
        if not user_id.strip():
            raise HTTPException(status_code=400, detail="user_id не может быть пустым.")
        if not product_id.strip():
            raise HTTPException(status_code=400, detail="product_id не может быть пустым.")

        with grpc.insecure_channel("ml-core-service:50051") as channel:
            stub = ml_core_pb2_grpc.ModelServiceStub(channel)
            request = ml_core_pb2.InferenceRequest(user_id=user_id, item_id=product_id)
            response = stub.Predict(request)

            return ResponseApi(
                data=GetProductRatingResponse(productRating=response.prediction),
                error=None
            )
    except grpc.RpcError as e:
         return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseApi(
                data=None,
                error=ErrorResponse(
                    code=500,
                    description=f"Ошибка при подключении к gRPC: {e.details() or 'Неизвестная ошибка'}"
                )
            ).dict()
        )
    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code,
            content=ResponseApi(
                data=None,
                error=ErrorResponse(
                    code=http_exc.status_code,
                    description=http_exc.detail
                )
            ).dict()
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseApi(
                data=None,
                error=ErrorResponse(
                    code=500,
                    description=f"Неожиданная ошибка: {str(e)}"
                )
            ).dict()
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
