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
import logging
import json

class PostList(APIView):
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
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PostListCategory(APIView):
    def get(self, request, category_id):
        posts = Post.objects.filter(categories__id = category_id).order_by('-created')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@require_http_methods(["GET"])
def post_list_category(request, category_id):

    try:
        logger.info(f"HTTP {request.method} request to {request.build_absolute_uri()}")

        posts_of_category = Post.objects.filter(categories__id = category_id).order_by('-created') #앞에 -를 붙이면 내림차순

        posts_of_category_json = []

        category_name = get_object_or_404(Category, id = category_id).name  #어떤 카테고리로 분류했는지 이름 저장

        for post in posts_of_category:

            post_json = {
                "id": post.id,
                "title" : post.title,
                "content": post.content,
                "status": post.status,
                "user": post.user.id,
            }

            posts_of_category_json.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '특정 카테고리의 게시글 목록 조회 성공',
            'category': category_name,  #분류한 카테고리 이름 보여줌
            'data': posts_of_category_json
        })
    except Exception as e:
        logger.error(f"Error occurred while fetching posts for category {category_id}: {e}")
        return JsonResponse({
            'status': 500,
            'message': '특정 카테고리의 게시글 목록 조회 실패',
            'data': str(e)
        })

