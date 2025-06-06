from datetime import datetime, timedelta,timezone  # New import for timestamps
import jwt  # New import for token generation
import uuid
from config import config

def generate_token(id:str)->dict:
        """
        Generates a JSON Web Token (JWT) for a given user ID.
        Args:
            id (uuid): The unique identifier of the user for whom the token is generated.
        Returns:
            str: The encoded JWT token as a string.
        The token includes the following claims:
            - expires_at: Expiration time (1 day from now)
            - issued_at: Issued at time (current time)
            - subject: Subject (user ID)
        """
        
        payload = generate_token_payload(id)
        token = jwt.encode(payload, config.token_secret, algorithm="HS256")
        user_response={"expires_at":payload["exp"],
                       "issued_at":payload["iat"],
                       "apikey":token}
        return user_response

def decode_token(credentials:str)->str:
        """
        Decodes a JWT token and retrieves the subject ("sub") claim.
        Args:
            token: An object containing the JWT credentials as an attribute.
        Returns:
            str: The subject claim from the decoded JWT payload.
        """
        
        payload = jwt.decode(credentials, config.token_secret, algorithms=["HS256"])
        return payload.get("sub")

def generate_token_payload(id:uuid,expiration_time: int = 86400) -> dict:
    """
    Generates a token payload with an expiration time.
    Args:
        expiration_time (int): The expiration time in seconds. Default is 86400 seconds (1 day).
    Returns:
        dict: The token payload with the expiration time.
    """
    return {
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expiration_time),
        "iat": datetime.now(timezone.utc), # Issuance timestamp
        "sub": str(id)
    }