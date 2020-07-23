# from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm

# 通过view层把评论的数据传递到模板层
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self,request,*args,**kwargs):
        comment_form = CommentForm(request.POST)
        print(request.POST)
        target = request.POST.get('target')

        # 验证并保存数据，并返回到文章页面
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        # 如果校验失败，仍然展示到评论结果页
        context = {
            'succeed':succeed,
            'form':comment_form,
            'target':target,
        }
        return self.render_to_response(context)

