from django.contrib import admin
from .models import AIModel, Tag, Prompt
# Register your models here.

admin.site.register(Tag)
admin.site.register(Prompt)
admin.site.register(AIModel)