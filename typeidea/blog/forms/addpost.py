# 文件: comment/forms.py
import mistune
from django import forms

from ..models import Category,Tag,Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete

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


class PostForm(forms.Form):
    title = forms.CharField(
        label = '标题',
        max_length = 255,
        widget = forms.widgets.Input(
            attrs ={'class':'form-control','style':"width: 80%;"}
        )
    )
    desc = forms.CharField(
        label = '摘要',
        max_length = 1024,
        widget=forms.widgets.Input(
            attrs={'rows':6,'cols':60,'class':'form-control'}
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    content = forms.CharField(
        label = '正文',
        widget = forms.widgets.Textarea(
            attrs = {'rows':10,'cols':60,'class':'form-control'}
        )
    )

    class Meta:
        model = Post
        fields = ('category','tag','title','desc','content','status',
                  'is_md','content_ck','content_md',
                  )
    def __init__(self,instance=None,initial=None,**kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content
        super().__init__(instance=instance,initial=initial,**kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name,'必填项!')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js',)
