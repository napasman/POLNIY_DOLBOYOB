"""
authentication urls
"""

from unicodedata import name
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from posts import views as post_views
from charts import views as chart_views




urlpatterns = [
    path('register/', views.register, name="register"),
    path('login_redirect/', views.login_redirect, name="login_redirect"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout, name="logout"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("dashboard/files/<str:category>/", views.view_files, name="view_files"),
    path("dashboard/filemanager/", views.file_manager, name="file_manager"),
    path("dashboard/customers", views.users, name="customers"),
    path("dashboard/download-file/<int:file_id>/", post_views.download_file, name="download_file"),
    path("dashboard/download-excel/<int:file_id>/", post_views.download_excel, name="download_excel"),
    path("dashboard/charts/", chart_views.charts, name="charts"),
    path('dashboard/view_all_notifications/', views.view_all_notifications, name='view_all_notifications'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('send_email_async/', views.send_email_async, name='send_email_async'),
    path('bulk_pages/', views.bulk_pages, name='bulk_pages'),
    path('order_details/', views.order_details, name='order_details'),
    path('update_order/', views.update_order, name='update_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('save_new_order/', views.save_new_order, name='save_new_order'),
    path('create_order_history_entry/', views.create_order_history_entry, name='create_order_history_entry'),
    path('mylistings/', views.marketplaceListings, name='marketplaceListings'),
]

