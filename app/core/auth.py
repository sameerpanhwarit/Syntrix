
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import SECRET_KEY, ALGORITHM


def create_access_token(user_id: str):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token