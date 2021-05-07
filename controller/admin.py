from django.contrib import admin
from .models import requestCount, threshold

# Register your models here.
admin.site.register(requestCount)
admin.site.register(threshold)