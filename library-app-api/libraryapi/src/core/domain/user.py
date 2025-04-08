"""Module containing user-related domain models."""
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class UserIn(BaseModel):
    """Model representing the input data required for user creation."""
    name: str
    email: str
    password: str
    phone: str

class User(UserIn):
    """Model representing the user attributes, including database fields."""
    id: UUID

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class UserAuth(BaseModel):
    """Model used for user authentication."""
    email: str
    password: str
