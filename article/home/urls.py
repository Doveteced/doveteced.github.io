from django.urls import path
<<<<<<< HEAD
=======

from home.helpers import set_language
>>>>>>> a8d18b23b80ec99c1d3244ee281b19dc054e7ea5
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_view, name="login_view"),
    path('register/', register_view, name="register_view"),
    path('add-blog/', add_blog, name="add_blog"),
    path('blog-detail/<slug>', blog_detail, name="blog_detail"),
<<<<<<< HEAD
    path('see-blog/', see_blog, name="see_blog"),
    path('blog-delete/<id>', blog_delete, name="blog_delete"),
    path('blog-update/<slug>/', blog_update, name="blog_update"),
    path('logout-view/', logout_view, name="logout_view"),
    path('verify/<token>/', verify, name="verify")
=======
    path('blogs/', see_blog, name="see_blog"),
    path('blog-delete/<id>', blog_delete, name="blog_delete"),
    path('blog-update/<slug>/', blog_update, name="blog_update"),
    path('featured/', featured_articles, name='featured_articles'),
    path('logout-view/', logout_view, name="logout_view"),
    path('verify/<str:token>/', verify, name='verify'),
    path('profile/', profile, name="profile"),
    path('author/<str:hashed_id>/', author, name='author_detail'),
    path('authors/', authors, name='authors'),
    path('about/', about, name="about_us"),
    path('services/', services, name="services"),
    path('team/', team, name="team"),
    path('advertise/', advertise, name="advertise"),
    path('advertise-with-us/', advertise_with_us, name="advertise_with_us"),
    path('search/', search, name="search"),
    path('category/<category>/', category, name="category"),
    path('tag/<tag>/', tag, name="tag_detail"),
    path('tags/', tags, name="tags"),
    path('like/<id>/', like, name="like"),
    path('dislike/<id>/', dislike, name="dislike"),
    path('comment/<str:post_id>/', add_comment, name="comment"),
    path('reply/<id>/', add_reply, name="reply"),
    path('delete-comment/<id>/', delete_comment, name="delete_comment"),
    path('delete-reply/<id>/', delete_reply, name="delete_reply"),
    path('edit-reply/<id>/', edit_reply, name="edit_reply"),
    path('edit-comment/<id>/', edit_comment, name="edit_comment"),
    path('edit-profile/', edit_profile, name="edit_profile"),
    path('change-password/', change_password, name="change_password"),
    path('forgot-password/', forget_password, name="forgot_password"),
    path('reset-password/<token>/', reset_password, name="reset_password"),
    path('privacy-policy/', privacy_policy, name="privacy_policy"),
    path('terms-and-conditions/', terms_and_conditions, name="terms_and_conditions"),
    path('cookie-policy/', cookie_policy, name="cookie_policy"),
    path('sitemap/', sitemap, name="sitemap"),
    path('robots.txt/', robots, name="robots"),
    path('ads.txt/', ads, name="ads"),
    path('contact-us/', contact_us, name="contact_us"),
    path('feedback/', feedback, name="feedback"),
    path('report/', report, name="report"),
    path('subscribe/', subscribe, name="subscribe"),
    path('unsubscribe/', unsubscribe, name="unsubscribe"),
    path('newsletter/', newsletter, name="newsletter"),
    path('newsletter-unsubscribe/', newsletter_unsubscribe, name="newsletter_unsubscribe"),
    path('set_language/', set_language, name='set_language'),

    path('help/', help_center, name='help_center'),
    path('help/faq/', faq, name='faq'),
    path('help/contact/', contact_us, name='contact'),

>>>>>>> a8d18b23b80ec99c1d3244ee281b19dc054e7ea5
]
