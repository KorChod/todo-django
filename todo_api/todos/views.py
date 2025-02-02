from rest_framework import generics, permissions
from .serializers import TodoSerializer
from .models import Todo


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    view_name = 'todo-list-create'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    view_name = 'todo-retrieve-update-destroy'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
