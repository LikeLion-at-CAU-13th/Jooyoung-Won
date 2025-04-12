from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가
from comments.models import Comment
import logging
import json

logger = logging.getLogger('django')

# 함수 데코레이터, 특정 http method만 허용
@require_http_methods(["POST", "GET"])
def post_list(request):

    logger.info(f"HTTP {request.method} request to {request.build_absolute_uri()}")

    if request.method == "POST":
        try:
            # byte -> 문자열 -> python 딕셔너리
            body = json.loads(request.body.decode('utf-8'))

            # 프론트에게서 user id를 넘겨받는다고 가정.
            # 외래키 필드의 경우, 객체 자체를 전달해줘야하기 때문에
            # id를 기반으로 user 객체를 조회해서 가져옵니다 !
            user_id = body.get('user')
            user = get_object_or_404(User, pk=user_id)

            # 새로운 데이터를 DB에 생성
            new_post = Post.objects.create(
                title = body['title'],
                content = body['content'],
                status = body['status'],
                user = user
            )

            # Json 형태 반환 데이터 생성
            new_post_json = {
                "id": new_post.id,
                "title" : new_post.title,
                "content": new_post.content,
                "status": new_post.status,
                "user": new_post.user.id
            }

            logger.info(f"Successfully created post with ID {new_post.id}")
            return JsonResponse({
                'status': 200,
                'message': '게시글 생성 성공',
                'data': new_post_json
            })
        
        except Exception as e:
            logger.error(f"Error occurred while creating post: {e}")
            return JsonResponse({
                'status': 500,
                'message': '게시글 생성 실패',
                'data': str(e)
            })
        
    
    if request.method == "GET":
        try:
            post_all = Post.objects.all()

            post_json_all = []

            for post in post_all:
                post_json = {
                    "id": post.id,
                    "title" : post.title,
                    "content": post.content,
                    "status": post.status,
                    "user": post.user.id
                }
                post_json_all.append(post_json)

            logger.info(f"Successfully retrieved post lists")
            return JsonResponse({
                'status': 200,
                'message': '게시글 목록 조회 성공',
                'data': post_json_all
            })
        
        except Exception as e:
            logger.error(f"Error occurred while fetching post list: {e}")
            return JsonResponse({
                'status': 500,
                'message': '게시글 목록 조회 실패',
                'data': str(e)
            })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, post_id):

    logger.info(f"HTTP {request.method} request to {request.build_absolute_uri()}")

    # post_id에 해당하는 단일 게시글 조회
    if request.method == "GET":
        try:
            post = get_object_or_404(Post, pk=post_id)

            post_json = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "status": post.status,
                "user": post.user.id,
                #post_detail에 categories 추가
                "categories" : [
                    {
                        "id": category.id,
                        "name": category.name,
                    }
                    for category in post.categories.all()
                ], 
            }
            
            logger.info(f"Successfully retrieved post with ID {post.id}")
            return JsonResponse({
                'status': 200,
                'message': '게시글 단일 조회 성공',
                'data': post_json
            })
        
        except Exception as e:
                logger.error(f"Error occurred while fetching post with ID {post_id}: {e}")
                return JsonResponse({
                    'status': 500,
                    'message': '게시글 조회 실패',
                    'data': str(e)
                })
    
    if request.method == "PATCH":
        try:
            body = json.loads(request.body.decode('utf-8'))
                            
            update_post = get_object_or_404(Post, pk=post_id)

            if 'title' in body:
                update_post.title = body['title']
            if 'content' in body:
                update_post.content = body['content']
            if 'status' in body:
                update_post.status = body['status']
            
            update_post.save()

            update_post_json = {
                "id": update_post.id,
                "title" : update_post.title,
                "content": update_post.content,
                "status": update_post.status,
                "user": update_post.user.id,
                #post_detail에 categories 추가
                "categories" : [
                    {
                        "id": category.id,
                        "name": category.name,
                    }
                    for category in update_post.categories.all()
                ], 
            }

            logger.info(f"Successfully updated post with ID {update_post.id}")
            return JsonResponse({
                'status': 200,
                'message': '게시글 수정 성공',
                'data': update_post_json
            })
        
        except Exception as e:
                logger.error(f"Error occurred while updating post with ID {post_id}: {e}")
                return JsonResponse({
                    'status': 500,
                    'message': '게시글 수정 실패',
                    'data': str(e)
                })
    
    if request.method == "DELETE":

        try:
            delete_post = get_object_or_404(Post, pk=post_id)
            delete_post.delete()

            logger.info(f"Successfully deleted post with ID {post_id}")
            return JsonResponse({
                    'status': 200,
                    'message': '게시글 삭제 성공',
                    'data': None
            })
        
        except Exception as e:
                logger.error(f"Error occurred while deleting post with ID {post_id}: {e}")
                return JsonResponse({
                    'status': 500,
                    'message': '게시글 삭제 실패',
                    'data': str(e)
                })
    
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

