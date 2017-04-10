from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_author', 'post_title', 'post_catagory', 'post_logo', 'post_content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_content']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
