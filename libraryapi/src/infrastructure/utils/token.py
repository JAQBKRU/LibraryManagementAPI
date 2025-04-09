"""A module containing helper functions for token generation."""
from datetime import datetime, timedelta, timezone

from jose import jwt
from pydantic import UUID4

from src.infrastructure.utils.consts import (
    EXPIRATION_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)

# my
def fix_jwt_padding(token: str) -> str:
    """Fixes JWT padding by ensuring the token has the correct base64 padding.

    Args:
        token (str): The JWT token string that may need padding.

    Returns:
        str: The padded JWT token.
    """
    padding_needed = len(token) % 4
    if padding_needed:
        token += "=" * (4 - padding_needed)
    return token


def generate_user_token(user_uuid: UUID4) -> dict:
    """A function returning JWT token for user.

    Args:
        user_uuid (UUID5): The UUID of the user.

    Returns:
        dict: The token details.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    jwt_data = {"sub": str(user_uuid), "exp": expire, "type": "confirmation"}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt = fix_jwt_padding(encoded_jwt) # my

    return {"user_token": encoded_jwt, "expires": expire}