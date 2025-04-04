# fanlore/models/content_like.py (or in models.py)
from django.db import models
from django.conf import settings
from .content import Content


class ContentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} liked {self.content.title}"
