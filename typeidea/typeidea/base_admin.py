from django.contrib import admin



# 基类 BaseOwnerAdrnin 类帮我们完成两件事：
# 一是重写save方法，此时需要设置对象的owner;
# 二是重写 get queryset 方法，让列页在展示文章或者分类时只能展示当前用户的；
class BaseOwnerAdmin(admin.ModelAdmin):

    exclude = ('owner',)

    def get_queryset(self,request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_models(self,request,obj,form,change):
        print('<><><><><><><>')
        obj.owner = request.user
        print('owner',request.user)
        return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)