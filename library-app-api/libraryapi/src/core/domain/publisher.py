"""Module containing publisher-related domain models."""
from pydantic import BaseModel, ConfigDict, UUID4

class PublisherIn(BaseModel):
    """Model representing the input data for creating or updating a publisher."""
    company_name: str
    contact_email: str

class PublisherBroker(PublisherIn):
    """Broker class extending PublisherIn to include a user_id."""
    user_id: UUID4

class Publisher(PublisherBroker):
    """Model representing a publisher in the database, including its unique ID."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")