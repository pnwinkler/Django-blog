# room to expand: delete images once a user changes their profile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class Profile(models.Model):
    # one profile for one user. If user is deleted, delete profile.
    # but deleting profile won't delete user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    # overwrite save method so we can compress image, and delete unused images
    def save(self, *args, **kwargs):
        # compare before and after profile images, to delete replaced images
        prior_profile_images = set()
        for profile in Profile.objects.all():
            prior_profile_images.add(profile.image.path)

        # save and compress
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        # delete now unused image
        profile_images_after_save = set()
        for profile in Profile.objects.all():
            profile_images_after_save.add(profile.image.path)
        if len(prior_profile_images - profile_images_after_save) > 0:
            for f in prior_profile_images - profile_images_after_save:
                os.remove(str(f))
