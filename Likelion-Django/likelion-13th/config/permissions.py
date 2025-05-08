from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from django.utils import timezone

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Request가 safe method라면 (get 등) 바로 true를 반환해 모두 볼 수 있도록 함 
        if request.method in SAFE_METHODS: 
            return True
        # 나머지 요청은 본인만 가능하도록
        print(f"obj.user = {obj.user}, request.user = {request.user}")
        return obj.user == request.user
    
class IsTimeNotLate(BasePermission):
    def has_permission(self, request, view):
        # 한국 시간대로 변환
        current_time = timezone.localtime(timezone.now())
        if current_time.hour >= 22 or current_time.hour < 7:
            print(f"오후 10시부터 오전 7시까지 모든 활동 금지. 현재 시간: {current_time}")
            return False 
        return True
