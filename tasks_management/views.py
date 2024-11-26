from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.db.utils import IntegrityError
from .decorators import token_required
from .utils import generate_jwt
from .models import User, Project, Task
import json

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'id': user.id}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        user = authenticate(username=username, password=password)
        if user is not None:
            token = generate_jwt(user)
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def projects(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        if name:
            projects =  request.user.projects.filter(name__icontains=name)
        else:
            projects = request.user.projects.all()     
        projects_dto = [
            {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'owner': project.owner.username
            } for project in projects
        ]
        return JsonResponse(projects_dto, safe=False, status=200)
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        owner = request.user
        end_date = data.get('end_date')
        try:
            if end_date:
                project = Project.objects.create(name=name, description=description, owner=owner, end_date=end_date)
            else:
                project = Project.objects.create(name=name, description=description, owner=owner)
            return JsonResponse({'id': project.id}, status=200)
        except IntegrityError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def project(request, project_id):
    try:
        project = request.user.projects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    if request.method == 'GET':
        project_dto = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date,
            'end_date': project.end_date,
            'owner': project.owner.username
        }
        return JsonResponse(project_dto, safe=False, status=200)
    if request.method == 'DELETE':
        project.delete()
        return JsonResponse({'message': 'Project deleted'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def project_tasks(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    if request.method == 'GET':
        if request.user == project.owner:
            tasks = project.tasks.all()
        else:
            tasks = project.tasks.filter(assigned_to=request.user)
        tasks = [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_date': task.created_date,
                'created_by': task.created_by.username,
                'due_date': task.due_date,
                'completed': task.completed,
                'assigned_to': task.assigned_to.username if task.assigned_to else None
            } for task in tasks
        ]
        return JsonResponse(tasks, safe=False, status=200)
    if request.method == 'POST':
        if request.user != project.owner:
            return JsonResponse({'error': 'You are not allowed to create tasks in this project'}, status=403)
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        created_by = request.user
        due_date = data.get('due_date')
        completed = False
        assigned_to = data.get('assigned_to')
        if assigned_to:
            assigned_to = User.objects.get(id=assigned_to)
        else:
            assigned_to = request.user
        try:
            task = Task.objects.create(title=title, description=description, created_by=created_by, due_date=due_date, completed=completed, project=project, assigned_to=assigned_to)
        except IntegrityError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        return JsonResponse({'id': task.id}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def tasks(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    if request.user != task.project.owner and request.user != task.assigned_to:
            return JsonResponse({'error': 'You are not allowed to access this task'}, status=403)
    if request.method == 'GET':
        task_dto = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_date': task.created_date,
            'created_by': task.created_by.username,
            'due_date': task.due_date,
            'completed': task.completed,
            'assigned_to': task.assigned_to.username if task.assigned_to else None
        }
        return JsonResponse(task_dto, safe=False, status=200)
    if request.method == 'PUT':
        task.completed = True
        task.save()
        return JsonResponse({'message': 'Task completed'}, status=200)
    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
