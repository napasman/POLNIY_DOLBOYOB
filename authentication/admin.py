"""
admin management
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, NotificationForm
from .models import User, Notification, Order, Product, OrderHistory, TelegramProfile


class CustomUserAdmin(UserAdmin):
    """
    custom user admin
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'name', 'is_superuser', 'subscribed')
    list_filter = ('email', 'is_staff', 'is_active',  'subscribed')
    fieldsets = (
        (None, {'fields': ('profile_picture', 'name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',  'subscribed')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', "name", 'password1', 'password2', 'is_staff', 'is_active',  'subscribed')}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('name', 'email')


admin.site.register(User, CustomUserAdmin)


@admin.register(Notification)
class PostAdmin(ImportExportModelAdmin):
    form = NotificationForm


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'username', 'first_name', 'auth_date')
    search_fields = ('username', 'first_name', 'telegram_id')
    readonly_fields = ('auth_date',)


admin.site.register(Order)
admin.site.register(OrderHistory)
admin.site.register(Product)
