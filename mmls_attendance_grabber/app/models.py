from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# Create your models here.

class UserData(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    course = models.JSONField(default=list) # mmlsattendance.Courses()

    class Meta:
        verbose_name = "user data"
        verbose_name_plural = "user data"
        permissions = [('can_view_all_attendance', 'Can view all attendance')]

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=get_user_model())
def courses_create(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        UserData.objects.create(user=instance,)

# @receiver(post_delete, sender=Profile)
# def post_delete_user(sender, instance, *args, **kwargs):
#     if instance.user: # just in case user is not specified
#         instance.user.delete()