from django.urls import path
from .views import TodoListCreateView, TodoRetrieveUpdateDestroyView


urlpatterns = [
    path('', TodoListCreateView.as_view(), name=TodoListCreateView.view_name),
    path('<int:pk>/', TodoRetrieveUpdateDestroyView.as_view(),
         name=TodoRetrieveUpdateDestroyView.view_name),
]
