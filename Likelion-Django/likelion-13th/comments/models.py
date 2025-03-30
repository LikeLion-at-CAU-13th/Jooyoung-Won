from django.db import models
from posts.models import Post

class Comment(models.Model):

    id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=3)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return f"{self.post.title} - {self.writer}"
        #게시물 - 댓글 작성자
        #f는 Python의 f-string (formatted string literal) 문법
        #f를 붙이고, 중괄호 {} 안에 변수를 넣으면 그 값이 문자열 안에 자동으로 들어감