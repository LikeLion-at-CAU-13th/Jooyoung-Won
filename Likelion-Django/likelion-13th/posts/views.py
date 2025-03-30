from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-13th!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "status" : post.status,
        "user" : post.user.username,
        "categories" : [category.name for category in post.categories.all()],
        "comments" : [
            {
                "id": comment.id,
                "writer": comment.writer,
                "content": comment.content,
                "created": comment.created,
                "updated": comment.updated
            }
            for comment in post.comments.all()
        ]
    }
    return JsonResponse({
        "status" : 200,
        "data" : post_detail_json})
