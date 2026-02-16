from django.contrib import admin
from .models import AIModel, Prompt, Contact
# Register your models here.

admin.site.register(Prompt)
admin.site.register(AIModel)
admin.site.register(Contact)