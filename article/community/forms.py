from django import forms
from .models import Post, Comment, Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'content']  # Assuming you want to select a topic when creating a post
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here...'}),
        }
        labels = {
            'topic': 'Select Topic',
            'content': 'Post Content',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }
        labels = {
            'content': 'Comment',
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Reply to this comment...'}),
        }
        labels = {
            'content': 'Reply',
        }
