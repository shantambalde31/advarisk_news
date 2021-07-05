from django.contrib import admin
from .models import User, SearchedKeywords

# Register your models here.

admin.site.register(User)
admin.site.register(SearchedKeywords)
