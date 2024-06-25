from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from api.models import user, event, filters

# Register your models here.

@admin.register(user.User)
class UserAdminConfig(UserAdmin):

    """User config for Admin Dashboard."""

    ordering = ['id']
    list_filter = ['id']
    list_display = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        })
    )


@admin.register(event.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','host', 'title', 'category', 'language', 'location', 'date_time', 'number_of_seats', 'ticket_price', 'currency', 'thumbnail', 'description' )
    prepopulated_fields = {'slug_title': ('title',),}
    
@admin.register(filters.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug_title': ('title',),}


@admin.register(filters.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    prepopulated_fields = {'slug_title': ('title',),}