from django.db import models
from django_quill.fields import QuillField

class Post(models.Model):
    content = models.TextField()