from django.db import models

# Create your models here.

class AIModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Prompt(models.Model):
    title = models.CharField(max_length=255)
    prompt = models.TextField()
    image = models.ImageField(upload_to='prompts/')
    tags = models.ManyToManyField(Tag, related_name='prompts')
    models_supported = models.ManyToManyField(AIModel, blank=True)
    instructions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
