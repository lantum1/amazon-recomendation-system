from pydantic import BaseModel

class GetProductRatingResponse(BaseModel):
    productRating: float
