from datetime import date
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class CardCreate(BaseModel):
    first_6digits: str
    last_4digits: str
    issuer: str
    country: str
    type: str
    token: str
    expiry: str