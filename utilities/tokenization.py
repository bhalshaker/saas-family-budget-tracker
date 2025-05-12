from datetime import datetime, timedelta,timezone  # New import for timestamps
import jwt  # New import for token generation
import uuid
from config import config

def generate_token(id:uuid):
        # Define the payload
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),  # Expiration time (1 day)
            "iat": datetime.now(timezone.utc),  # Issued at time
            "sub": str(id),  # Subject - the user ID
        }

        # Create the JWT token
        token = jwt.encode(payload, config.token_secret, algorithm="HS256")

        return token