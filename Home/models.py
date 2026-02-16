from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
import uuid


# Create your models here.

class AIModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name




class Prompt(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompts", null=True)
    prompt = models.TextField()
    image = models.ImageField(upload_to='prompts/')
    models_supported = models.ManyToManyField(AIModel, blank=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If no image, do nothing
        if not self.image:
            return

        img_path = self.image.path

        # Prevent re-processing already converted images
        if img_path.endswith(".webp"):
            return

        img = Image.open(img_path)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail((1024, 1024), Image.LANCZOS)

        new_name = f"{uuid.uuid4().hex}.webp"
        new_path = os.path.join(os.path.dirname(img_path), new_name)

        img.save(new_path, "WEBP", quality=70, method=6)

        os.remove(img_path)

        self.image.name = f"prompts/{new_name}"
        super().save(update_fields=["image"])
    

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
    
    