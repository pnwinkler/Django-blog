from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os


# when a user is saved, send the post_save signal.
# the receiver is this function below.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # if user was created, create a Profile for that same user
    if created:
        Profile.objects.create(user=instance)


# signals allow applications to get notified when actions occur elsewhere
# in the framework
# signals allow certain senders to notify receivers that some action has taken place
# post_save means after an object is saved into the database with Model.save(...)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_image(sender, instance, **kwargs):
    os.remove(instance.profile.image.path)
