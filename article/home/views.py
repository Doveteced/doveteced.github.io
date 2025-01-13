import hashlib
import logging
import random
import string
import uuid
from django.core.cache import cache
from datetime import datetime, timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


from community.forms import CommentForm
from community.models import Post
from home.form import ArticleForm
from .models import Article, Comment, Profile, Reply, Tag

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
            
            # Render the verification email template
            email_context = {
                'verification_link': verification_link,
            }
            message = render_to_string('verify_account.html', email_context)

            send_mail(
                'Verify your email',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message  # Send the HTML version
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
            return render(request, 'verify_email.html', {'error': 'Invalid OTP'})

    # If the request is a GET, automatically verify the user
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
    return render(request, 'index.html', context)

def login_view(request):
    return render(request, 'login.html')

def blog_detail(request, slug):
    context = {}
    try:
        article_obj = get_object_or_404(Article, slug=slug)
        context['article_obj'] = article_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)

def featured_articles(request):
    """
    View to display featured articles.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with featured articles.
    """
    featured_articles = Article.objects.filter(featured=True)
    context = {
        'featured_articles': featured_articles
    }
    return render(request, 'forum/featured_articles.html', context)

def trending_articles(request):
    """
    View to display trending articles based on views.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with trending articles.
    """
    trending_articles = Article.objects.order_by('-views')[:10]
    context = {
        'trending_articles': trending_articles
    }
    return render(request, 'forum/trending_articles.html', context)

def latest_articles(request):
    """
    View to display the latest articles based on creation date.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with the latest articles.
    """
    latest_articles = Article.objects.order_by('-created_at')[:10]
    context = {
        'latest_articles': latest_articles
    }
    return render(request, 'latest_articles.html', context)

def popular_articles(request):
    """
    View to display popular articles based on likes.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with popular articles.
    """
    popular_articles = Article.objects.order_by('-likes')[:10]
    context = {
        'popular_articles': popular_articles
    }
    return render(request, 'forum/popular_articles.html', context)

def most_commented_articles(request):
    """
    View to display the most commented articles.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with the most commented articles.
    """
    most_commented_articles = Article.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:10]
    context = {
        'most_commented_articles': most_commented_articles
    }
    return render(request, 'forum/most_commented_articles.html', context)

def random_articles(request):
    """
    View to display random articles.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with random articles.
    """
    random_articles = Article.objects.order_by('?')[:10]
    context = {
        'random_articles': random_articles
    }
    return render(request, 'forum/random_articles.html', context)



# Set up logging
logger = logging.getLogger(__name__)

@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def see_blog(request):
    context = {}
    try:
        # Fetch blog articles for the logged-in user
        article_objs = Article.objects.filter(user=request.user)
        context['article_objs'] = article_objs

        # Fetch all categories and tags for the sidebar
        all_categories = Article.objects.values_list('category', flat=True).distinct()
        all_tags = Tag.objects.all()
        context['all_categories'] = all_categories
        context['all_tags'] = all_tags

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching blog articles: {e}")
        context['error'] = "An error occurred while fetching your blog articles. Please try again later."

    return render(request, 'see_blog.html', context)

def add_blog(request):
    context = {'form': ArticleForm()}
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Include files in the form instance
        
        if form.is_valid():
            try:
                article_obj = form.save(commit=False)  # Don't save to the database yet
                article_obj.user = request.user  # Assign the user
                article_obj.save()  # Now save the blog object

                # Redirect to the article detail page after successful creation
                return redirect('article_detail', slug=article_obj.slug)  # Make sure this URL is defined in your urls.py
            
            except Exception as e:
                print(f"Error adding blog: {e}")
                context['error'] = "An error occurred while adding the blog. Please try again."

        # If the form is not valid, pass it back to the context for rendering
        context['form'] = form

    return render(request, 'add_blog.html', context)


def blog_update(request, slug):
    context = {}
    try:
        article_obj = get_object_or_404(Article, slug=slug)

        if article_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': article_obj.content}
        form = ArticleForm(initial=initial_dict)
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']
                article_obj.title = title
                article_obj.content = content
                article_obj.image = image
                article_obj.save()

        context['article_obj'] = article_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)

def blog_delete(request, id):
    try:
        article_obj = get_object_or_404(Article, id=id)

        if article_obj.user == request.user:
            article_obj.delete()

    except Exception as e:
        print(e)

    return redirect('see_blog')

def render(request, template_name, context=None):
    return render(request, template_name, context or {})

def profile(request):
    return render(request, 'profile.html')

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
    return render(request, 'about_us.html')

def services(request):
    return render(request, 'services.html')

def team(request):
    return render(request, 'team.html')

from django.shortcuts import render

def advertise(request):
    return render(request, 'advertise.html')



def search(request):
    """
    Handles the search functionality for articles.

    This view function retrieves the search query from the request's GET parameters,
    performs a case-insensitive search on the title and content of articles, and
    returns the results to the 'search.html' template.

    Args:
        request (HttpRequest): The HTTP request object containing the search query.

    Returns:
        HttpResponse: The rendered 'search.html' template with the search query and
                      the list of articles matching the search criteria.

    Context:
        query (str): The search query string.
        articles (Page): The paginated page object containing the list of articles
                         matching the search criteria.
    """
    query = request.GET.get('q', '')  # Retrieve the search query from GET parameters
    articles = Article.objects.none()  # Initialize an empty queryset to avoid errors

    if query:
        # Use Q objects to perform a case-insensitive search on the title and content fields
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()  # Use distinct() to eliminate duplicate entries

    # Paginate the results, displaying 10 articles per page
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page', 1)  # Default to the first page if no page number is specified
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    # Prepare context data to be passed to the template
    context = {
        'query': query,
        'articles': page_obj,  # Pass the paginated articles
    }

    # Render the search results page with the context
    return render(request, 'search.html', context)

def category(request, category):
    """
    Handles the request to display articles belonging to a specific category.

    Args:
        request (HttpRequest): The HTTP request object.
        category (str): The category of articles to be fetched.

    Returns:
        HttpResponse: The rendered HTML page displaying the articles of the specified category,
                      along with all available categories and tags for the sidebar or navigation.
    """
    # Fetch articles that belong to the specified category
    articles = Article.objects.filter(category__iexact=category)  # Use case-insensitive filtering

    # Fetch all unique categories for sidebar or navigation
    all_categories = Article.objects.values_list('category', flat=True).distinct()

    # Fetch all tags for the sidebar or navigation
    all_tags = Tag.objects.all()

    # Prepare the context data
    context = {
        'articles': articles,
        'category': category,
        'all_categories': all_categories,
        'all_tags': all_tags,
    }

    # Render the category page with the context
    return render(request, 'category.html', context)

def tag(request, tag):
    """
    Display articles associated with a specific tag.

    Args:
        request (HttpRequest): The HTTP request object.
        tag (str): The tag name to filter articles.

    Returns:
        HttpResponse: The rendered HTML page displaying articles associated with the specified tag.
    """
    # Fetch articles that are associated with the specified tag
    articles = Article.objects.filter(tags__name=tag)
    
    # Fetch all categories and tags for the sidebar or navigation
    all_categories = Article.objects.values_list('category', flat=True).distinct()
    all_tags = Tag.objects.all()

    context = {
        'tag': tag,
        'articles': articles,
        'all_categories': all_categories,
        'all_tags': all_tags,
    }

    return render(request, 'tag.html', context)

def tags(request):
    context = {
        'tags': Tag.objects.all()
    }
    return render(request, 'tags.html', context)

def like(request, id):
    """
    Handle the liking of an article by a user.
    This view function increments the like count of an article if the user has not already liked it.
    It uses the session to track whether the user has liked the article before.
    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the article to be liked.
    Returns:
        HttpResponse: A redirect to the article detail page.
    Side Effects:
        - Increments the like count of the article.
        - Sets a session variable to track the like status.
        - Adds a success or error message to the messages framework.
    """
    article = get_object_or_404(Article, id=id)
    session_key = f'liked_article_{article.id}'
    
    if not request.session.get(session_key, False):
        article.likes += 1
        article.save()
        request.session[session_key] = True
        messages.success(request, 'You liked this article.')
    else:
        messages.error(request, 'You have already liked this article.')
    
    return redirect('article_detail', slug=article.slug)

def dislike(request, id):
    """
    Handles the dislike action for an article.
    This view function decreases the like count of an article by 1 if the user
    has not already disliked it. It uses the session to track whether the user
    has disliked the article before.
    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the article to be disliked.
    Returns:
        HttpResponse: A redirect response to the article detail page.
    Side Effects:
        - Decreases the like count of the article by 1 if not already disliked.
        - Sets a session key to track the dislike action.
        - Adds a success or error message to the messages framework.
    """
    article = get_object_or_404(Article, id=id)
    session_key = f'disliked_article_{article.id}'
    
    if not request.session.get(session_key, False):
        article.likes -= 1
        article.save()
        request.session[session_key] = True
        messages.success(request, 'You disliked this article.')
    else:
        messages.error(request, 'You have already disliked this article.')
    
    return redirect('article_detail', slug=article.slug)

def article_detail(request, post_id):
    article = get_object_or_404(Article, post_id=post_id)
    comments = article.comments.all()
    return render(request, 'article_detail.html', {'article': article, 'comments': comments})

# @login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def add_comment(request, post_id):
    """
    Handle the addition of a comment to a post.
    This view function processes a POST request to add a comment to a specific post.
    It retrieves the post and its associated article using the provided post_id.
    If the request method is POST and the form is valid, it saves the comment,
    associates it with the article and the current user, and redirects to the article detail page
    with a success message. If the form is invalid, it redirects with an error message.
    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the post to which the comment is being added.
    Returns:
        HttpResponse: A redirect to the article detail page.
    """

    post = get_object_or_404(Post, id=post_id)
    article = get_object_or_404(Article, slug=post.slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('article_detail', slug=article.slug)
        else:
            messages.error(request, 'There was an error adding your comment.')
    return redirect('article_detail', slug=article.slug)


def add_reply(request, comment_id):
    """
    Add a reply to a specific comment.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        comment_id (int): The ID of the comment to which the reply is being added.

    Returns:
        HttpResponse: A redirect to the article detail page.

    Behavior:
        - If the request method is POST, it attempts to retrieve the 'content' from the POST data.
        - If 'content' is present, it creates a new Reply object associated with the comment and the current user.
        - If 'content' is empty, it adds an error message indicating that the reply content cannot be empty.
        - In both cases, it redirects to the article detail page.
        - If the request method is not POST, it simply redirects to the article detail page.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Reply.objects.create(comment=comment, user=request.user, content=content)
            messages.success(request, 'Reply added successfully.')
        else:
            messages.error(request, 'Reply content cannot be empty.')
        return redirect('article_detail', slug=comment.article.slug)
    return redirect('article_detail', slug=comment.article.slug)

@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def delete_reply(request, id):
    """
    Delete a specific reply.
    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the reply to be deleted.
    Returns:
        HttpResponseRedirect: Redirects to the article detail page.
    Raises:
        Http404: If the reply with the given ID does not exist.
    Messages:
        Success: If the reply is deleted successfully.
        Error: If the user does not have permission to delete the reply.
    """
    """Delete a specific reply."""
    reply = get_object_or_404(Reply, id=id)
    if request.user == reply.user:
        reply.delete()
        messages.success(request, 'Reply deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this reply.')
    
    return redirect('article_detail', slug=reply.comment.article.slug)

@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def edit_reply(request, id):
    """
    Edit a specific reply.
    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the reply to be edited.
    Returns:
        HttpResponse: The HTTP response object.
    The function retrieves the reply object based on the provided ID. If the request method is POST and the user is the owner of the reply, it updates the reply content and saves it. If the update is successful, it redirects to the article detail page and displays a success message. If the user does not have permission to edit the reply, it displays an error message. If the request method is not POST, it renders the edit reply page with the reply object.
    """
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

@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def delete_comment(request, comment_id):
    """
    Deletes a comment if the requesting user is the owner of the comment.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        comment_id (int): The ID of the comment to be deleted.
    Returns:
        HttpResponseRedirect: Redirects to the article detail page.
    Raises:
        Http404: If the comment with the given ID does not exist.
    Side Effects:
        - Deletes the comment from the database if the user is authorized.
        - Adds a success message if the comment is deleted.
        - Adds an error message if the user is not authorized to delete the comment.
    """
    
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    return redirect('article_detail', slug=comment.article.slug)

@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def edit_comment(request, comment_id):
    """
    Edit a specific comment.

    This view handles the editing of a comment identified by its ID. It ensures that only the user who 
    created the comment can edit it. If the request method is POST and the user is the owner of the 
    comment, the comment's content is updated and saved. Appropriate success or error messages are 
    displayed based on the outcome.

    Args:
        request (HttpRequest): The HTTP request object.
        comment_id (int): The ID of the comment to be edited.

    Returns:
        HttpResponse: Renders the edit comment page with the comment object if the request method is 
        not POST or the user is not the owner. Redirects to the article detail page if the comment is 
        successfully updated.
    """
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


@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def edit_profile(request):
    """
    Edit user profile.
    This view handles the editing of a user's profile. If the request method is POST,
    it updates the user's email, first name, and last name with the data provided in
    the request. Upon successful update, it displays a success message and redirects
    the user to the profile page. If the request method is not POST, it renders the
    edit profile page.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
    Returns:
        HttpResponse: A redirect to the profile page if the profile is updated successfully,
                      otherwise renders the edit profile page.
    """
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, "edit_profile.html")

@login_required(login_url='login_view')  # Redirects to 'login_view' if not authenticated
def change_password(request):
    """
    Change user password with verification.

    This view handles the password change process for a logged-in user. It verifies the current password,
    checks if the new password and confirmation password match, and then updates the user's password.

    Args:
        request (HttpRequest): The HTTP request object containing POST data with 'current_password',
                               'new_password', and 'confirm_password'.

    Returns:
        HttpResponse: Redirects to 'change_password' with an error message if the current password is incorrect
                      or if the new passwords do not match. Redirects to 'profile' with a success message if the
                      password is changed successfully. Renders the 'change_password.html' template for GET requests.
    """
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
    """
    Generate and send a One-Time Password (OTP) to the user's email.

    This function generates a 6-digit OTP, assigns it to the user's profile,
    records the current timestamp, saves the profile, and sends an email
    containing the OTP to the user's registered email address.

    Args:
        user (User): The user object to whom the OTP will be sent. The user
                     object is expected to have a related profile with 'otp'
                     and 'otp_timestamp' fields, and an 'email' attribute.

    Raises:
        smtplib.SMTPException: If there is an error sending the email.
    """
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
    """
    Handle forgotten password by sending a reset link or OTP.
    This view handles POST requests to initiate the password reset process. 
    It performs the following steps:
    1. Retrieves the email from the POST request.
    2. Fetches the user associated with the provided email.
    3. Implements rate limiting to prevent abuse of OTP requests.
    4. Generates and sends an OTP to the user's email.
    5. Increments the OTP request count and sets a timeout for rate limiting.
    6. Displays success or error messages based on the process outcome.
    7. Redirects the user to the appropriate page.
    Args:
        request (HttpRequest): The HTTP request object containing method and POST data.
    Returns:
        HttpResponse: Renders the forget_password.html template for GET requests.
        HttpResponseRedirect: Redirects to the 'verify_otp' page for successful OTP generation.
        HttpResponseRedirect: Redirects to the 'forget_password' page if rate limit is exceeded.
    """
    
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
    return render(request, "privacy_policy.html")

def terms_and_conditions(request):
    return render(request, "terms_and_conditions.html")

def cookie_policy(request):
    return render(request, "cookie_policy.html")

def sitemap(request):
    return render(request, "sitemap.html")

def robots(request):
    return render(request, "robots.html")

def ads(request):
    return render(request, "ads.html")

def advertise_with_us(request):
    return render(request, "advertise_with_us.html")

def feedback(request):
    return render(request, "feedback.html")

def report(request):
    return render(request, "report.html")

def subscribe(request):
    return render(request, "subscribe.html")

def unsubscribe(request):
    return render(request, "unsubscribe.html")

def newsletter(request):
    return render(request, "newsletter.html")

def newsletter_unsubscribe(request):
    return render(request, "newsletter_unsubscribe.html")

def help_center(request):
    return render(request, "help_center.html")

def faq(request):
    return render(request, "faq.html")

def current_year(request):
    def current_year(request):
        """
        Display the current year in the footer.

        Usage:
        <!-- Copyright - Component -->
        <div class="py-3 py-md-4 py-xl-5 border-top">
          <div class="container">
            <div class="row">
              <div class="col-12">
                <div class="copyright-wrapper mb-1 fs-7 text-md-center">
                  &copy; {{current_year}}. All Rights Reserved.
                </div>
                <div class="credit-wrapper text-secondary fs-8 text-md-center">
                  
                </div>
              </div>
            </div>
          </div>
        </div>
        """

        current_year = datetime.now().year
        return render(request, 'footer.html', {'current_year': current_year})
