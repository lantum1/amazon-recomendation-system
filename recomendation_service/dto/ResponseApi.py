from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel
from dto.ErrorResponse import ErrorResponse

T = TypeVar("T")

class ResponseApi(GenericModel, Generic[T]):
    data: Optional[T]
    error: Optional[ErrorResponse]
