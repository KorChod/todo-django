from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name=RegisterView.view_name),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
]
