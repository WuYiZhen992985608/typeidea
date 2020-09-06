# import requests
import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row,Fieldset,Container

from django.urls import reverse
from django.utils.html import format_html


from .adminforms import PostAdminForm
from .models import Post,Category,Tag
from typeidea.base_admin import BaseOwnerAdmin



# 分类编辑页面增加文章编辑功能
class PostInline:
    # 文章可编辑的项目
    form_layout = (
        Container(
            Row('title','desc'),
        )
    )
    # 显示1行可编辑对象
    extra = 1
    model = Post

# 定制 site 来实现一个系统对外提供多套 dmin 后台的逻辑
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline,]
    # 展示category的各项内容
    list_display = ('name','status','is_nav','created_time','post_count')
    # 可编辑的category各项内容
    fields = ('name','status','is_nav')

    # 展示该分类下有多少篇文章
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户分类"""

    # 确认字段是否需要被当前的过滤器处理
    @classmethod
    def test(cls,field,request,params,model,admin_view,field_path):
        return field.name == 'cateogry'

    def __init__(self,field,request,params,model,model_admin,field_path):
        super().__init__(field,request,params,model,model_admin,field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id','name')


manager.register(CategoryOwnerFilter,take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # 将desc字段展示更改为textarea
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','owner','operator'
    ]
    list_display_links = []

    # 配置页面过滤器，需要通过哪些字段来过滤列表页
    list_filter = ['category',]
    # 设置搜索字段
    search_fields = ['title','category__name']
    # 保存、编辑、编辑并新建按钮是否在顶部展示
    save_on_top = False
    # 上下各有一个动作按钮
    actions_on_top = True
    actions_on_bottom = True

    exclude = ['owner']
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )
    # 设置tag横向展示
    # filter_vertical = ('tag',)
    # filter_horizontal = ('tag',)


    # 自定义方法，用来设置文章编辑入口
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'



    # @property
    # def get_media(self):
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     })
    #     return media


