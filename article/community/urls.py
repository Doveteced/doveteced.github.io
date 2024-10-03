from django.urls import path
from .views import topic_list, topic_detail, post_detail, reply_detail, toggle_like, toggle_dislike

urlpatterns = [
    
    path('', topic_list, name='community'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('comment/<int:comment_id>/reply/', reply_detail, name='reply_detail'),
    path('post/<int:post_id>/like/', toggle_like, name='toggle_like'),
    path('post/<int:post_id>/dislike/', toggle_dislike, name='toggle_dislike'),
]
