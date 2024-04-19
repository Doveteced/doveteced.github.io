from django.shortcuts import render
from .models import Blog, Reply
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Reply
from django.contrib.auth.decorators import login_required, user_passes_test

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    replies = Reply.objects.filter(blog=blog)
    return render(request, 'blog_detail.html', {'blog': blog, 'replies': replies})


def create_reply(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        reply_text = request.POST.get('reply_text')
        reply = Reply.objects.create(blog=blog, text=reply_text)
        return redirect('blog_detail', blog_id=blog_id)
    else:
        return redirect('blog_detail', blog_id=blog_id)

def reply_detail(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    return render(request, 'reply_detail.html', {'reply': reply})


def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    blog_id = reply.blog.id
    reply.delete()
    return redirect('blog_detail', blog_id=blog_id)


def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.method == 'POST':
        reply.text = request.POST.get('reply_text')
        reply.save()
        return redirect('reply_detail', reply_id=reply_id)
    else:
        return render(request, 'edit_reply.html', {'reply': reply})

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        blog = Blog.objects.create(title=title, text=text)
        return redirect('blog_detail', blog_id=blog.id)
    else:
        return render(request, 'create_blog.html')

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.text = request.POST.get('text')
        blog.save()
        return redirect('blog_detail', blog_id=blog_id)
    else:
        return render(request, 'edit_blog.html', {'blog': blog})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def post_new(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    else:
        # Render the form
        pass

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # Handle form submission
        pass
    else:
        # Render the form
        pass

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Delete the post
    pass

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # Handle form submission
        pass
    else:
        # Render the form
        pass

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # Approve the comment
    pass

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # Remove the comment
    pass