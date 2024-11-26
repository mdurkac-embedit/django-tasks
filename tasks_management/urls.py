from django.urls import path
from . import views

app_name = 'tasks_management'

urlpatterns = [
    path('api/login', views.login_view, name='login'),
    path('api/register', views.register_view, name='register'),
    path('api/projects', views.projects, name='projects'),
    path('api/projects/<int:project_id>', views.project, name='project'),
    path('api/projects/<int:project_id>/tasks', views.project_tasks, name='tasks'),
    path('api/tasks/<int:task_id>', views.tasks, name='task'),
]