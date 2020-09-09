import random,os
import logging
from datetime import date
from django.core.cache import cache
from django.db.models import Q,F
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404,render, redirect
# from django.http import HttpResponse
from config.models import SideBar
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Post, Tag, Category,User,Favorite
from blog.forms.login import LoginForm
from django.http import HttpResponse

from django.urls import reverse
from django.contrib.auth import logout

# from comment.forms import CommentForm
# from comment.models import Comment
# from silk.profiling.profiler import silk_profile

# def post_list(request,category_id=None,tag_id=None):
#     # content = 'post_list category_id={category_id},tag_id={tag_id}'.format(
#     #     category_id=category_id,
#     #     tag_id=tag_id,
#     # )
#     # return HttpResponse(content)
#     tag = None
#     category = None
#     if tag_id:
#         post_list,tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list,category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#     context = {
#         'category':category,
#         'tag':tag,
#         'post_list':post_list,
#         'sidebars':SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request,'blog/list.html',context=context)


# def post_detail(request,post_id=None):
#     # return HttpResponse('detail')
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request,'blog/detail.html',context=context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'

logger = logging.getLogger(__name__)

# 新建类增加通用数据，分类导航，侧边栏，底部导航
class CommonViewMixin:
    # 12章
    # @silk_profile(name='get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        context.update(self.get_loginstatus())
        # context.update(self.get_favorites())
        # print('++++++',context)
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    # 分别列出导航及非导航category集合
    def get_navs(cls):
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

    def get_loginstatus(self):
        if self.request.session.get('token'):
            loginstatus = '已登录'
        else:
            loginstatus = '未登录'
        return {'loginstatus':loginstatus}

    # def get_favorites(self):
    #     if self.request.session.get('token'):
    #         token=self.request.session.get('token')
    #         user = User.obejcts.get(userToken=token)
    #         favorites = Favorite.objects.filter(userAccount=user.userAccount)
    #     return {'favorites':favorites}


# 对应post_list函数，作为主页模板基类，
# category,tag都从这里继承来处理多个URL的逻辑
class IndexView(CommonViewMixin, ListView):
    # queryset = Post.latest_posts()
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL).select_related('owner').select_related('category')
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


# 主页带category_id的URL处理
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        # print('context', context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

# 主页带tag_id参数的URL处理
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        # print("----------")
        # print("*****",**kwargs)
        context = super().get_context_data(**kwargs)
        # print('>>>>>', context)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

# 处理文章详情页URL
class PostDetailView(CommonViewMixin, DetailView):
    # queryset = Post.latest_posts()
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # 在get请求中添加处理pv,uv的函数
    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        # if request.session.get('token'):
        #     token = self.request.session.get('token')
        #     user = User.objects.get(userToken=token)
        #     print(request.META)
        #     blogid = request.META['PATH_INFO'].split('/')[2].split('.')[0]
        #     if 'changefavorite' in request.META['HTTP_REFERER']:
        #         favoriter = Favorite.objects.filter(userAccount=user.userAccount).get(blogid=blogid)
        #         print(favoriter.isDelete)
        #         favoriter.isDelete = True
        #         print(favoriter.isDelete)
        #         favoriter.save()
        self.handle_visited()
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        return response

    # 用于判断是否有缓存，如果没有，则进行＋1的操作，
    # 最后的几个条件语句是避免执行两次更新操作
    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid

        pv_key = 'pv:%s:%s' % (uid,self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key,1,1*60)

        uv_key = 'uv:%s:%s:%s' % (uid,str(date.today()),self.request.path)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key,1,24*60*60)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)

        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)

        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)



        # from django.db import connection
        # print(connection.queries)
        # return response
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form':CommentForm,
    #         'comment_list':Comment.get_by_target(self.request.path),
    #     })
    #     return context


def aurl(request):
    return render(request, 'blog/demo.html')

# 主页搜索及结果处理
class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        # print(context,'++++')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        # print(queryset)
        # print(keyword)
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

# 主页带owner_id的URL处理
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)



def login(request):
    #print("===",request.method)
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            nameid = f.cleaned_data['username']
            # print(nameid)
            pswd = f.cleaned_data['passwd']
            # print(pswd)
            try:
                user = User.objects.get(userAccount=nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:

                return redirect('/login/')
            token = random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session['username'] = user.userName
            request.session['token'] = user.userToken
            return redirect('/')
        else:
            return render(request, 'blog/login.html', {'title': '登录', 'form': f, 'error': f.errors})
    else:
        f = LoginForm()
        return render(request, 'blog/login.html', {'title': '登录', 'form': f})
        # return HttpResponse("hello login")

def register(request):
    # print("+++++",request.method)
    if request.method == 'POST':
        userAccount = request.POST.get('userAccount')
        userPasswd = request.POST.get('userPasswd')
        userName = request.POST.get('userName')
        userPhone = request.POST.get('userPhone')
        userAdderss = request.POST.get('userAddress')
        userRank = 0
        token = random.randrange(1,100000)
        userToken = str(token)
        f = request.FILES['userImg']
        userImg = os.path.join(settings.MEDIA_ROOT,userAccount+'.png')
        with open(userImg,'wb') as fp:
            for data in f.chunks():
                fp.write(data)
        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userRank,userToken,userImg)
        user.save()
        request.session['username'] = userName
        request.session['token'] = userToken
        return redirect('/')
    else:
        #print(settings.MEDIA_ROOT)
        return render(request,'blog/register.html',{'title':'注册'})



def newblog(request):
    render(request,'blog/newblog.html')

def quit(request):
    logout(request)
    # print("_____++++++")
    # return render(request,'blog/base.html')
    return redirect('/')

def Favoritelist(request):
    # print("_+_+_++_+++")
    token = request.session.get('token')
    # print(token)
    if token == None:
        return redirect(reverse('blog:index'))
    user = User.objects.get(userToken=token)
    # print('user',user)
    userid = user.userAccount
    favorites = Favorite.objects.filter(userAccount=userid).filter(isDelete=False)
    # print('favorites',favorites)
    bloglist = []
    for f in favorites:
        bloglist.append(Post.objects.get(id=f.blogid))
    # print('bloglist',bloglist)
    return render(request, 'blog/favoritelist.html',{'userid': userid, 'favorites': favorites, 'bloglist': bloglist})

def changefavorite(request,flag):
    # print('<><><><>')
    token = request.session.get('token')
    # print(token)
    if token==None:
        f = LoginForm()
        return render(request,'blog/login.html', {'title': '登录', 'form': f})
    # print(request.method)
    blogid = flag
    # print(blogid)
    user = User.objects.get(userToken=token)
    blog = Post.objects.get(id=blogid)
    if Favorite.objects.get(noRepeat=user.userAccount+blogid):
        favoriter = Favorite.objects.get(noRepeat=user.userAccount+blogid)
        if favoriter.isDelete == False:
            favoriter.isDelete = True
            favoriter.save()
            # print('+',favoriter.isDelete)
            return render(request, 'blog/uncollect.html', {'post': blog})
        else:
            favoriter.isDelete = False
            favoriter.save()
            # print('-',favoriter.isDelete)
            return render(request,'blog/collect.html', {'post': blog})
    else:
        favoriter = Favorite.createfavorite(user.userAccount,blogid,user.userAccount+blogid,False)
        favoriter.save()
        # print(blog.title)
        return render(request, 'blog/collect.html', {'post': blog})



