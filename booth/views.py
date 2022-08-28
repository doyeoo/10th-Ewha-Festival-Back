from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import *
from .serializers import *
from .permissions import IsAuthorOrReadOnly


class BoothListView(views.APIView):
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

        booths = Booth.objects.filter(**arguments)
        if user:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked=True

        serializer = self.serializer_class(booths, many=True)

        return Response({'message': '부스 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)


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
            return Response({'message': '부스 좋아요 성공', 'data': serializer.data}, status=HTTP_200_OK)
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
            return Response({'message': '부스 좋아요 취소 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '부스 좋아요 취소 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class SearchView(views.APIView):
    serializer_class = BoothListSerializer

    def get(self, request):
        keyword= request.GET.get('keyword')
        booths = Booth.objects.filter(name__contains=keyword) | Booth.objects.filter(menus__menu__contains=keyword)

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