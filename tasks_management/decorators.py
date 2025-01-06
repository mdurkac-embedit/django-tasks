from django.http import JsonResponse
from functools import wraps
from .utils import decode_jwt
from .models import User

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_id = decode_jwt(token)
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    request.user = user
                    return view_func(request, *args, **kwargs)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'User does not exist'}, status=401)
        return JsonResponse({'error': 'Bearer token missing'}, status=401)
    return _wrapped_view
