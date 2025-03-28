import cloudinary.models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    followed_fandoms = models.JSONField(default=list, null=True, blank=True)
    is_creator = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    profile_image = cloudinary.models.CloudinaryField(
        "image",
        folder="user_profile_image/",
        blank=True,
        null=True
    )

    groups = models.ManyToManyField(Group, related_name="fanlore_user_groups",
                                    blank=True)
    user_permissions = models.ManyToManyField(Permission,
                                              related_name="fanlore_user_permissions",
                                              blank=True)
