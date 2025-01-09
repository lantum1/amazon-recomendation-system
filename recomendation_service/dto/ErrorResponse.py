from pydantic import BaseModel

class ErrorResponse(BaseModel):
    code: int
    description: str