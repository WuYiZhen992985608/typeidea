import random,os
import operator
import logging
import mistune
from datetime import date
from django.core.cache import cache
from django.db.models import Q,F
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404,render, redirect
# from django.http import HttpResponse
from config.models import SideBar
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Post, Tag, Category,MyUser,Favorite
from blog.forms.login import LoginForm
from blog.forms.addpost import PostForm
from django.http import HttpResponse

from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.csrf import csrf_exempt
import pprint
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
            'hot_posts':self.get_hot_posts(),
        })
        # pprint.pprint(context)
        context.update(self.get_navs())
        # pprint.pprint(context)
        context.update(self.get_loginstatus())
        # pprint.pprint(context)
        # context.update(self.get_post_dict())
        # context.update(self.get_favorites())
        # print('++++++',context)
        # for k, v in context.items:
        #     print(k,':',v)
        # pprint.pprint(context)
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    def get_hot_posts(self):
        hot_posts = Post.hot_posts()
        hot_posts = hot_posts[:10]
        return hot_posts
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
            token = self.request.session.get('token')
            loginstatus = '已登录'
            try:
                user = MyUser.objects.get(userToken=token)
                userimg = user.userImg
                userimg = userimg[75:]
            except:
                user = '不存在'
        else:
            loginstatus = '未登录'
            user = '不存在'
            userimg = '不存在'
        return {'loginstatus':loginstatus,'user':user,'userimg':userimg}


    # def get_post_dict(self):
    #     postlist = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     post_dict = {}
    #     post_title_list = []
    #     post_id_list = []
    #     for i in postlist:
    #         post_title_list.append(i.title)
    #         post_id_list.append(i.id)
    #         post_dict.update(zip(post_title_list,post_id_list))
    #     print(post_dict)
    #     return post_dict
    # def get_favorites(self):
    #     if self.request.session.get('token'):
    #         token=self.request.session.get('token')
    #         user = MyUser.obejcts.get(userToken=token)
    #         favorites = Favorite.objects.filter(username=user.username)
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
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        return response

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.object.id
        # print(post_id)
        post_dict = {}
        post_title_list = []
        post_index_list = []
        # print('len',len(self.queryset))
        queryset_length = len(self.queryset)
        queryset_list = list(self.queryset)
        # print(queryset_list)
        post_index = queryset_list.index(self.object)
        # print('index',post_index)
        # if语句添加上下篇链接
        if post_index == queryset_length-1:
            post_title_list.append(self.queryset[post_index-1].title)
            post_index_list.append(self.queryset[post_index-1].id)
            post_title_list.append('前面没有了')
            post_index_list.append(post_index+1)
            mark = 2
            # print(post_index_list)
            # print(post_title_list)
            post_dict.update(zip(post_title_list, post_index_list))
            post_dict2 = sorted(post_dict.items(), key=operator.itemgetter(1), reverse=False)
            # print(post_dict2)
            # print(type(post_dict2))
            context.update({'post_list': post_dict2, 'mark': mark})
            # pprint.pprint(context)
        elif post_index == 0:
            post_title_list.append('后面没有了')
            post_index_list.append(-1)
            post_title_list.append(self.queryset[post_index+1].title)
            post_index_list.append(self.queryset[post_index+1].id)
            mark = 0
            # print(post_index_list)
            # print(post_title_list)
            post_dict.update(zip(post_title_list, post_index_list))
            post_dict2 = sorted(post_dict.items(), key=operator.itemgetter(1), reverse=False)
            # print(post_dict2)
            # print(type(post_dict2))
            context.update({'post_list': post_dict2, 'mark': mark})
            # pprint.pprint(context)
        else:
            post_title_list.append(self.queryset[post_index-1].title)
            post_index_list.append(self.queryset[post_index-1].id)
            post_title_list.append(self.queryset[post_index+1].title)
            post_index_list.append(self.queryset[post_index+1].id)
            mark = 1
            # print(post_index_list)
            # print(post_title_list)
            post_dict.update(zip(post_title_list, post_index_list))
            post_dict2 = sorted(post_dict.items(), key=operator.itemgetter(1), reverse=False)
            # print(post_dict2)
            # print(type(post_dict2))
            context.update({'post_list': post_dict2, 'mark': mark})
            # pprint.pprint(context)

        user = context['user']
        if type(user)!= str and self.object.owner.id == user.id:
            delete_post = 1
        else:
            delete_post = 0
        try:
            favoriter = Favorite.objects.filter(isDelete=False).get(noRepeat=str(user.username)+str(post_id))
            # print('=',favoriter.noRepeat)
        except:
            favoriter = None
        # print("self.get_sidebars",self.get_sidebars())
        context.update({'favoriter':favoriter,'delete_post':delete_post})
        # pprint.pprint(context)
        return context



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
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            encoded = make_password(password)
            if check_password(password,encoded):
                try:
                    user = MyUser.objects.get(username=username)
                    token = random.randrange(1, 100000)
                    user.userToken = str(token)
                    user.save()
                    request.session['username'] = username
                    request.session['token'] = str(token)
                    return redirect('/')
                except MyUser.DoesNotExist as e:
                    return redirect('/login/')
            else:
                return redirect('/login/')
        else:
            return render(request, 'blog/login.html', {'title': '登录', 'form': f, 'error': f.errors})
    else:
        f = LoginForm()
        return render(request, 'blog/login.html', {'title': '登录', 'form': f})
        # return HttpResponse("hello login")


def register(request):
    # print("+++++",request.method)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(password)
        password = make_password(password)
        # print(password)
        userPhone = request.POST.get('userPhone')
        userAdderss = request.POST.get('userAddress')
        userRank = 0
        token = random.randrange(1,100000)
        userToken = str(token)
        f = request.FILES['userImg']
        userImg = os.path.join(settings.MEDIA_ROOT,username+'.png')
        cleanStatus = True
        with open(userImg,'wb') as fp:
            for data in f.chunks():
                fp.write(data)
        user = MyUser.createuser(password,username,userPhone,userAdderss,userImg,userRank,userToken,cleanStatus)
        user.save()
        request.session['username'] = username
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
    user = MyUser.objects.get(userToken=token)
    # print('user',user)
    username = user.username
    favorites = Favorite.objects.filter(username=username).filter(isDelete=False)
    # print('favorites',favorites)
    bloglist = []
    for f in favorites:
        bloglist.append(Post.objects.get(id=f.blogid))
    # print('bloglist',bloglist)
    return render(request, 'blog/favoritelist.html',{'username': username, 'favorites': favorites, 'bloglist': bloglist})

# def changefavorite(request,flag):
#     # print('<><><><>')
#     token = request.session.get('token')
#     # print(token)
#     if token==None:
#         f = LoginForm()
#         return render(request,'blog/login.html', {'title': '登录', 'form': f})
#     # print(request.method)
#     blogid = flag
#     # print(blogid)
#     user = MyUser.objects.get(userToken=token)
#     blog = Post.objects.get(id=blogid)
#     try:
#         favoriter = Favorite.objects.get(noRepeat=user.username+blogid)
#         print('create',favoriter.noRepeat)
#         if favoriter.isDelete == False:
#             # print('-', request.META['HTTP_REFERER'])
#             # print('-', request.META['PATH_INFO'])
#             # print(request.META)
#             favoriter.isDelete = True
#             favoriter.save()
#             # print('+', favoriter.isDelete)
#             # return render(request, 'blog/uncollect.html', {'post': blog})
#             return render(request, 'blog/changefavorite.html', {'post': blog})
#         else:
#             favoriter.isDelete = False
#             favoriter.save()
#             # print('-', favoriter.isDelete)
#             # return render(request, 'blog/collect.html', {'post': blog})
#             return render(request, 'blog/changefavorite.html', {'post': blog})
#     except:
#         favoriter = Favorite.createfavorite(user.username,blogid,user.username+blogid,False)
#         favoriter.save()
#         # print(blog.title)
#         # return render(request, 'blog/collect.html', {'post': blog})
#         return render(request, 'blog/changefavorite.html', {'post': blog})

class ChangeFavorite(PostDetailView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    template_name = 'blog/changefavorite.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.pk_url_kwarg)
        post_id = self.object.id
        # print('=',post_id)
        favoriter = self.change_favorite(post_id)
        context.update({'favoriter':favoriter})
        # print('context',context)
        return context

    def change_favorite(self, post_id):
        # print('<><><><>')
        token = self.request.session.get('token')
        # print(token)
        if token == None:
            f = LoginForm()
            return render(self.request, 'blog/login.html', {'title': '登录', 'form': f})
        # print(request.method)
        user = MyUser.objects.get(userToken=token)
        try:
            favoriter = Favorite.objects.get(noRepeat=str(user.username) + str(post_id))
            # print('find', favoriter.noRepeat)
            if favoriter.isDelete == False:
                # print('-', request.META['HTTP_REFERER'])
                # print('-', request.META['PATH_INFO'])
                # print(request.META)
                favoriter.isDelete = True
                favoriter.save()
                # print('+', favoriter.isDelete)
                # return render(request, 'blog/uncollect.html', {'post': blog})
                return favoriter
            else:
                favoriter.isDelete = False
                favoriter.save()
                # print('-', favoriter.isDelete)
                # return render(request, 'blog/collect.html', {'post': blog})
                return favoriter
        except:
            favoriter = Favorite.createfavorite(user.username, post_id, str(user.username) + str(post_id), False)
            favoriter.save()
            # print(blog.title)
            # return render(request, 'blog/collect.html', {'post': blog})
            return favoriter

@csrf_exempt
def addpost(request):
    token = request.session.get('token')
    if token == None:
        return redirect('/login/')
    # print("+++")
    # print(request.method)
    # print('meta', request.META)
    try:
        user = MyUser.objects.get(userToken=token)
        if request.method == 'POST':
            # print('username',user.username)
            title = request.POST.get('title')
            # print('title', title)
            desc = request.POST.get('desc')
            # print('desc', desc)
            category = request.POST.get('category')
            # print(category)
            category_instance = Category.objects.get(name=category)
            # print(type(category_instance))
            # print(category_instance.id)
            status = request.POST.get('status')
            # print(status)
            writer = request.POST.get('writer')
            is_md = request.POST.get('is_md')
            if is_md:
                is_md = True
            else:
                is_md = False
            content_ck = request.POST.get('content_ck')
            # print('ck', content_ck)
            content_md = request.POST.get('content_md')
            # print('md', content_md)
            if is_md:
                content = content_md
            else:
                content = content_ck
            # p = Post.createpost(title, desc, content,status,category_instance.id,tag_instance.id,is_md,user.id)
            p = Post(title=title)
            # print(type(p))
            p.desc = desc
            p.content = content
            p.status = status
            p.is_md = is_md
            # print("+——")
            p.category_id = category_instance.id
            # print("_____+")
            p.owner_id = user.id
            p.writer = writer
            p.save()
            tag = request.POST.get('tag')
            # print(tag)
            if tag == "不添加标签":
                return redirect('/')
            else:
                try:
                    tag_instance = Tag.objects.get(name=tag)
                except:
                    tag_instance = Tag.createtag(tag, user)
                    # print("create tag")
                    tag_instance.save()
                # print(type(tag_instance))
                tag_instance_queryset = Tag.objects.filter(id=tag_instance.id)
                p.tag.add(*tag_instance_queryset)
                return redirect('/')
        else:
            # print('_+_+')
            # return render(request,'blog/addpost.html')
            categorylist = Category.objects.filter(status=Category.STATUS_NORMAL)
            taglist = Tag.objects.filter(status=Tag.STATUS_NORMAL)
            return render(request, 'blog/blogblock.html',
                          {'post_form': PostForm, 'categorylist': categorylist, 'taglist': taglist,'user':user})
    except MyUser.DoesNotExist as e:
        return redirect('/login/')
        # return HttpResponse('提交文章')


def deletepost(request,post_id):
    token = request.session.get('token')
    if token == None:
        return redirect('/login/')
    try:
        user = MyUser.objects.get(userToken=token)
        user_id = user.id
        post = Post.objects.get(id=post_id)
        if user.id == post.owner.id:
            # print(post.status)
            post.status = Post.STATUS_DELETE
            # print(post.status)
            post.save()
            return redirect('/')
        else:
            return redirect('/login/')
    except Post.DoesNotExist as e:
        return HttpResponse('meiyou')

