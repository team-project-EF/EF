from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your models here.

# 미디어 파일의 세부 정보를 저장하기 위한 class 지정
class Upload(models.Model):
    img = models.ImageField(upload_to='images/', blank=True, null=True)