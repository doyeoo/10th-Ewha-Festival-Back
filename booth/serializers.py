from rest_framework import serializers

from .models import Booth, Menu, Image, Comment
from account.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'menu', 'price', 'is_soldout']


class BoothListSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    is_liked = serializers.BooleanField(default=False)
    
    class Meta:
        model = Booth
        fields = ['id', 'user', 'day', 'college', 'name', 'number', 'thumnail', 'description', 'is_liked', 'created_at', 'updated_at']
        read_only_fields= ('thumnail', )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'booth', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields= ('booth', 'user', )


class BoothDetailSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    menus = MenuSerializer(read_only=True, many=True)
    images = ImageSerializer(read_only=True, many=True)
    is_liked = serializers.BooleanField(default=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Booth
        fields = ['id', 'user', 'day', 'college', 'name', 'number', 'thumnail', 'notice', 'description', 'images', 'menus', 'is_liked', 'created_at', 'updated_at', 'comments']

