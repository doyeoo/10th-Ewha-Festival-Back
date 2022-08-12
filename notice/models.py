from django.db import models
from account.models import User
from booth.models import TimeStamp

class Notice(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()