from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods 
from .models import *
import json
import logging
from rest_framework.views import APIView   
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer
from config.permissions import IsTimeNotLate
from drf_yasg.utils import swagger_auto_schema

class CommentList(APIView):
    #permission_classes = [IsTimeNotLate] 
    @swagger_auto_schema(
        operation_summary="댓글 목록 조회",
        operation_description="게시글의 댓글을 조회합니다.",
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request, post_id, format=None):
        comments = Comment.objects.all().filter(post__id = post_id) 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # 댓글 작성 api 추가
    def post(self, request, post_id, format=None):
        data = request.data.copy()
        data['post'] = post_id  # post 필드를 명시적으로 추가

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
