from django import forms
from froala_editor.widgets import FroalaEditor
from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_verified', 'token']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        widgets = {
            'content': FroalaEditor(),
        }