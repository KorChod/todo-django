from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Todo
from .views import TodoListCreateView, TodoRetrieveUpdateDestroyView


class TodoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.todo = Todo.objects.create(user=self.user, title='Test Todo')

    def test_todo_list(self):
        """
        Access user's list of dotos
        """
        url = reverse(TodoListCreateView.view_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_todo_create(self):
        """
        Create new todo for authenticated user
        """
        url = reverse(TodoListCreateView.view_name)
        data = {'title': 'New Todo',
                'description': 'New Description', 'is_completed': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

        todos = Todo.objects.filter(user=self.user)
        self.assertEqual(len(todos), 2)
        todo2 = Todo.objects.filter(
            user=self.user, id=response.data["id"]).first()
        self.assertEqual(todo2.title, data['title'])
        self.assertEqual(todo2.description, data['description'])
        self.assertEqual(todo2.is_completed, data['is_completed'])

    def test_todo_detail(self):
        """
        Preview todo details for authenticated user
        """
        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Todo')

    def test_todo_update(self):
        """
        Update todo details for authenticated user
        """
        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])
        data = {'title': 'Updated Todo'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

        todos = Todo.objects.filter(user=self.user)
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].title, data['title'])

    def test_todo_delete(self):
        """ 
        Delete todo for authenticated user
        """
        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])

        todos = Todo.objects.filter(user=self.user)
        self.assertEqual(len(todos), 1)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        todos = Todo.objects.filter(user=self.user)
        self.assertEqual(len(todos), 0)


class ProtectedTodoAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and todo item but DO NOT authenticate
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.another_user = User.objects.create_user(
            username='anotheruser', password='testpass')
        self.todo = Todo.objects.create(user=self.user, title='Test Todo')

    def test_protected_list_access(self):
        """
        Unauthenticated users cannot access the TODO list.
        """
        url = reverse(TodoListCreateView.view_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)

        self.client.force_authenticate(user=self.another_user)
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)

    def test_protected_detail_access(self):
        """
        Users cannot access another user's TODO item.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.force_authenticate(user=self.another_user)

        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_protected_update_access(self):
        """
        Users cannot access another user's TODO item.
        """
        self.client.force_authenticate(user=self.another_user)
        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])
        data = {'title': 'Updated Todo'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 404)

    def test_protected_delete_access(self):
        """
        Users cannot access another user's TODO item.
        """
        self.client.force_authenticate(user=self.another_user)
        url = reverse(TodoRetrieveUpdateDestroyView.view_name,
                      args=[self.todo.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)
