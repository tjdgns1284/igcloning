from django import forms
from .models import Comment,Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['image' , 'content',]
        read_only_fields = ['likeusers']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]
        read_only_fields = ['likeusers']
