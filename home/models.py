from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from froala_editor.fields import FroalaField
from django.utils import timezone
from django.utils.text import slugify
import hashlib

from dovetecenterprises import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=30, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        if self.username:
            return self.username
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

class Profile(models.Model):
    """
    Profile model extends the built-in User model with additional fields.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_timestamp = models.DateTimeField(null=True, blank=True)
    hashed_id = models.CharField(max_length=64, unique=True, editable=False)
    image = models.ImageField(upload_to='profile', blank=True, null=True)

    def is_otp_expired(self):
        """Check if the OTP is expired (10 minutes)."""
        if self.otp_timestamp:
            return timezone.now() > self.otp_timestamp + timezone.timedelta(minutes=10)
        return True

    def is_token_expired(self):
        """Check if the token is expired (1 hour from user registration)."""
        return timezone.now() > self.user.date_joined + timezone.timedelta(hours=1)

    def save(self, *args, **kwargs):
        """Override save method to generate hashed_id if not present."""
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(str(self.user.id).encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

class Tag(models.Model):
    """
    Tag model for categorizing articles.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    """
    Article model with fields for SEO and content editing using Froala.
    
    Args:
        id (AutoField): Unique identifier for the article.
        title (CharField): Title of the article.
        content (FroalaField): Content of the article.
        seo_description (TextField): Description for SEO purposes.
        slug (SlugField): Unique slug for the article.
        user (ForeignKey): Reference to the User who created the article.
        image (ImageField): Featured image for the article.
        created_at (DateTimeField): Timestamp when the article was created.
        updated_at (DateTimeField): Timestamp when the article was last updated.
        category (CharField): Category of the article.
        tags (ManyToManyField): Tags associated with the article.
        likes (PositiveIntegerField): Number of likes for the article.
        dislikes (PositiveIntegerField): Number of dislikes for the article.
        views (PositiveIntegerField): Number of views for the article.
        author (ForeignKey): Reference to the Profile who created the article.
        featured (BooleanField): Indicates if the article is featured.
        
    Methods:
        __str__(): Returns a string representation of the article.
        save(*args, **kwargs): Overrides the save method to generate a unique slug if not present.
        hashed_id(): Generates a hashed_id for the article if ID exists.
        generate_unique_slug(): Generates a unique slug for the
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, unique=True)
    content = FroalaField()
    seo_description = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=1000, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE, related_name='articles')
    featured = models.BooleanField(default=False)

    class Meta:
        abstract = False

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to generate a unique slug if not present."""
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def hashed_id(self):
        """Generate a hashed_id for the article if ID exists."""
        return hashlib.md5(str(self.id).encode()).hexdigest() if self.id else None

    def generate_unique_slug(self):
        """Generate a unique slug for the article."""
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

class Comment(models.Model):
    """
    Comment model represents a user's comment on an article.

    Attributes:
        article (ForeignKey): Reference to the related Article object.
        user (ForeignKey): Reference to the User who made the comment.
        content (TextField): The content of the comment.
        created_at (DateTimeField): Timestamp when the comment was created.
        hashed_id (CharField): Unique hashed identifier for the comment.
        is_deleted (BooleanField): Indicates if the comment is soft deleted.

    Methods:
        __str__(): Returns a string representation of the comment.
        save(*args, **kwargs): Overrides the save method to generate a hashed_id if it doesn't exist.
        delete(*args, **kwargs): Overrides the delete method to perform a soft delete by setting is_deleted to True.
    """
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hashed_id = models.CharField(max_length=64, unique=True, editable=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete field

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(f"{self.article.id}-{self.user.id}".encode()).hexdigest()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class Reply(models.Model):
    """
    Reply model linked to a Comment.
    """
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hashed_id = models.CharField(max_length=64, unique=True, editable=False)

    def __str__(self):
        return f"Reply by {self.user.username} on comment {self.comment.id}"

    def save(self, *args, **kwargs):
        """Override save method to generate hashed_id if not present."""
        if not self.hashed_id:
            self.hashed_id = hashlib.md5(f"{self.comment.id}-{self.user.id}".encode()).hexdigest()
        super().save(*args, **kwargs)

class Like(models.Model):
    """
    Like model for users to like articles.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"
    
class Dislike(models.Model):
    """
    Dislike model for users to dislike articles.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    dislike_ptr = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} disliked {self.article.title}"
