from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response

from .models import *
from .serializers import *


class BoothListView(views.APIView):
    serializer_class = BoothSerializer

    def get(self, request):
        booths = Booth.objects.all()
        serializer = self.serializer_class(booths, many=True)

        return Response({'message': '부스 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)


class BoothDetailView(views.APIView):
    serializer_class = BoothSerializer

    def get(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        serializer = self.serializer_class(booth)

        return Response({'message': '부스 상세 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
