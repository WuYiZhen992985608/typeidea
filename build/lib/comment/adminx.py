import xadmin

from .models import Comment

from django.utils.html import format_html




@xadmin.sites.register(Comment)
class CommentAdmin:
    # form = CommentAdminForm
    list_display = ('target','content','website','email','operator')
    # 管理员审核评论是否展示
    def operator(self,obj):
        return format_html(
            '<a href="/admin/comment/comment/{}/change/">编辑</a>'.format(obj.id),
            # '<a href="{}">编辑</a>',
            # reverse('cus_admin:comment',args=(obj.id,))
        )
    operator.short_description = '操作'

