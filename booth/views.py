import boto3
import uuid
import math

from django.shortcuts import get_object_or_404
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr

from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .permissions import IsAuthorOrReadOnly
from .pagination import PaginationHandlerMixin
from .storages import FileUpload, s3_client


class BoothPagination(PageNumberPagination):
    page_size = 10


class BoothListView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    serializer_class = BoothListSerializer

    def get(self, request):
        user = request.user
        
        day = request.GET.get('day')
        college = request.GET.get('college')

        params = {'day': day, 'college': college}
        arguments = {}
        for key, value in params.items():
            if value:
                arguments[key] = value

        booths = Booth.objects.filter(**arguments).annotate(
                    number_order = Cast(Substr("number", 2), IntegerField())
                ).order_by("number_order")
        total = booths.__len__()
        total_page = math.ceil(total/10)
        booths = self.paginate_queryset(booths)

        if user:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked=True
        
        serializer = self.serializer_class(booths, many=True)
        return Response({'message': '부스 목록 조회 성공', 'total': total, 'total_page' : total_page, 'data': serializer.data}, status=HTTP_200_OK)


class BoothDetailView(views.APIView):
    serializer_class = BoothDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        booth = get_object_or_404(Booth, pk=pk)
        self.check_object_permissions(self.request, booth)
        return booth

    def get(self, request, pk):
        user = request.user
        booth = self.get_object(pk=pk)

        if booth.like.filter(pk=user.id).exists():
            booth.is_liked=True

        serializer = self.serializer_class(booth)

        return Response({'message': '부스 상세 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

    def patch(self, request, pk):
        booth = self.get_object(pk=pk)
        serializer = self.serializer_class(data=request.data, instance=booth, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '부스 정보 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '부스 정보 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class MenuListView(views.APIView):
    serializer_class = MenuSerializer

    def get(self, request, pk):
        menus = Menu.objects.filter(booth=pk)
        serializer = self.serializer_class(menus, many=True)
            
        return Response({'message': '메뉴 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)


class MenuDetailView(views.APIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        menu = get_object_or_404(Menu, pk=pk)
        self.check_object_permissions(self.request, menu.booth)
        return menu

    def patch(self, request, pk, menu_pk):
        menu = self.get_object(pk=menu_pk)
        serializer = self.serializer_class(data=request.data, instance=menu, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '메뉴 정보 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '메뉴 정보 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LikeView(views.APIView):
    serializer_class = BoothDetailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        booth = get_object_or_404(Booth, pk=pk)
        booth.like.add(user)
        booth.is_liked=True

        serializer = self.serializer_class(data=request.data, instance=booth, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '부스 좋아요 성공', 'data': {'booth': serializer.data['id'], 'is_liked': serializer.data['is_liked']}}, status=HTTP_200_OK)
        else:
            return Response({'message': '부스 좋아요 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = request.user
        booth = get_object_or_404(Booth, pk=pk)
        booth.like.remove(user)
        booth.is_liked=False

        serializer = self.serializer_class(data=request.data, instance=booth, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '부스 좋아요 취소 성공', 'data': {'booth': serializer.data['id'], 'is_liked': serializer.data['is_liked']}}, status=HTTP_200_OK)
        else:
            return Response({'message': '부스 좋아요 취소 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class SearchView(views.APIView):
    serializer_class = BoothListSerializer

    def get(self, request):
        user = request.user
        keyword= request.GET.get('keyword')

        booths = (Booth.objects.filter(name__icontains=keyword) | Booth.objects.filter(menus__menu__contains=keyword)).distinct()

        if user:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked=True

        serializer = self.serializer_class(booths, many=True)

        return Response({'message':'부스 검색 성공', 'data': serializer.data}, status=HTTP_200_OK)


class CommentView(views.APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, booth=booth)
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    

class CommentDetailView(views.APIView): 
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment

    def delete(self, request, pk, comment_pk):
        comment = self.get_object(pk=comment_pk)
        comment.delete()
        
        return Response({'message': '댓글 삭제 성공'}, status=HTTP_204_NO_CONTENT)


class BoothThumnailView(views.APIView):
    def patch(self, request, pk):
        file = request.FILES.get('file')
        booth = get_object_or_404(Booth, pk=pk)
        folder = booth.name+'/thumnail'
    
        serializer = BoothListSerializer(data=request.data, instance=booth, partial=True)
        
        if serializer.is_valid():
            file_url = FileUpload(s3_client).upload(file, folder)
            serializer.save(thumnail=file_url)
            return Response({'message': '대표 사진 업로드 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '대표 사진 업로드 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class BoothImageView(views.APIView):
    serialize_class = ImageSerializer
    
    def post(self, request, pk) :
        files = request.FILES.getlist('file')
        booth = get_object_or_404(Booth, pk=pk)
        folder = booth.name+'/images'

        for file in files :
            file_url = FileUpload(s3_client).upload(file, folder)
            Image.objects.create(
                booth = booth,
                image = file_url
            )
        return Response({"message" : "이미지 업로드 성공"}, status=HTTP_200_OK)
    
