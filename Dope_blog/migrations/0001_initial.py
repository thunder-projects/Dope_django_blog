# Generated by Django 3.0.5 on 2020-05-20 15:21

import ckeditor.fields
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=254)),
                ('colour', models.CharField(choices=[('primary', 'blue'), ('secondary', 'grey'), ('success', 'green'), ('danger', 'red'), ('warning', 'yellow'), ('info', 'Sky blue'), ('light', 'white'), ('dark', 'black')], max_length=254)),
                ('image', models.ImageField(blank=True, default='blog/images/defaultforcat.png', null=True, upload_to='blog/images')),
                ('decs', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255)),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(max_length=5000, null=True)),
                ('head_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usercontact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('query', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='blog/images/iconfinder_user-01_186382.png', null=True, upload_to='blog/images')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subheading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subheading', models.CharField(max_length=255)),
                ('subtext', ckeditor_uploader.fields.RichTextUploadingField(max_length=5000, null=True)),
                ('subhead_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subheadings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=25, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True)),
                ('title', models.TextField(max_length=500)),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(max_length=5000, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='', verbose_name='blog/images')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='', verbose_name='blog/images')),
                ('views', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('heading', models.ManyToManyField(blank=True, related_name='posts', to='Dope_blog.Heading')),
                ('likes', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('subheading', models.ManyToManyField(blank=True, related_name='posts', to='Dope_blog.Subheading')),
            ],
        ),
        migrations.AddField(
            model_name='heading',
            name='subheading',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headings', to='Dope_blog.Subheading'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('dislike', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Dope_blog.Post')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Dope_blog.Comment')),
            ],
        ),
    ]
