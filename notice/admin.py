from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'user', 'created_at']
	list_display_links = ['id', 'title']
