from django.urls import path
from .views import topic_list, topic_detail, post_detail, toggle_like, toggle_dislike
from home.views import add_comment, add_reply

urlpatterns = [
   
    path('', topic_list, name='community'),
    path('topic/<slug:topic_slug>/', topic_detail, name='topic_detail'),
    path('post/<slug:post_slug>/', post_detail, name='post_detail'),
    path('post/<slug:post_slug>/like/', toggle_like, name='toggle_like'),
    path('post/<slug:post_slug>/dislike/', toggle_dislike, name='toggle_dislike'),
    path('like/<slug:post_slug>/', toggle_like, name='toggle_like'),
    path('dislike/<slug:post_slug>/', toggle_dislike, name='toggle_dislike'),
    path('comment/<slug:post_slug>/', add_comment, name='add_comment'),
    path('reply/', add_reply, name='add_reply'),
]
