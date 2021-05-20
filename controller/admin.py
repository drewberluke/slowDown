from django.contrib import admin
from .models import requestCount, threshold, requestReset, studentWaitTime

# Register your models here.
admin.site.register(requestCount)
admin.site.register(threshold)
admin.site.register(requestReset)
admin.site.register(studentWaitTime)