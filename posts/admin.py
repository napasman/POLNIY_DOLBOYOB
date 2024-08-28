from django.contrib import admin
from . models import Contact, Post, BlogComment, EmailSubscriptions,  ApiUser, Download, Group, Channel, Member, Admin, ReferralLink, AdLink, LevelThreshold, Tag
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.forms import widgets
from django.utils.html import format_html
from django.db import models
from django.template.loader import render_to_string
from .forms import PostForm
from django.conf import settings  # Import the settings module


class PostResource(resources.ModelResource):
    model = Post
    fields = ["title", "description", "short_description"]


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    form = PostForm  # Use the custom form for the admin
    prepopulated_fields = {'slug': ('title',)}
    resource_class = PostResource


admin.site.register(Contact)
admin.site.register(BlogComment)
admin.site.register(EmailSubscriptions)


class ReferralLinkAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'user_email', 'clicks')

    list_filter = ('user_email',)  # Use 'user_email' for filtering

    def user_email(self, obj):
        return obj.user_email

    user_email.short_description = 'User Email'


admin.site.register(ReferralLink, ReferralLinkAdmin)
admin.site.register(AdLink)

admin.site.register(LevelThreshold)

admin.site.register(Tag)


class CustomSelectMultiple(widgets.SelectMultiple):
    template_name = 'admin/widgets/select_multiple_custom.html'

    def render(self, name, value, attrs=None, renderer=None):
        selected_download_ids = value
        selected_downloads = Download.objects.filter(id__in=selected_download_ids)
        selected_download_names = [download.file.name for download in selected_downloads]
        context = {
            'widget': self,
            'name': name,
            'value': value,
            'attrs': attrs,
            'selected_download_names': selected_download_names,
        }
        return render_to_string(self.template_name, context)


class DownloadInline(admin.TabularInline):
    model = ApiUser.downloads.through
    extra = 1


class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'ip_address', 'balance', 'status', 'created')
    search_fields = ('id', 'user__email', 'ip_address', 'balance', 'status')
    list_filter = ('status', 'created')
    exclude = ('downloads', )

    def email(self, obj):
        return obj.user.email if obj.user else obj.ip_address

    email.short_description = "User Email"

    inlines = [DownloadInline]


admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(Download)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('url', 'filter', 'additional_keyword', 'language')  # Fields to display in the admin list view
    list_filter = ('language',)  # Filter options to display in the admin sidebar
    search_fields = ['url', 'filter', 'additional_keyword']


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('url', 'filter', 'additional_keyword', 'language')  # Fields to display in the admin list view
    list_filter = ('language',)  # Filter options to display in the admin sidebar
    search_fields = ['url', 'filter', 'additional_keyword']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('url', 'filter', 'additional_keyword', 'language')  # Fields to display in the admin list view
    list_filter = ('language',)  # Filter options to display in the admin sidebar
    search_fields = ['url', 'filter', 'additional_keyword']


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('url', 'filter', 'additional_keyword', 'language')  # Fields to display in the admin list view
    list_filter = ('language',)  # Filter options to display in the admin sidebar
    search_fields = ['url', 'filter', 'additional_keyword']

# class PostAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('title',)}
#     class Media:
#         js= ('tinyInject.js',)
