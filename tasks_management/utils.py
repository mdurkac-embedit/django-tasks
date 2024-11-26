import jwt
from django.conf import settings
from datetime import datetime

def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
        'iat': datetime.now()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except Exception:
        return None
