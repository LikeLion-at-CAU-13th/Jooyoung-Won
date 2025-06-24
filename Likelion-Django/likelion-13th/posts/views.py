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
from django.core.files.storage import default_storage  
from .serializers import ImageSerializer
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import boto3
import uuid
from rest_framework.parsers import MultiPartParser, FormParser

class PostList(APIView): 
    permission_classes = [IsTimeNotLate, IsAuthenticatedOrReadOnly] # 로그인 안 하면 작성 X
    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="새로운 게시글을 생성합니다.",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "잘못된 요청"}
    )
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="모든 게시글을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, format=None):
        posts = Post.objects.all()
        # 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    permission_classes = [IsTimeNotLate, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시글 상세 조회",
        operation_description="특정 게시글을 조회합니다.",
        responses={200: PostSerializer, 404: "게시글 조회 오류"}
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="게시글 수정",
        operation_description="게시글을 수정합니다.",
        request_body=PostSerializer,
        responses={200: PostSerializer, 404: "잘못된 요청"}
    )
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        # 객체 레벨 권한은 .get_object()가 호출될 때 실행됨. get_object_or_404()를 쓴다면 수동으로 호출해줘야 함
        self.check_object_permissions(request, post)  
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="게시글 삭제",
        operation_description="게시글을 삭제합니다.",
        responses={204: "삭제 완료", 404: "게시글을 불러오지 못함"}
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)  # 권한 체크 수동
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PostListCategory(APIView):
    permission_classes = [IsTimeNotLate]
    @swagger_auto_schema(
        operation_summary="카테고리별 게시글 목록 조회",
        operation_description="카테고리별 게시글을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, category_id):
        posts = Post.objects.filter(categories__id = category_id).order_by('-created')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_summary="이미지 업로드",
        operation_description="이미지를 S3에 업로드합니다.",
        manual_parameters=[            
            openapi.Parameter(
                name="image",
                in_ = openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="업로드할 이미지 파일"
            )
        ],
        responses={201: ImageSerializer, 400: "요청에 이미지 파일이 없음", 500: "서버 에러"}
    )
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image file"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # S3에 파일 저장
        file_path = f"uploads/{uuid.uuid4()}_{image_file.name}"
        # S3에 파일 업로드
        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path,
                Body=image_file.read(),
                ContentType=image_file.content_type,
            )
        except Exception as e:
            return Response({"error": f"S3 Upload Failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 업로드된 파일의 URL 생성
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_path}"

        # DB에 저장
        image_instance = Image.objects.create(image_url=image_url)
        serializer = ImageSerializer(image_instance)


        return Response(serializer.data, status=status.HTTP_201_CREATED)