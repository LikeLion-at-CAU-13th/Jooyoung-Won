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

class CommentList(APIView):

    def get(self, request, post_id, format=None):
        comments = Comment.objects.all().filter(post__id = post_id) 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)