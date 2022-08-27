from rest_framework.response import Response
from rest_framework import views
from rest_framework.status import *
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class NoticeListView(views.APIView):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        notices = Notice.objects.all()
        serializer = self.serializer_class(notices, many=True)
        return Response({'message': 'TF 공지 목록 조회 성공', 'data': serializer.data})

    def post(self, request):
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'content': request.data.get('content')
        }
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'TF 공지 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': 'TF 공지 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
