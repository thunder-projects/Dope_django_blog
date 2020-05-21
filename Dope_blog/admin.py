from django.contrib import admin
from django.db import models
from django.contrib import messages
# Register your models here.
from .models import Post, Heading, Subheading, Usercontact, Comment, UserProfile, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('title',)

    def get_ordering(self,request):
        if request.user.is_superuser:
            return ('title','-timestamp')
        return ('title',)

    def active(self, obj):
        return obj.is_active == 1
    
    def make_active(modeladmin, request, queryset): 
        queryset.update(is_active = 1) 
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!") 
  
    def make_inactive(modeladmin, request, queryset): 
        queryset.update(is_active = 0) 
        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!") 
  
    admin.site.add_action(make_active, "Make Active") 
    admin.site.add_action(make_inactive, "Make Inactive")

    active.boolean = True

admin.site.register(Post,PostAdmin)
admin.site.register(Heading)
admin.site.register(Subheading)
admin.site.register(Usercontact)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Category)

