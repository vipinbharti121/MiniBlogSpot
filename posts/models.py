from django.contrib.auth.models import Permission, User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, default=1)
    post_author = models.CharField(max_length=250)
    post_title = models.CharField(max_length=500)
    post_catagory = models.CharField(max_length=100)
    post_logo = models.FileField()
    post_content = models.TextField(max_length=6000)
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.post_title + ' - ' + self.post_author


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=100, default='Anonymous')
    comment_content = models.TextField(max_length=700)
    comment_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.comment_content
