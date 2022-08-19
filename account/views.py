from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from booth.models import Booth
from booth.serializers import BoothDetailSerializer


class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({'message': "로그인 성공", 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': "로그인 실패", 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = get_object_or_404(User, pk=user.id)

        serializer = self.serializer_class(data)

        return Response({'message': "프로필 조회 성공", 'data': serializer.data}, status=HTTP_200_OK)


class LikedListView(views.APIView):
    serializer_class = BoothDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        booths = Booth.objects.filter(like=user.id)

        for booth in booths:
            booth.is_liked=True
            
        serializer = self.serializer_class(booths, many=True)

        return Response({'message': "좋아요한 부스 목록 조회 성공", 'data': serializer.data}, status=HTTP_200_OK)

