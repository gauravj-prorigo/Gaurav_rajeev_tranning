from django.contrib import admin
from .models import *
# Register your models here.
class blogcustom(admin.ModelAdmin):
    list_display = ('title','content','created_at',)
   


admin.site.register(Blog,blogcustom),