from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.


class NoticeListView(views.APIView):
    serializer_class = NoticeListSerializer

    def get(self, request, format=None):
        notices = Notice.objects.all()
        serializer = NoticeListSerializer(notices, many=True)
        return Response({'message': 'TF 목록 조회 성공', 'data': serializer.data})
