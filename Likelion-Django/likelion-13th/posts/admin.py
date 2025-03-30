from django.contrib import admin
from .models import Post, PostCategory

#중간 테이블 커스터마이징. 보이기만 하도록.
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')  #리스트 화면에 보일 컬럼 지정
    readonly_fields = ('post', 'category')  #필드 수정 막기
    actions = None  #선택 삭제 버튼 숨기기

    def has_add_permission(self, request):
        return False  #추가 금지

    def has_change_permission(self, request, obj=None):
        return False  #수정 금지

    def has_delete_permission(self, request, obj=None):
        return False  #삭제 금지
    
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1 #기본 폼 1개

class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline] 

admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)