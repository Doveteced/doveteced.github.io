from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import generate_slug
import hashlib
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_timestamp = models.DateTimeField(null=True, blank=True)
    hashed_id = models.CharField(max_length=64, unique=True, editable=False)

    def is_otp_expired(self):
        if self.otp_timestamp:
            return timezone.now() > self.otp_timestamp + timezone.timedelta(minutes=10)
        return True

    def is_token_expired(self):
        return timezone.now() > self.user.date_joined + timezone.timedelta(hours=1)

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(str(self.user.id).encode()).hexdigest()
        super().save(*args, **kwargs)

class Article(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    likes = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(str(self.id).encode()).hexdigest() if self.id else None
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hashed_id = models.CharField(max_length=64, unique=True, editable=False)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(f"{self.article.id}-{self.user.id}".encode()).hexdigest()
        super().save(*args, **kwargs)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hashed_id = models.CharField(max_length=64, unique=True, editable=False)

    def __str__(self):
        return f"Reply by {self.user.username} on comment {self.comment.id}"

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(f"{self.comment.id}-{self.user.id}".encode()).hexdigest()
        super().save(*args, **kwargs)

