from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from community.forms import CommentForm, ReplyForm
from community.models import Category, Comment, Post, Reply, Topic, Like, Dislike
from home.models import Article


# View to list all topics
def topic_list(request):
    topics = Category.objects.all()
    return render(request, 'forum/topic_list.html', {'topics': topics})


# View to display a specific topic and its related posts
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all()
    return render(request, 'forum/topic_detail.html', {'topic': topic, 'posts': posts})

# View to display a specific post and its comments
def post_detail(request, post_slug):
    """View function to display a specific post and its comments."""
    post = get_object_or_404(Article, slug=post_slug)  # Use slug field to get the post
    comments = post.comments.all()  # Retrieve all comments for the post
    comment_form = CommentForm(request.POST or None)  # Instantiate form with POST data if available

    if request.method == "POST" and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post_detail', post_slug=post.slug)  # Avoid form resubmission by redirecting

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

# View to add a comment to a post
def add_comment(request, post_id):
    '''Add a comment to a post.

    This view handles the creation of a new comment for a post. It expects a POST request with the comment content. If the content is not empty, a new comment is created and associated with the post.

    Args:
        request (HttpRequest): The request object
        post_id (int): The ID of the post to add the comment to

    Returns:
        HttpResponseRedirect: Redirects to the post detail page after adding the comment
    '''
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('post_detail', post_slug=post.slug)

def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    article = parent_comment.article  # Get the associated article
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.article = article
            reply.user = request.user
            reply.parent = parent_comment  # Set the parent comment
            reply.save()
            messages.success(request, 'Reply added successfully.')
            return redirect('article_detail', slug=article.slug)  # Use article.slug for redirection
        else:
            messages.error(request, 'There was an error adding your reply.')
    
    # If the request is AJAX, return a JSON response
    if request.is_ajax():
        return JsonResponse({'success': True, 'message': 'Reply added successfully.'})
    
    # For non-AJAX requests, redirect as usual
    return redirect('article_detail', slug=article.slug)

def reply_detail(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    return render(request, {'reply': reply})

# Toggle like on a post for authenticated users
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()  # Remove like if it already exists
    
    return redirect('post_detail', post_id=post.id)


# Toggle dislike on a post for authenticated users
@login_required
def toggle_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    dislike, created = Dislike.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        dislike.delete()  # Remove dislike if it already exists
    
    return redirect('post_detail', post_id=post.id)
