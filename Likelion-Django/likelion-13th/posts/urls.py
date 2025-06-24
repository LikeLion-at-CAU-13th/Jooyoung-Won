from django.urls import path
from posts.views import *
from comments.views import *

urlpatterns = [

    # path('', post_list, name="post_list"),
    # path('category/<int:category_id>/', post_list_category, name="post_list_category"),
    # path('<int:post_id>/', post_detail, name='post_detail'),
    # path('<int:post_id>/comment/', comment_list, name='comment_list'),

    path('', PostList.as_view()),   # post 전체 조회
    path('<int:post_id>/', PostDetail.as_view()), # post 개별 조회
    path('category/<int:category_id>/', PostListCategory.as_view()),
    path('<int:post_id>/comment/', CommentList.as_view()),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]