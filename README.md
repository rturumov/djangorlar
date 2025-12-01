# Djangolar Education API

Djangolar is a Django REST Framework project for managing **courses** and **lessons**.  
Users can create, update, and manage courses and lessons with JWT authentication.

---

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repo-url>
    cd djangolar
    ```

2. **Create and activate virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the server:**

    ```
    python manage.py runserver
    ```

---
## Authentication
### Obtain JWT Token
- **POST** `/api/token/`  
- **Request Body Example:**

    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword"
    }
    ```

- **Response:**
    ```json
    {
        "refresh": "refresh_token_here",
        "access": "access_token_here"
    }
    ```
### Refresh JWT Token
- **POST** `/api/token/refresh/`
- **Request:**

    ```json
    {
        "refresh": "refresh_token_here"
    }
    ```
- **Response:**
 
    ```json
    {
        "access": "new_access_token_here"
    }
    ```

---
## Courses
### List & Create Courses
- **GET** `/ POST /api/v1/education/courses/`
- **POST Request Example:**

    ```json
    {
        "title": "Python Basics",
        "description": "Learn Python from scratch"
    }
    ```

- **Response Example (201 Created):**

    ```json
    {
        "id": 1,
        "title": "Python Basics",
        "description": "Learn Python from scratch",
        "owner": 1,
        "is_active": false
    }
    ```
### Retrieve, Update, Delete Course
- **GET / PUT / DELETE** `/api/v1/education/courses/<id>/`
- **PUT Request Example:**

    ```json
    {
        "title": "Advanced Python",
        "description": "Deep dive into Python"
    }
    ```
### Activate / Deactivate Course
- **POST** `/api/v1/education/courses/<id>/activate/`
- **POST** `/api/v1/education/courses/<id>/deactivate/`

### List Lessons of a Course
- **GET** `/api/v1/education/courses/<id>/lessons/`
- **Response Example:**

    ```json
    [
        {
            "id": 1,
            "title": "Lesson 1",
            "content": "Lesson content here",
            "owner": 1,
            "course": 1,
            "is_published": true
        }
    ]
    ```

## Lessons
### Create Lesson
- **POST** `/api/v1/education/lessons/`
- **Request Example:**

    ```json
    {
        "title": "Introduction to Functions",
        "content": "Functions are blocks of code...",
        "course": 1
    }
    ```

### Move Lesson
- **PUT** `/api/v1/education/lessons/<id>/move/`
- **Request Example:**
    ```json
    {
        "new_course": 2,
        "new_position": 1
    }
    ```
### Delete Lesson

- **DELETE** `/api/v1/education/lessons/<id>/`

### Publish / Unpublish Lesson
- **POST** `/api/v1/education/lessons/<id>/publish/`
- **POST** `/api/v1/education/lessons/<id>/unpublish/`
---

## Testing
**Run all tests using:**
```bash
PYTHONPATH=$(pwd) pytest -v
```
---
Note: All endpoints require JWT authentication except `/api/token/` and `/api/token/refresh/`.