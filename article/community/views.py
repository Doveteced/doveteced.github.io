from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Post, Comment, Reply, Like, Dislike
from .forms import PostForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required

# List all topics
def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'forum/topic_list.html', {'topics': topics})

# View a specific topic and its posts
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all()
    return render(request, 'forum/topic_detail.html', {'topic': topic, 'posts': posts})

# View a specific post and its comments
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

# Reply to a comment
def reply_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
            return redirect('post_detail', post_id=post.id)
    else:
        reply_form = ReplyForm()

    return render(request, 'forum/reply_detail.html', {
        'comment': comment,
        'reply_form': reply_form,
    })

# Like a post
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect('post_detail', post_id=post.id)

# Dislike a post
@login_required
def toggle_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    dislike, created = Dislike.objects.get_or_create(post=post, user=request.user)
    if not created:
        dislike.delete()  # Remove dislike if already disliked
    return redirect('post_detail', post_id=post.id)
