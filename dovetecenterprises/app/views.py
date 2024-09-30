from django.shortcuts import render

# Create your views here.
from django.template import loader
from .models import *

# Create your views here.


def index(request):
    page_title = "Dovetec Enterprises | Solving Workforce Complexities"
    return render(request, 'app/index.html', {'page_title': page_title})

def about(request):
    page_title = 'About Us! | Dovetec Enterprises'
    return render(request, 'app/about.html', {'page_title': page_title})
 
def contact(request):
    page_title = 'Contact Us! | Dovetec Enterprises'
    return render(request, 'app/contact.html', {'page_title': page_title})

def services(request):
    page_title = 'Our Services | Dovetec Enterprises'
    return render(request, 'app/services.html', {'page_title': page_title})

def portfolio(request):
    page_title = 'Our Portfolio | Dovetec Enterprises'
    return render(request, 'app/portfolio.html', {'page_title': page_title})

def portfolio_showcase(request):
    page_title = 'Portfolio Showcase | Dovetec Enterprises'
    return render(request, 'app/portfolio-case-studies-v1.html', {'page_title': page_title})


# Portfolio Massionary
def portfolio_massionry(request):
    page_title = 'Portfolio Massionry | Dovetec Enterprises'
    return render(request, 'app/portfolio-masonry.html', {'page_title': page_title})
# Case Studies
def case_study(request):
    page_title = 'Our Case Studies | Dovetec Enterprises'
    return render(request, 'app/portfolio-case-studies-v2.html', {'page_title': page_title})
# Join our team
def join_our_team(request):
    page_title = 'Join Us! | Dovetec Enterprises'
    return render(request, 'app/join-our-team.html', {'page_title': page_title})
# Product Demo
def product_demo(request):
    page_title = 'Request a Product Demo'
    return render(request, 'app/product-demo.html', {'page_title': page_title})

# Gallery
def gallery(request):
    page_title = 'Our Rich Gallery | Dovetec Enterprises'
    return render(request, 'app/gallery.html', {'page_title': page_title})

# Gallery
def products(request):
    page_title = 'Our Products | Dovetec Enterprises'
    return render(request, 'app/products.html', {'page_title': page_title})
