# signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from Home.models import Prompt
import os

@receiver(post_delete, sender=Prompt)
def delete_prompt_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
