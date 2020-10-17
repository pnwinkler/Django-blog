from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# each class will be its own table in db
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # we don't use auto_add options because they don't allow manual updating
    date_posted = models.DateTimeField(default=timezone.now)
    # one-to-many relationship. And, if a user is deleted, delete post too
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title