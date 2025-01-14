from django.db import models

from dovetecenterprises import settings

# Create user model    
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.username:
            if self.email:
                self.username = self.email.split('@')[0]
            else:
                self.username = (self.first_name + self.last_name).lower()
        super(User, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.username
    
