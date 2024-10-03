import hashlib
import uuid
import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from home.form import ArticleForm
from .models import Profile, Article, Comment, Reply, Tag
from django.conf import settings

def unhash_author_id(hashed_id):
    """Reverse the hashing process of the author_id."""
    for user in User.objects.all():
        if hashlib.md5(str(user.id).encode()).hexdigest() == hashed_id:
            return user.id
    return None
def authors(request):
    authors = Profile.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context)

def author(request, hashed_id):
    # Fetch the author's profile using the hashed_id directly
    profile = get_object_or_404(Profile, user__id=hashed_id)
    
    # Fetch articles written by the author
    articles_by_author = Article.objects.filter(author=profile)
    
    # Fetch related articles based on tags or categories
    related_articles = Article.objects.filter(tags__in=articles_by_author.values('tags')).exclude(author=profile)
    
    # Fetch all tags associated with the author's articles for display
    author_tags = Tag.objects.filter(article__author=profile).distinct()

    context = {
        'author': profile.user,
        'articles_by_author': articles_by_author,
        'related_articles': related_articles,
        'author_tags': author_tags,
    }

    return render(request, 'author.html', context)

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})
            
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email already exists'})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            
            token = str(uuid.uuid4())
            otp = generate_otp()
            profile = Profile.objects.create(user=user, token=token, is_verified=False)

            verification_link = request.build_absolute_uri(f'/verify/{token}/')
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_link}\nYour OTP is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            profile.otp = otp
            profile.save()

            return redirect('/login/')
        
        except Exception as e:
            print(e)
            return render(request, 'register.html', {'error': 'Something went wrong'})
    
    return render(request, 'register.html')

def verify(request, token):
    profile_obj = get_object_or_404(Profile, token=token)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        if profile_obj.otp == entered_otp:
            profile_obj.is_verified = True
            profile_obj.user.is_active = True
            profile_obj.user.save()
            profile_obj.save()
            return redirect('/login/')
        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP'})

    profile_obj.is_verified = True
    profile_obj.user.is_active = True
    profile_obj.user.save()
    profile_obj.save()
    return redirect('/login/')

def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    context = {'blogs': Article.objects.all()}
    return render(request, 'home/index.html', context)

def login_view(request):
    return render(request, 'login.html')

def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = get_object_or_404(Article, slug=slug)
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)

def featured_articles(request):
    featured_articles = Article.objects.filter(featured=True)
    context = {
        'featured_articles': featured_articles
    }
    return render(request, 'community/featured_articles.html', context)

def see_blog(request):
    context = {}
    try:
        blog_objs = Article.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)

def add_blog(request):
    context = {'form': ArticleForm}
    try:
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

                blog_obj = Article.objects.create(
                    user=user, title=title,
                    content=content, image=image
                )
                return redirect('/add-blog/')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)

def blog_update(request, slug):
    context = {}
    try:
        blog_obj = get_object_or_404(Article, slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = ArticleForm(initial=initial_dict)
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']
                blog_obj.title = title
                blog_obj.content = content
                blog_obj.image = image
                blog_obj.save()

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)

def blog_delete(request, id):
    try:
        blog_obj = get_object_or_404(Article, id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')

def render_template(request, template_name, context=None):
    return render(request, template_name, context or {})

def profile(request):
    return render_template(request, 'profile.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        send_mail(
            f'Contact Form Submission from {name}',
            f'Message: {message}\n\nFrom: {email}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        
        return render(request, 'contact.html', {'success': 'Your message has been sent successfully!'})
    
    return render(request, 'contact.html')

def about(request):
    return render_template(request, 'about_us.html')

def services(request):
    return render_template(request, 'services.html')

def team(request):
    return render_template(request, 'team.html')

def advertise(request):
    return render_template(request, 'advertise.html')

from django.shortcuts import render
from .models import Article

def search(request):
    query = request.GET.get('q', '')
    context = {
        'query': query,  # Include the search query in the context
        'articles': []   # Initialize as an empty list
    }
    
    if query:
        # Search articles by title or content
        context['articles'] = Article.objects.filter(
            title__icontains=query
        ) | Article.objects.filter(
            content__icontains=query
        ).distinct()  # Use distinct() to avoid duplicate results

    return render(request, 'search.html', context)



def category(request, category):
    context = {
        'articles': Article.objects.filter(category=category)
    }
    return render_template(request, 'category.html', context)

def tag(request, tag):
    context = {
        'articles': Article.objects.filter(tags__name=tag)
    }
    return render_template(request, 'tag.html', context)

def tags(request):
    context = {
        'tags': Tag.objects.all()
    }
    return render_template(request, 'tags.html', context)

@login_required
def like(request, id):
    article = get_object_or_404(Article, id=id)
    article.likes += 1
    article.save()
    return redirect('article_detail', slug=article.slug)

@login_required
def dislike(request, id):
    article = get_object_or_404(Article, id=id)
    article.likes -= 1
    article.save()
    return redirect('article_detail', slug=article.slug)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all()
    return render_template(request, 'article_detail.html', {'article': article, 'comments': comments})



from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache

@login_required
def add_comment(request, slug):
    """Add a comment to an article."""
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(article=article, user=request.user, content=content)
        messages.success(request, 'Comment added successfully.')
        return redirect('article_detail', slug=slug)
    return redirect('article_detail', slug=slug)

@login_required
def add_reply(request, comment_id):
    """Add a reply to a specific comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Reply.objects.create(comment=comment, user=request.user, content=content)
        messages.success(request, 'Reply added successfully.')
        return redirect('article_detail', slug=comment.article.slug)
    return redirect('article_detail', slug=comment.article.slug)

@login_required
def delete_reply(request, id):
    """Delete a specific reply."""
    reply = get_object_or_404(Reply, id=id)
    if request.user == reply.user:
        reply.delete()
        messages.success(request, 'Reply deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this reply.')
    
    return redirect('article_detail', slug=reply.comment.article.slug)

@login_required
def edit_reply(request, id):
    """Edit a specific reply."""
    reply = get_object_or_404(Reply, id=id)
    
    if request.method == 'POST':
        if request.user == reply.user:
            reply.content = request.POST.get('content')
            reply.save()
            messages.success(request, 'Reply updated successfully.')
            return redirect('article_detail', slug=reply.comment.article.slug)
        else:
            messages.error(request, 'You do not have permission to edit this reply.')
    
    return render(request, "edit_reply.html", {'reply': reply})

@login_required
def delete_comment(request, comment_id):
    """Delete a specific comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    return redirect('article_detail', slug=comment.article.slug)

@login_required
def edit_comment(request, comment_id):
    """Edit a specific comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.user == comment.user:
            comment.content = request.POST.get('content')
            comment.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('article_detail', slug=comment.article.slug)
        else:
            messages.error(request, 'You do not have permission to edit this comment.')

    return render(request, "edit_comment.html", {'comment': comment})

@login_required
def edit_profile(request):
    """Edit user profile."""
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, "edit_profile.html")

@login_required
def change_password(request):
    """Change user password with verification."""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully.')
        return redirect('profile')

    return render(request, "change_password.html")

def send_otp(user):
    """Generate and send OTP to user's email."""
    otp = str(random.randint(100000, 999999))
    user.profile.otp = otp
    user.profile.otp_timestamp = timezone.now()
    user.profile.save()

    send_mail(
        'Your OTP Code',
        f'Your OTP code is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def forget_password(request):
    """Handle forgotten password by sending a reset link or OTP."""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)

        # Rate limiting for OTP requests
        otp_request_count = cache.get(f'otp_request_count_{email}', 0)
        if otp_request_count >= 5:
            messages.error(request, 'Too many requests. Please try again later.')
            return redirect('forget_password')

        # Generate and send OTP
        send_otp(user)

        # Increment the request count
        cache.set(f'otp_request_count_{email}', otp_request_count + 1, timeout=3600)  # Reset after 1 hour
        
        messages.success(request, 'An OTP has been sent to your email.')
        return redirect('verify_otp', email=email)

    return render(request, "forget_password.html")

def verify_otp(request, email):
    """Verify the OTP sent to user's email."""
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = get_object_or_404(User, email=email)
        profile = user.profile

        if profile.otp == otp:
            if not profile.is_otp_expired():
                # Clear the OTP after successful verification
                profile.otp = None
                profile.otp_timestamp = None
                profile.save()
                messages.success(request, 'OTP verified successfully. You can reset your password now.')
                return redirect('reset_password', email=email)
            else:
                messages.error(request, 'OTP has expired. Please request a new OTP.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, "verify_otp.html", {'email': email})

def reset_password(request, email):
    """Reset the user's password."""
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password', email=email)

        user = get_object_or_404(User, email=email)
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Your password has been reset successfully.')
        return redirect('login')

    return render(request, "reset_password.html", {'email': email})

# Additional pages

def privacy_policy(request):
    return render_template(request, "privacy_policy.html")

def terms_and_conditions(request):
    return render_template(request, "terms_and_conditions.html")

def cookie_policy(request):
    return render_template(request, "cookie_policy.html")

def sitemap(request):
    return render_template(request, "sitemap.html")

def robots(request):
    return render_template(request, "robots.html")

def ads(request):
    return render_template(request, "ads.html")

def advertise_with_us(request):
    return render_template(request, "advertise_with_us.html")

def feedback(request):
    return render_template(request, "feedback.html")

def report(request):
    return render_template(request, "report.html")

def subscribe(request):
    return render_template(request, "subscribe.html")

def unsubscribe(request):
    return render_template(request, "unsubscribe.html")

def newsletter(request):
    return render_template(request, "newsletter.html")

def newsletter_unsubscribe(request):
    return render_template(request, "newsletter_unsubscribe.html")

def help_center(request):
    return render_template(request, "help_center.html")

def faq(request):
    return render_template(request, "faq.html")
