import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from home.models import Article, Tag, Profile, Comment as HomeComment, Reply as HomeReply, Dislike as HomeDislike, Like as HomeLike # Updated community Profile model
class Profile(Profile):
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Updated community Post model inheriting from Article
class Post(Article):
    topic = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to generate a unique slug if not present."""
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def hashed_id(self):
        """Generate a hashed_id for the post if ID exists."""
        return hashlib.md5(str(self.id).encode()).hexdigest() if self.id else None

    def generate_unique_slug(self):
        """Generate a unique slug for the post."""
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug
# Updated community Comment model inheriting from home Comment model
class Comment(HomeComment):
    comment_ptr = models.OneToOneField(HomeComment, on_delete=models.CASCADE, parent_link=True, default=None)
    pass

# Updated community Reply model inheriting from home Reply model
class Reply(HomeReply):
    pass
    
# Updated community Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# Updated community Topic model inheriting from home Tag model
class Topic(Tag):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='topics')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
# Updated community Like model to inherit from home Like model
class Like(HomeLike):
    class Meta:
        proxy = True  # Use proxy if you don't need to add any new fields

# Updated community Dislike model to inherit from home Dislike model
class Dislike(HomeDislike):
    class Meta:
        proxy = True  # Use proxy if you don't need to add any new fields
