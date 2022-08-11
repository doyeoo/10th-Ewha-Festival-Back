from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response

from .models import *
from .serializers import *


class SignUpView(views.APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

