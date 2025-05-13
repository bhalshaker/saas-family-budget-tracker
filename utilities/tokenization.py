from datetime import datetime, timedelta,timezone  # New import for timestamps
import jwt  # New import for token generation
import uuid
from config import config

def generate_token(id:uuid):
        """
        Generates a JSON Web Token (JWT) for a given user ID.
        Args:
            id (uuid): The unique identifier of the user for whom the token is generated.
        Returns:
            str: The encoded JWT token as a string.
        The token includes the following claims:
            - exp: Expiration time (1 day from now)
            - iat: Issued at time (current time)
            - sub: Subject (user ID)
        """
        
        # Define the payload
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(id),
        }

        # Create the JWT token
        token = jwt.encode(payload, config.token_secret, algorithm="HS256")

        return token

def decode_token(token)->str:
        """
        Decodes a JWT token and retrieves the subject ("sub") claim.
        Args:
            token: An object containing the JWT credentials as an attribute.
        Returns:
            str: The subject ("sub") claim from the decoded JWT payload.
        """
        
        payload = jwt.decode(token.credentials, config.token_secret, algorithms=["HS256"])
        return payload.get("sub")