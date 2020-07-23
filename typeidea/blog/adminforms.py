from django import forms

# 将desc字段展示更改为textarea
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)

