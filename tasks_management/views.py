from django.contrib.auth import authenticate
from django.http import JsonResponse
from .decorators import token_required
from .utils import generate_jwt
from .models import User, Project, Task
import json

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'id': user.id})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = generate_jwt(user)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def projects(request):
    if request.method == 'GET':
        projects = [
            {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'owner': project.owner.username
            } for project in request.user.projects.all()
        ]
        return JsonResponse(projects, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        owner = request.user
        end_date = data.get('end_date')
        if end_date:
            project = Project.objects.create(name=name, description=description, owner=owner, end_date=end_date)
        else:
            project = Project.objects.create(name=name, description=description, owner=owner)
        return JsonResponse({'id': project.id})
    return JsonResponse({'error': 'Invalid request method'}, status=405)