from django.db import models

class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, unique=True) #Django는 char, varchar 구분이 없음. varchar가 기본
    #unique로 중복 허용 X

    def __str__(self):
        return self.name