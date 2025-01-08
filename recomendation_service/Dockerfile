FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir grpcio grpcio-tools fastapi uvicorn pydantic

WORKDIR /app

COPY . /app

RUN python -m grpc_tools.protoc \
    -I./proto \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/ml_core.proto

EXPOSE 8080

CMD ["python", "main.py"]
