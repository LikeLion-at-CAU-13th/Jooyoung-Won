from django.urls import path
from posts.views import *
from comments.views import *

urlpatterns = [

    path('', post_list, name="post_list"),
    path('category/<int:category_id>/', post_list_category, name="post_list_category"),
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('<int:post_id>/comment/', comment_list, name='comment_list'),
]