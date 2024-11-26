# Task management REST API

## Startup

Install libraries: `pip install -r requirements.txt`

## Endpoints

### 1. Login

**URL:** `/api/login`  
**Method:** `POST`  
**Description:** Authenticates a user and returns a JWT token.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**

- **Success (200):**

```json
{
    "token": "your_jwt_token"
}
```

- **Error invalid credentials (400):**

```json
{
    "error": "Invalid credentials"
}
```

- **Error missing data (400):**

```json
{
    "error": "Invalid data"
}
```

### 2. Register

**URL:** `/api/register`  
**Method:** `POST`  
**Description:** Registers a new user.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
    "username": "your_username",
    "password": "your_password",
}
```

**Response:**

- **Success (200):**

```json
{
    "message": "User registered successfully"
}
```

- **Error missing data (400):**

```json
{
    "error": "Invalid data"
}
```

### 3a. Get projects

**URL:** `/api/projects`  
**Method:** `GET`  
**Description:** Retrieves a list of all projects. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
```

**Parameters**

- `name` (string): Filters proects by name.

**Response:**

- **Success (200):**

```json
[
    {
        "id": 1,
        "name": "Project 1",
        "description": "Description of Project 1",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "owner": "jeff"
    },
    ...
]
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

### 3b. Create projects

**URL:** `/api/projects`  
**Method:** `POST`  
**Description:** Creates a new project. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
Content-Type: application/json
```

**Request Body:**

```json
{
    "name": "Project Name",
    "description": "Project Description",
    "end_date": "2023-12-31"
}
```

**Response:**

- **Success (200):**

```json
{
    "id": 1
}
```

- **Error (400):**

```json
{
    "error": "Invalid data"
}
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

### 4a. Project Details

**URL:** `/api/projects/<int:project_id>`  
**Method:** `GET`  
**Description:** Retrieves details of a specific project. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
```

**Path Parameters**

- `project_id` (integer): The ID of the project.

**Response:**

- **Success (200):**

```json
{
    "id": 1,
    "name": "Project 1",
    "description": "Description of Project 1",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
}
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

- **Error (404):**

```json
{
    "error": "Project not found"
}
```

### 4b. Delete a Project

**URL:** `/api/projects/<int:project_id>`  
**Method:** `DELETE`  
**Description:** Deletes a specific project. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
```

**Path Parameters:**

- `project_id` (integer): The ID of the project to be deleted.

**Response:**

- **Success (200):**

```json
{
    "message": "Project deleted"
}
```

- **Error (404):**

```json
{
    "error": "Project not found"
}
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

### 5a. Get project tasks

**URL:** `/api/projects/<int:project_id>/tasks`  
**Method:** `GET`  
**Description:** Retrieves a list of tasks for a specific project. Requires authentication. Project owner can see all the tasks for project, person who is not an owner can only see his own tasks.

**Headers:**

```
Authorization: Bearer your_jwt_token
```

**Path Parameters**

- `project_id` (integer): The ID of the project.

**Response:**

- **Success (200):**

```json
[
    {
        "id": 1,
        "title": "Task 1",
        "description": "Description of Task 1",
        "created_date": "2023-01-01T00:00:00Z",
        "created_by": "username",
        "due_date": "2023-06-30",
        "completed": false,
        "assigned_to": "username"
    },
    ...
]
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

- **Error (404):**

```json
{
    "error": "Project not found"
}
```

### 5b. Create project tasks

**URL:** `/api/projects/<int:project_id>/tasks`  
**Method:** `POST`  
**Description:** Creates a new task for a specific project. Only the project owner can create tasks. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
Content-Type: application/json
```

**Path Parameters**

- `project_id` (integer): The ID of the project.

**Request body**

```json
{
    "title": "Task Title",
    "description": "Task Description",
    "due_date": "2023-06-30",
    "assigned_to": 2  // User ID of the assigned user (optional)
}
```

**Response:**

- **Success (200):**

```json
[
    {
        "id": 1
    },
    ...
]
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

- **Error (403):**

```json
{
    "error": "You are not allowed to create tasks in this project"
}
```

- **Error (404):**

```json
{
    "error": "Project not found"
}
```

### 6a. Get task details

**URL:** `/api/tasks/<int:task_id>`  
**Method:** `GET`  
**Description:** Retrieves details of a specific task. Only project owner or assigned user can view the task. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
```

**Path Parameters:**

- `project_id` (integer): The ID of the task.

**Response:**

- **Success (200):**

```json
{
    "id": 1,
    "title": "Task 1",
    "description": "Description of Task 1",
    "created_date": "2023-01-01T00:00:00Z",
    "created_by": "username",
    "due_date": "2023-06-30",
    "completed": false,
    "assigned_to": "username"
}
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

- **Error (403):**

```json
{
    "error": "You are not allowed to access this task"
}
```

- **Error (404):**

```json
{
    "error": "Task not found"
}
```

### 6b. Complete task

**URL:** `/api/tasks/<int:task_id>`  
**Method:** `PUT`  
**Description:** Completes specific task. Only project owner or assigned user can complete the task. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
Content-Type: application/json
```

**Path Parameters**

- `task_id` (integer): The ID of the task.

**Response:**

- **Success (200):**

```json
{
    "message": "Task completed"
}
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

- **Error (403):**

```json
{
    "error": "You are not allowed to access this task"
}
```

- **Error (404):**

```json
{
    "error": "Task not found"
}
```

### 6c. Delete task

**URL:** `/api/tasks/<int:task_id>`  
**Method:** `PUT`  
**Description:** Delete specific task. Only project owner ot assigned user can delete task. Requires authentication.

**Headers:**

```
Authorization: Bearer your_jwt_token
Content-Type: application/json
```

**Path Parameters**

- `task_id` (integer): The ID of the task.

**Response:**

- **Success (200):**

```json
{
    "message": "Task deleted"
}
```

- **Error (401):**

```json
{
    "error": "Unauthorized"
}
```

- **Error (403):**

```json
{
    "error": "You are not allowed to access this task"
}
```

- **Error (404):**

```json
{
    "error": "Task not found"
}
```