from django.contrib import admin

# Register your models here.
from .models import UserData

class UserDataAdmin(admin.ModelAdmin):
    exclude = ("user",)
    readonly_fields = ("user",)
    fields = ("user", "course",)


admin.site.register(UserData, UserDataAdmin)