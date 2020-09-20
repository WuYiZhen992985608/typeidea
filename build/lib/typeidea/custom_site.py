from django.contrib.admin import AdminSite


# 定制 site 来实现一个系统对外提供多套 dmin 后台的逻辑
class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = '管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')