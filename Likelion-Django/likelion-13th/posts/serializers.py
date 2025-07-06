### Model Serializer case

from rest_framework import serializers
from .models import Post
from .models import Image
from config.custom_api_exceptions import PostConflictException
from config.custom_api_exceptions import PostDailyLimitException
from django.utils.timezone import now

class PostSerializer(serializers.ModelSerializer):

  class Meta:
	# 어떤 모델을 시리얼라이즈할 건지
    model = Post
	# 모델에서 어떤 필드를 가져올지
	# 전부 가져오고 싶을 때
    fields = "__all__"

  # 중복된 게시글 제목이 있다면 예외 발생, 하루에 여러 개 올리면 예외 발생
  def validate(self, data):
    user= data.get('user')
    today = now().date()
  
    if Post.objects.filter(title=data['title']).exists():
      raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")

    if Post.objects.filter(user=user, created__date=today).exists():
      raise PostDailyLimitException(detail=f"Today post limit")
    
    return data

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"