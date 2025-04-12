from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods 
from .models import *
import json
import logging

logger = logging.getLogger('django')

@require_http_methods(["GET"])
def comment_list(request, post_id):

    logger.info(f"HTTP {request.method} request to {request.build_absolute_uri()}")

    try:
        comments_of_post = Comment.objects.all().filter(post__id = post_id) 
        # 외부 모델의 필드를 사용할 때, 조건을 사용한 경우에는 언더바 2개 __ 사용. 
        # 현재는 comment가 가진 post의, id를 사용하기 때문에 외부 필드
        comments_of_post_json = []

        for comment in comments_of_post:
            comment_json = {
                "id": comment.id,
                "writer": comment.writer,
                "content": comment.content,
                "post": comment.post.id
            }
            comments_of_post_json.append(comment_json)

        return JsonResponse({
            "status": 200,
            "message": "댓글 목록 조회 성공",
            "data": comments_of_post_json
        })
    except Exception as e:
        logger.error(f"Error occurred while fetching comments for post ID {post_id}: {e}")
        return JsonResponse({
            'status': 500,
            'message': '댓글 목록 조회 실패',
            'data': str(e)
        })