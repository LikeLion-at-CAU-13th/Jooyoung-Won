from django.db import models
from accounts.models import User

# Create your models here.
# 추상 클래스 정의
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    updated = models.DateTimeField(auto_now=True)  # 객체를 저장할 때 날짜와 시간 갱신

    class Meta:
        abstract = True


class Post(BaseModel): # BaseModel을 상속받음

    CHOICES = (
        ('STORED', '보관'),
        ('PUBLISHED', '발행')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=CHOICES, default='STORED')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    categories = models.ManyToManyField('categories.Category', through='PostCategory')
    #categories.Category (모델이 정의된 앱 이름).(모델 클래스 이름)
    #post에서 다대다 관계를 설정했으면 category에서는 설정 안 해도 됨. 설정할 경우 중복 오류 발생 가능

    def __str__(self): # 표준 파이썬 클래스 메서드, 사람이 읽을 수 있는 문자열을 반환하도록 함
        return self.title
    
#중간 테이블 모델
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"