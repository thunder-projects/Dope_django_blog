from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Post, Heading, Subheading, Usercontact, Comment, UserProfile, Category


admin.site.register(Post)
admin.site.register(Heading)
admin.site.register(Subheading)
admin.site.register(Usercontact)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Category)

