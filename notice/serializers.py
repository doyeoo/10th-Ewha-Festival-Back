from rest_framework import serializers
from .models import Notice


class NoticeListSerializer(serializers.ModelSerializer):
    update_date = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Notice
        fields = ["id", "title", "update_date"]
