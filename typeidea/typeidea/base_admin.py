from django.contrib import admin



# 基类 BaseOwnerAdrnin 类帮我们完成两件事：
# 一是重写save方法，此时需要设置对象的owner;
# 二是重写 get queryset 方法，让列页在展示文章或者分类时只能展示当前用户的；
class BaseOwnerAdmin(object):

    exclude = ('owner',)

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()