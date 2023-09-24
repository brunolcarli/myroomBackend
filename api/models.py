from django.db import models
from django.contrib.auth.models import User


class UserModel(User):
    avatar = models.BinaryField(null=True)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    birthdate = models.DateField(null=False)


class Room(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description = models.TextField(null=True)
    user = models.OneToOneField(UserModel, null=True, on_delete=models.CASCADE)
    room_picture = models.BinaryField(null=True)
    background_picture = models.BinaryField(null=True)
    default_background_active = models.BooleanField(default=True)
    photos_section_active = models.BooleanField(default=True)
    articles_section_active = models.BooleanField(default=True)
    threads_section_active = models.BooleanField(default=True)


class Article(models.Model):
    room = models.ForeignKey(Room, null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    post_datetime = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
    room = models.ForeignKey(Room, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, null=False, on_delete=models.CASCADE)
    data = models.BinaryField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True)
    post_datetime = models.DateTimeField(auto_now_add=True)


class ThreadModel(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserModel, null=False, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=False, on_delete=models.CASCADE)
    last_comment_datetime = models.DateTimeField(null=True)
    public = models.BooleanField(default=True)
    num_comments = models.IntegerField(default=0)


class ThreadComment(models.Model):
    author = models.ForeignKey(UserModel, null=False, on_delete=models.CASCADE)
    thread = models.ForeignKey(ThreadModel, null=False, on_delete=models.CASCADE)
    post_datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False, blank=False)
