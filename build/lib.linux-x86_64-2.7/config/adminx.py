import xadmin
from .models import Link,SideBar
from typeidea.base_admin import BaseOwnerAdmin

# 展示友链信息
@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title','href','status','weight','created_time','owner')
    fields = ('title','href','status','weight')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)

# 展示侧边栏信息
@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title','display_type','content','created_time')
    fields = ('title','display_type','content')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(SideBarAdmin,self).save_model(request,obj,form,change)
