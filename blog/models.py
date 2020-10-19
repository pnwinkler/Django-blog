from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


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

    # need this so we have a URL to send users to after they post an entry
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
