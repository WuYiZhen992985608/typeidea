import mistune
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property



class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )

    name = models.CharField(max_length=50,verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
    # category是依附于user的，所有一个category只能属于一个user,参考page87数据关系模型；
    owner = models.ForeignKey(User,verbose_name='作者',on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name




class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者',on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'
        ordering = ['-id']

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content = models.TextField(verbose_name='正文',help_text='正文必须为MarkDown格式')
    content_html = models.TextField(verbose_name="正文html代码",blank=True,editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    is_md = models.BooleanField(default=True,verbose_name="markdown语法")
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    owner = models.ForeignKey(User,verbose_name='作者',on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        # 按post生成id的逆序排列，即是最新文章靠前的排序
        ordering = ['-id']

    def __str__(self):
        return self.title

    # post内容保存为html格式，便于提取展示
    def save(self,*args,**kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        # print('content',self.owner_id)
        # print('content',self.content)
        # print('content_html',self.content_html)
        super().save(*args,**kwargs)

    # 根据标签获取文章
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        # try语句没有发生任何异常时执行else语句
        else:
            # 针对一对多的数据库模型，使用selected_related解决外键产生的N+1次查询的问题
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')
        return post_list,tag


    # 根据分类获取文章
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')

        return post_list,category


    # def latest_posts(cls,with_related=True):
    @classmethod
    def latest_posts(cls,with_related=True):
        # 获取状态为1的文章，默认按id倒序，也是时间倒序输出，以下两句等效
        # queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('owner','category')
        return queryset

    # 获取最热文章，根据热度从大到小排列
    @classmethod
    def hot_posts(cls):
        result = cache.get('hot_posts')
        if not result:
            result = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
            cache.set('hot_posts',result,10*60)
        return result


    # 把返回的数据绑定到实例上，不用每次都去执行tags中的代码；
    @cached_property
    # 在模型中增加属性来输出配置好的tags
    def tags(self):
        tgs = ','.join(self.tag.values_list('name',flat=True))
        print('tgstgstgs',tgs)
        return tgs

class User(models.Model):
    userAccount = models.CharField(max_length=20,unique=True)
    userPasswd = models.CharField(max_length=20)
    userName = models.CharField(max_length=20)
    userPhone = models.CharField(max_length=20)
    userAdderss = models.CharField(max_length=100)
    userImg = models.CharField(max_length=150)
    userRank = models.IntegerField()
    userToken = models.CharField(max_length=200)
    cleanStatus = models.BooleanField(default=True,verbose_name="注销")
    @classmethod
    def createuser(cls,account,passwd,name,phone,adderss,img,rank,token,clean_status):
        u = cls(userAccount= account,userPasswd=passwd,userName=name,userPhone=phone,userAdderss=adderss,userImg=img,userRank=rank,userToken=token,cleanStatus=clean_status)
        return u

class Favorite(models.Model):
    userAccount = models.CharField(max_length=20)
    blogid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)
    noRepeat = models.CharField(max_length=30,default=1)
    @classmethod
    def createfavorite(cls,userAccount,blogid,noRepeat,isDelete):
        f = cls(userAccount=userAccount,blogid=blogid,noRepeat=noRepeat,isDelete=isDelete)
        return f