from rest_framework import serializers
from .models import Booth, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['menu', 'image', 'price', 'is_soldout']


class BoothSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    menus = MenuSerializer(read_only=True, many=True)
    
    class Meta:
        model = Booth
        fields = ['id', 'user', 'day', 'college', 'name', 'image', 'notice', 'description', 'menus', 'like', 'created_at', 'updated_at']