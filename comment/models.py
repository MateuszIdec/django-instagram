from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from post.models import Post
from django.db.models.signals import post_save, post_delete
from notification.models import Notification


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

@receiver(post_save, sender=Comment)
def user_comment_post(sender, instance, created, **kwargs):
    if created:
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender_user = comment.user
        notify = Notification(
            post=post,
            sender=sender_user,
            user=post.user,
            text_preview=text_preview,
            notification_types=2
        )
        notify.save()

@receiver(post_delete, sender=Comment)
def user_del_comment_post(sender, instance, **kwargs):
    comment = instance
    post = comment.post
    sender_user = comment.user
    Notification.objects.filter(
        post=post,
        sender=sender_user,
        user=post.user,
        notification_types=2
    ).delete()
