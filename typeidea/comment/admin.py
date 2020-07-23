from django.contrib import admin


from .models import Comment
from typeidea.custom_site import custom_site
# from typeidea.base_admin import BaseOwnerAdmin
# from .adminforms import CommentAdminForm
from django.utils.html import format_html
from django.urls import reverse




@admin.register(Comment,site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    # form = CommentAdminForm
    list_display = ('target','content','website','email','operator')
    # exclude = ['owner']
    fieldsets = (
        ('基础配置', {
            'fields': (
                'nickname',
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                # 'comment_desc'
                'content',
            ),
        }),
    )
    # 管理员审核评论是否展示
    def operator(self,obj):
        return format_html(
            '<a href="/admin/comment/comment/{}/change/">编辑</a>'.format(obj.id),
            # '<a href="{}">编辑</a>',
            # reverse('cus_admin:comment',args=(obj.id,))
        )
    operator.short_description = '操作'

