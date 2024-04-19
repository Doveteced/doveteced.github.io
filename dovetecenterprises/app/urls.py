import os
from django.urls import path
from . import views

# create url patterns for the main app
urlpatterns = [
    path('', views.index, name='Home'),
    path('about/', views.about, name='About Us!'),
    path('contact/', views.contact, name='COntact Us'),
    path('services/', views.services, name='Our Services'),
    path('portfolio/', views.portfolio, name='Our Portfolio'),
    path('portfolio-showcase/', views.portfolio_showcase, name='Our Portfolio Showcase'),
    path('portfolio-massionry/', views.portfolio_massionry, name='Our Portfolio Massionry'),
    path('case-study/', views.case_study, name='Our Case Studies'),
    path('join-our-team/', views.join_our_team, name='Join Our Team'),
    path('product-demo/', views.product_demo, name=' Request Product Demo'),
    path('gallery/', views.gallery, name=' Our Rich Gallery'),
    path('products/', views.products, name=' Our Products'),
]

