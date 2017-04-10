from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    # url(r'^$', views.public_index, name='public_index'),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^(?P<post_id>[0-9]+)/delete_album/$', views.delete_post, name='delete_post'),
]
