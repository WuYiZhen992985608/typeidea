# 文件: comment/forms.py
import mistune
from django import forms

from blog.models import Post

# 文章下面展示评论区
# class PostForm(forms.ModelForm):
#     nickname = forms.CharField(
#         label = '昵称',
#         max_length = 50,
#         widget = forms.widgets.Input(
#             attrs ={'class':'form-control','style':"width: 60%;"}
#         )
#     )
#     email = forms.CharField(
#         label = 'Email',
#         max_length = 50,
#         widget=forms.widgets.EmailInput(
#             attrs={'class':'form-control','style':"width: 60%;"}
#         )
#     )
#     website = forms.CharField(
#         label = '网站',
#         max_length = 100,
#         widget = forms.widgets.URLInput(
#             attrs= {'class':'form-control','style':"width: 60%;"}
#         )
#     )
#     content = forms.CharField(
#         label = '内容',
#         max_length = 500,
#         widget = forms.widgets.Textarea(
#             attrs = {'rows':6,'cols':60,'class':'form-control'}
#         )
#     )
#     # 控制评论长度
#     def clean_content(self):
#         content = self.cleaned_data.get('content')
#         if len(content) < 10:
#             raise forms.ValidationError('内容长度怎么能这么短呢!')
#         content = mistune.markdown(content)
#         return content
#
#     class Meta:
#         model = Comment
#         fields = ['nickname','email','website','content']


# class PostForm(forms.Form):
#     title = forms.CharField(
#         label = '标题',
#         max_length = 255,
#         widget = forms.widgets.Input(
#             attrs ={'class':'form-control','style':"width: 80%;"}
#         )
#     )
#     desc = forms.CharField(
#         label = '摘要',
#         max_length = 1024,
#         widget=forms.widgets.Input(
#             attrs={'rows':6,'cols':60,'class':'form-control'}
#         )
#     )

    # content_html = forms.TextField(
    #     label = '正文',
    #     widget = forms.widgets.Textarea(
    #         attrs = {'rows':10,'cols':60,'class':'form-control'}
    #     )
    # )


