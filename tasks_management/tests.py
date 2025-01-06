from django.test import TestCase
import time, unittest, datetime
from django.test import Client
from .models import User, Project, Task
from django.urls import reverse

class RestApiTest(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        # Vymažeme všechny záznamy z tabulek v databázi
        Project.objects.all().delete()
        User.objects.all().delete()
        Task.objects.all().delete()

    def test_post_login(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        response = self.client.post(reverse('tasks_management:login'),data={
            "username": "KacKac",
            "password": "Hroch2"   
        }, content_type="application/json")
        login = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(login["token"])

    def test_post_login_not_name_pass(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        response = self.client.post(reverse('tasks_management:login'),data={
            "username": "KacKac",   
        }, content_type="application/json")
        login = response.json()
        self.assertEqual(login["error"], "Invalid data")
        self.assertEqual(response.status_code, 400)

    def test_post_login_credentials(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        response = self.client.post(reverse('tasks_management:login'),data={
            "username": "KacKac",  
            "password": "Hroch22"  
        }, content_type="application/json")
        login = response.json()
        self.assertEqual(login["error"], "Invalid credentials")
        self.assertEqual(response.status_code, 400)
        
    def test_post_login_invalid_request_method(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        response = self.client.put(reverse('tasks_management:login'),data={
            "username": "KacKac",  
            "password": "Hroch2"  
        }, content_type="application/json")
        login = response.json()
        self.assertEqual(login["error"], "Invalid request method")
        self.assertEqual(response.status_code, 405)
    
    def test_register(self):
        response = self.client.post(reverse('tasks_management:register'),data={
            "username": "KacKac",
            "password": "Hroch2"   
        }, content_type="application/json")
        register = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(register["id"])
        register_databaze = User.objects.get(id=register["id"])
        self.assertEqual(register_databaze.username, "KacKac")
        response = self.client.post(reverse('tasks_management:login'),data={
            "username": "KacKac",
            "password": "Hroch2"   
        }, content_type="application/json")
        login = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(login["token"])
    
    def test_post_register_not_name_pass(self):
        response = self.client.post(reverse('tasks_management:register'),data={
            "username": "KacKac",   
        }, content_type="application/json")
        register = response.json()
        self.assertEqual(register["error"], "Invalid data")
        self.assertEqual(response.status_code, 400)

    def test_post_register_invalid_request_method(self):
        response = self.client.put(reverse('tasks_management:register'),data={
            "username": "KacKac",  
            "password": "Hroch2"  
        }, content_type="application/json")
        register = response.json()
        self.assertEqual(register["error"], "Invalid request method")
        self.assertEqual(response.status_code, 405)
    
    def test_user_exist(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        response = self.client.post(reverse('tasks_management:register'),data={
            "username": "KacKac",
            "password": "Hroch2"   
        }, content_type="application/json")
        register = response.json()
        self.assertEqual(register["error"], "User already exists")
        self.assertEqual(response.status_code, 400)

    def get_auth_token(self, username="KacKac", password="Hroch2"):
        response = self.client.post(reverse('tasks_management:login'), data={
            "username": username,
            "password": password
        }, content_type="application/json")
        return response.json().get("token")

    def test_post_3b_Create_projects(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.post(reverse('tasks_management:projects'), 
            data =  {
            "name":"Liska", 
            "description":"LLL", 
            "end_date":"2025-01-01", 
            } , content_type="application/json", HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(project["id"])
        my_project = Project.objects.get(id=project["id"])
        self.assertEqual(my_project.name, "Liska")
        self.assertEqual(my_project.description, "LLL")
        self.assertEqual(my_project.end_date, datetime.date(2025, 1, 1))
        self.assertEqual(my_project.id, project["id"])
        self.assertEqual(my_project.owner.username, "KacKac")


    def test_post_3b_Create_projects_no_end_date(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.post(reverse('tasks_management:projects'), 
            data =  {
            "name":"Liska", 
            "description":"LLL",  
            } , content_type="application/json", HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(project["id"])
        my_project = Project.objects.get(id=project["id"])
        self.assertEqual(my_project.name, "Liska")
        self.assertEqual(my_project.description, "LLL")
        self.assertEqual(my_project.id, project["id"])
        self.assertEqual(my_project.owner.username, "KacKac")
    
    def test_post_3b_Create_projects_Invalid_data(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.post(reverse('tasks_management:projects'), 
            data =  {
            "description":"LLL",   
            } , content_type="application/json", HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(project["error"], "Invalid data")
    
    
    
    def test_post_3b_Create_projects_Invalid_request_method(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.put(reverse('tasks_management:projects'), 
            data =  {
            "name":"Liska",
            "description":"LLL",   
            } , content_type="application/json", HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 405)
        self.assertEqual(project["error"], "Invalid request method")

    def test_post_3b_Create_projects_no_token(self):
        response = self.client.post(reverse('tasks_management:projects'), 
            data =  {
            "description":"LLL",   
            } , content_type="application/json",
        )
        project = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(project["error"], "Bearer token missing")
    
    def test_get_3a_Create_projects_empty(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.get(reverse('tasks_management:projects'), 
         HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual (project, [])

    def test_get_3a_Create_projects_full(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project= Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.get(reverse('tasks_management:projects'), 
         HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(project), 1)
        slovnik = project[0]
        self.assertEqual (slovnik["name"], 'Liska')
        self.assertEqual (slovnik["description"], "LLL")
        self.assertEqual (slovnik["end_date"], "2025-01-01")
        self.assertEqual (slovnik["owner"], "KacKac")
        self.assertEqual (slovnik["start_date"], "2024-12-12")
    
    def test_get_3a_Create_projects_if(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        morce = User.objects.create_user(username='Morce', password='Morce3')
        project_1= Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project_1.save()
        project_2= Project (name= "Kocka", description= "MMM",end_date = "2025-02-02", owner = opice, start_date = datetime.date(2024, 1, 1))
        project_2.save()
        project_3= Project (name= "Pes", description= "PPP",end_date = "2025-10-01", owner = opice, start_date = datetime.date(2024, 11, 12))
        project_3.save()
        project_4= Project (name= "Pes", description= "PPP",end_date = "2025-10-01", owner = morce, start_date = datetime.date(2024, 11, 12))
        project_4.save()
        token = self.get_auth_token()
        response = self.client.get(reverse('tasks_management:projects')+'?name=pes', 
         HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        project = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(project), 1)
        slovnik = project[0]
        self.assertEqual (slovnik["name"], 'Pes')
        self.assertEqual (slovnik["description"], "PPP")
        self.assertEqual (slovnik["end_date"], "2025-10-01")
        self.assertEqual (slovnik["owner"], "KacKac")
        self.assertEqual (slovnik["start_date"], "2024-11-12")
    
    def test_get_4a_Project_details_get(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project= Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:project', kwargs={'project_id': project.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_response["name"], "Liska")
        self.assertEqual(project_response["description"], "LLL")
        self.assertEqual(project_response["start_date"], "2024-12-12")
        self.assertEqual(project_response["end_date"], "2025-01-01")
        self.assertEqual(project_response["id"], project.id)
        self.assertEqual(project_response["owner"], 'KacKac')
    
    def test_get_4a_Project_details_get_404(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:project', kwargs={'project_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(project_response["error"], "Project not found")
    
    def test_get_4b_Delete_Project_delite_200(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project= Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.delete( reverse('tasks_management:project', kwargs={'project_id': project.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id = project.id)
        self.assertEqual(project_response["message"], "Project deleted")
    
    def test_get_4b_Delete_Project_delete_404(self):
        User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.delete( reverse('tasks_management:project', kwargs={'project_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(project_response["error"], "Project not found")
        self.assertEqual(response.status_code, 404)
    
    def test_get_4b_Delete_Project_put_404(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.put( reverse('tasks_management:project', kwargs={'project_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(project_response["error"], "Invalid request method")
        self.assertEqual(response.status_code, 405)




    def test_get_project_tasks_5a(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "Task Title", description = "Task Description", created_date = "2024-12-29", created_by = opice, due_date= "2023-06-30", assigned_to = opice, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(project_response), 1)
        slovnik = project_response[0]
        self.assertEqual (slovnik["title"], 'Task Title')
        self.assertEqual (slovnik["description"], "Task Description")
        self.assertEqual (slovnik["created_date"], "2024-12-29")
        self.assertEqual (slovnik["created_by"], "KacKac")
        self.assertEqual (slovnik["due_date"], "2023-06-30")
        self.assertEqual (slovnik["assigned_to"], "KacKac")

    def test_get_project_tasks_5a_no_owner(self):
        nosorozec = User.objects.create_user(username='NosNos', password='Nosnos2')
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = nosorozec, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "Task Title", description = "Task Description", created_date = "2024-12-29", created_by = opice, due_date= "2023-06-30", assigned_to = nosorozec, project = project)
        my_task_1 = Task (title = "LLL", description = "LLL", created_date = datetime.date(2024, 12, 12), created_by = opice, due_date= "2023-06-12", assigned_to = opice, project = project)
        my_task.save()
        my_task_1.save()
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(project_response), 1)
        slovnik = project_response[0]
        self.assertEqual (slovnik["title"], 'LLL')
        self.assertEqual (slovnik["description"], "LLL")
        self.assertEqual (slovnik["created_date"], "2024-12-12")
        self.assertEqual (slovnik["created_by"], "KacKac")
        self.assertEqual (slovnik["due_date"], "2023-06-12")
        self.assertEqual (slovnik["assigned_to"], "KacKac")
        self.assertEqual (slovnik["id"], my_task_1.id)

    def test_get_project_tasks_5a_404(self):
        nosorozec = User.objects.create_user(username='NosNos', password='Nosnos2')
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:tasks', kwargs={'project_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(project_response["error"], "Project not found")
    
    def test_post_create_project_tasks_5b_403(self):
        nosorozec = User.objects.create_user(username='NosNos', password='Nosnos2')
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = nosorozec, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "Task Title", description = "Task Description", created_date = "2024-12-29", created_by = opice, due_date= "2023-06-30", assigned_to = nosorozec, project = project)
        my_task_1 = Task (title = "LLL", description = "LLL", created_date = datetime.date(2024, 12, 12), created_by = opice, due_date= "2023-06-12", assigned_to = opice, project = project)
        my_task.save()
        my_task_1.save()
        token = self.get_auth_token()
        response = self.client.post( reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(project_response["error"], "You are not allowed to create tasks in this project")
        
    def test_post_create_project_tasks_5b_(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.post(
        reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
        data = ({
            "title": "TTT",
            "description": "LLL",
            "created_date": "2024-12-29",
            "created_by": opice.username,
            "due_date": "2025-06-30",
            "assigned_to": opice.username
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        project_response = response.json()
        self.assertIsNotNone(project_response["id"])
        id = project_response["id"]
        my_task = Task.objects.get(id=id)
        self.assertEqual(my_task.title, "TTT")
        self.assertEqual(my_task.description, "LLL")
        self.assertEqual(my_task.created_date, datetime.date.today())
        self.assertEqual(my_task.due_date, datetime.date(2025, 6, 30))

    def test_post_create_project_tasks_5b_no_assigned_to(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.post(
        reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
        data = ({
            "title": "TTT",
            "description": "LLL",
            "created_date": "2024, 12-29",
            "due_date": "2025-06-30",
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        project_response = response.json()
        self.assertIsNotNone(project_response["id"])
        id = project_response["id"]
        my_task = Task.objects.get(id=id)
        self.assertEqual(my_task.title, "TTT")
        self.assertEqual(my_task.description, "LLL")
        self.assertEqual(my_task.created_date, datetime.date.today())
        self.assertEqual(my_task.due_date, datetime.date(2025, 6, 30))
        
    def test_post_create_project_tasks_5b_400(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.post(
        reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
        data = ({
            "description": "LLL",
            "created_date": "2024, 12-29",
            "due_date": "2025-06-30",
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 400)
        project_response = response.json()
        self.assertEqual(project_response["error"], "Invalid data")
        

    def test_post_create_project_tasks_5b_405(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        token = self.get_auth_token()
        response = self.client.put(
        reverse('tasks_management:tasks', kwargs={'project_id': project.id}),
        data = ({
            "description": "LLL",
            "created_date": "2024, 12-29",
            "due_date": "2025-06-30",
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 405)
        project_response = response.json()
        self.assertEqual(project_response["error"], "Invalid request method")
    
    def test_get_task_details_6a_404(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        self.assertFalse(Task.objects.filter(id=1).exists())
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:task', kwargs={'task_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(project_response["error"], "Task not found")
    
    def test_get_task_details_6a_403(self):
        nosorozec = User.objects.create_user(username='NosNos', password='Nosnos2')
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = nosorozec, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "Task Title", description = "Task Description", created_date = "2024-12-29", created_by = opice, due_date= "2023-06-30", assigned_to = nosorozec, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:task', kwargs={'task_id': my_task.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(project_response["error"], "You are not allowed to access this task")
    
    def test_get_task_details_6a_200(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "LLL", description = "MMM", created_date = "2024-12-30", created_by = opice, due_date= "2025-06-30", assigned_to = opice, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.get( reverse('tasks_management:task', kwargs={'task_id': my_task.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_response["title"], "LLL")
        self.assertEqual(project_response["description"], "MMM")
        self.assertEqual(project_response["created_date"], "2024-12-30")
        self.assertEqual(project_response["due_date"], "2025-06-30")
        self.assertEqual(project_response["id"], my_task.id)
        self.assertEqual(project_response["assigned_to"], 'KacKac')
    
    def test_get_task_details_6c_200_delete(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "LLL", description = "MMM", created_date = "2024-12-30", created_by = opice, due_date= "2025-06-30", assigned_to = opice, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.delete( reverse('tasks_management:task', kwargs={'task_id': my_task.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id = my_task.id)
        self.assertEqual(project_response["message"], "Task deleted")
    
    def test_get_task_details_6c_403_delete(self):
        nosorozec = User.objects.create_user(username='NosNos', password='Nosnos2')
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = nosorozec, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "Task Title", description = "Task Description", created_date = "2024-12-29", created_by = opice, due_date= "2023-06-30", assigned_to = nosorozec, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.delete( reverse('tasks_management:task', kwargs={'task_id': my_task.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(project_response["error"], "You are not allowed to access this task")
    
    def test_get_task_details_6c_404_delete(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        self.assertFalse(Task.objects.filter(id=1).exists())
        token = self.get_auth_token()
        response = self.client.delete( reverse('tasks_management:task', kwargs={'task_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(project_response["error"], "Task not found")

    def test_get_task_details_6b_404_put(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        self.assertFalse(Task.objects.filter(id=1).exists())
        token = self.get_auth_token()
        response = self.client.put( reverse('tasks_management:task', kwargs={'task_id': 1}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(project_response["error"], "Task not found")
    
    def test_get_task_details_6b_403_put(self):
        nosorozec = User.objects.create_user(username='NosNos', password='Nosnos2')
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = nosorozec, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "Task Title", description = "Task Description", created_date = "2024-12-29", created_by = opice, due_date= "2023-06-30", assigned_to = nosorozec, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.put( reverse('tasks_management:task', kwargs={'task_id': my_task.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(project_response["error"], "You are not allowed to access this task")
    
    def test_get_task_details_6b_200_put(self):
        opice = User.objects.create_user(username='KacKac', password='Hroch2')
        project = Project (name= "Liska", description= "LLL",end_date = "2025-01-01", owner = opice, start_date = datetime.date(2024, 12, 12))
        project.save()
        my_task = Task (title = "LLL", description = "MMM", created_date = "2024-12-30", created_by = opice, due_date= "2025-06-30", assigned_to = opice, project = project)
        my_task.save()
        token = self.get_auth_token()
        response = self.client.put( reverse('tasks_management:task', kwargs={'task_id': my_task.id}),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        project_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_response["message"], "Task completed")
        task = Task.objects.get(id=my_task.id)
        self.assertEqual(task.completed, True)
    
    

    
        
       
        

    
    

        


        

        

