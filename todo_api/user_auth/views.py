from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    view_name = 'register'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
