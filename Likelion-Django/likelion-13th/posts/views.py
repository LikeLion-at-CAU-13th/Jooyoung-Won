from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가
from comments.models import Comment
from rest_framework.views import APIView    # APIView를 사용하기 위해 import
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import *

class PostList(APIView): 
    permission_classes = [IsTimeNotLate, IsAuthenticatedOrReadOnly] # 로그인 안 하면 작성 X
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        posts = Post.objects.all()
        # 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    permission_classes = [IsTimeNotLate, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        # 객체 레벨 권한은 .get_object()가 호출될 때 실행됨. get_object_or_404()를 쓴다면 수동으로 호출해줘야 함
        self.check_object_permissions(request, post)  
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)  # 권한 체크 수동
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PostListCategory(APIView):
    permission_classes = [IsTimeNotLate]
    def get(self, request, category_id):
        posts = Post.objects.filter(categories__id = category_id).order_by('-created')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
