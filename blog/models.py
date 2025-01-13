from django.db import models

# create blog model
class Blog(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (str): The title of the blog post.
        text (str): The content of the blog post.
        author (str): The author of the blog post.
        created_at (datetime): The date and time when the blog post was created.
        updated_at (datetime): The date and time when the blog post was last updated.
        user (User): The user who created the blog post.
        images (ManyToManyField): The images associated with the blog post.
        category (ForeignKey): The category associated with the blog post.
    """
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    images = models.ManyToManyField('Image')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

# Blog Categories with image
class Category(models.Model):
    """
    Represents a category for blog posts.

    Attributes:
        name (str): The name of the category.
        description (str): The description of the category.
        image (ImageField): The image associated with the category.
        created_at (datetime): The date and time when the category was created.
        updated_at (datetime): The date and time when the category was last updated.
        user (User): The user who created the category.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
# create reply model
class Reply(models.Model):
    """
    Represents a reply to a blog post.

    Attributes:
        text (str): The content of the reply.
        created_at (datetime): The date and time when the reply was created.
        updated_at (datetime): The date and time when the reply was last updated.
        user (User): The user who created the reply.
    """
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

# create image model
class Image(models.Model):
    """
    Represents an image associated with a blog post.

    Attributes:
        image (ImageField): The image file.
        created_at (datetime): The date and time when the image was created.
        updated_at (datetime): The date and time when the image was last updated.
        user (User): The user who uploaded the image.
    """
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
