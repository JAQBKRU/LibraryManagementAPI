"""A DTO model for user details."""
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4


class UserDTO(BaseModel):
    """A model representing DTO for user data."""
    id: UUID4
    name: str
    email: str
    phone: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "UserDTO":
        """A method for creating a UserDTO instance from a database record.

        Args:
            record (Record): The database record containing user details.

        Returns:
            UserDTO: An instance of the UserDTO with populated fields.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            email=record_dict.get("email"),  # type: ignore
            phone=record_dict.get("phone"),  # type: ignore
        )