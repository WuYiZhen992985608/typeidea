# import requests
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from .adminforms import PostAdminForm
from .models import Post,Category,Tag
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site

# from django.contrib.auth import get_permission_codename
# PERMISSION_API = "http://permission.sso.com/has_perm?user={}&perm_code={}"



# 分类编辑页面增加文章编辑功能
class PostInline(admin.TabularInline):
    # 文章可编辑的项目
    fields = ('title','desc')
    # 显示1行可编辑对象
    extra = 1
    model = Post

# 定制 site 来实现一个系统对外提供多套 dmin 后台的逻辑
@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]
    # 展示category的各项内容
    list_display = ('name','status','is_nav','created_time','post_count')
    # 可编辑的category各项内容
    fields = ('name','status','is_nav')

    # 展示该分类下有多少篇文章
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    # 返回要展示的内查询用的id,侧边栏显示
    def lookups(self,request,model_admin):
        # 只提取id和name字段
        return Category.objects.filter(owner=request.user).values_list('id','name')

    # 根据URL Query的内容返回列表页数据集合
    def queryset(self,request,queryset):
        # 比如URL最后的Query是?owner_category ＝1，那么这里拿self.value()就是1
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # 将desc字段展示更改为textarea
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','owner','operator'
    ]
    list_display_links = []

    # 配置页面过滤器，需要通过哪些字段来过滤列表页
    list_filter = [CategoryOwnerFilter,]
    # 设置搜索字段
    search_fields = ['title','category__name']
    # 保存、编辑、编辑并新建按钮是否在顶部展示
    save_on_top = False
    # 上下各有一个动作按钮
    actions_on_top = True
    actions_on_bottom = True

    # exclude = ('owner',)
    fields = (
        ('category','title'),
        'desc',
        'status',
        'content',
        'tag',
    )
    # fieldsets = (
    #     ('基础配置',{
    #         'description':'基础配置描述',
    #         'fields':(
    #             ('title','category'),
    #             'status',
    #             'owner',
    #         ),
    #     }),
    #     ('内容',{
    #         'fields':(
    #             'desc',
    #             'content',
    #         ),
    #     }),
    #     ('额外信息',{
    #         'classes':('wide',),
    #         'fields':('tag',),
    #     })
    # )
    # 设置tag横向展示
    # filter_vertical = ('tag',)
    filter_horizontal = ('tag',)

    # def has_add_permission(self,request):
    #     opts = self.opts
    #     codename = get_permission_codename('add',opts)
    #     perm_code = "%s.%s" % (opts.app_label,codename)
    #     resp = requests.get(PERMISSION_API.format(request.user.username,perm_code))
    #     if resp_status_code == 200:
    #         return True
    #     else:
    #         return False

    # 自定义方法，用来设置文章编辑入口
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'


    # def save_models(self,reqeust,obj,form,change):
    #     obj.owner = request.user
    #     return super(PostAdmin,self).save_model(request,obj,form,change)
    #
    # def get_queryset(self,request):
    #     qs = super(PostAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    class Media:
        css = {
            'all':('https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.0.0/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.0.0/js/bootstrap.bundle.js',)

# 日志记录显示
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']

