## SETUP

1. Create and activate virtual environment (optional but recommended)  
`python3 -m venv .venv`  
`source .venv/bin/activate`

2. Install dependencies  
`pip install -r requirements.txt`

3. Go to Django project directory  
`cd todo_api`

4. Make and apply migrations  
`python manage.py makemigrations`  
`python manage.py migrate`

5. Run the server  
`python manage.py runserver`

6. The tests can be run with the following command
`python manage.py test`

## APPROACH
I have created the main Django project called `todo_api` which consists of two applications. The first one called `todos` is responsible for TODO CRUD operations and the second one `user_auth` for user registration and login/token retrieval. I have used the default db configuration using sqlite3. The tests are located in the `todo_api/tests.py` and `user_auth/tests.py` files. The first file contains test cases for CRUD operations on the Todo API. The second one contains tests for user registration and authentication endpoints.

Available endpoints:
1. register new user: POST /api/auth/register/
2. obtain access token: POST /api/auth/token/
3. browse user todos: GET /api/todos/
4. create new todo: POST /api/todos/
5. browse todo details: GET /api/todos/<int:pk>/
6. edit todo: PATCH /api/todos/<int:pk>/
7. delete todo: DELETE /api/todos/<int:pk>/
8. log in to browsable API: /api-auth/login/

All the endpoints are accessible through DRF browsable API in the browser.

## FUTURE IMPROVEMENTS
1. Make password require special characters, numbers, min length.
2. Add support for refresh token
3. I have added session authentication to settings to support login through DRF UI for debugging purposes. It would be wise to allow it only for development and disable this option for production.
4. Introduce Docker to run the application and the database.
