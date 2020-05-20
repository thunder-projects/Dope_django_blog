from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField


COLOUR_CHOICES = (
    ("primary", "blue"),
    ("secondary", "grey"),
    ("success", "green"),
    ("danger", "red"),
    ("warning", "yellow"),
    ("info", "Sky blue"),
    ("light", "white"),
    ("dark", "black"),
)


class Category(models.Model):
    category = models.CharField(max_length=254)
    colour = models.CharField(max_length=254, choices=COLOUR_CHOICES)
    image = models.ImageField(
        upload_to='blog/images', default='blog/images/defaultforcat.png', null=True, blank=True)
    decs = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.category


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', null=True)
    avatar = models.ImageField(
        upload_to='blog/images', default='blog/images/iconfinder_user-01_186382.png', null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # def __str__(self):
    #     return self.user


class Subheading(models.Model):
    subheading = models.CharField(max_length=255)
    subtext = RichTextUploadingField(max_length=5000, null=True)
    subhead_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subheadings', null=True)

    def __str__(self):
        return self.subheading


class Heading(models.Model):
    heading = models.CharField(max_length=255)
    text = RichTextUploadingField(max_length=5000, null=True)
    head_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='headings', null=True)
    subheading = models.OneToOneField(
        Subheading, on_delete=models.CASCADE, related_name='headings', blank=True, null=True)

    def __str__(self):
        return self.heading


class Post(models.Model):
    topic = models.CharField(max_length=25, null=True)
    description = RichTextField(max_length=1000, blank=True, null=True)
    title = models.TextField(max_length=500)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', null=True)
    heading = models.ManyToManyField(
        Heading, related_name='posts', blank=True)
    subheading = models.ManyToManyField(
        Subheading, related_name='posts', blank=True)
    text = RichTextUploadingField(max_length=5000, null=True)
    thumbnail = models.ImageField('blog/images', null=True, blank=True)
    cover = models.ImageField('blog/images', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def totalLikes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post', args=[int(self.id)])


class Usercontact(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    query = models.TextField(max_length=500)

    def __str__(self):
        return self.email


class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', null=True)
    reply = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    like = models.ManyToManyField(User, blank=True)
    dislike = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # class Meta:
    #     ordering = ['-timestamp']

    def __str__(self):
        return self.comment


    # @property
    # def is_reply(self):
    # # """Return `True` if instance is a parent."""
    #     if self.reply is not None:
    #         return False
    #     return True
    # def children(self):
    # # Return replies of a comment
    #     return Comment.objects.filter(reply=self)


# print(Post.objects.filter(pk=1))
