from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe, Comment

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'bio', 'avatar')}),
    )

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Recipe)
admin.site.register(Comment)
