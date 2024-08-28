"""skote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from .views import MyPasswordSetView, MyPasswordChangeView, MyPasswordResetView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    # Dashboards View
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("dashboard_saas", views.SaasView.as_view(), name="dashboard_saas"),
    path("dashboard_crypto", views.CryptoView.as_view(), name="dashboard_crypto"),
    path("dashboard_blog", views.BlogView.as_view(), name="dashboard_blog"),
    # Calender View
    path("calendar", views.CalendarView.as_view(), name="calendar"),
    path("full-calendar", views.CalendarFullView.as_view(), name="full-calendar"),
    # Chat View
    path("chat", views.ChatView.as_view(), name="chat"),
    # Layouts
    path("layout/", include("skote_admin.layout.urls")),
    # File manager View
    path("filemanager", views.FileManagerView.as_view(), name="filemanager"),
    # Ecommerce
    path("ecommerce/", include("skote_admin.ecommerce.urls")),
    # Crypto
    path("crypto/", include("skote_admin.crypto.urls")),
    # Email
    path("email/", include("skote_admin.e_mail.urls")),
    # Invoices
    path("invoices/", include("skote_admin.invoices.urls")),
    # Projects
    path("projects/", include("skote_admin.projects.urls")),
    # Tasks
    path("tasks/", include("skote_admin.tasks.urls")),
    # Blog
    path("blog/", include("skote_admin.blog.urls")),
    # Blog
    path("contacts/", include("skote_admin.contacts.urls")),
    # Authencation
    # path('authentication/',include('authentication.urls')),
    # Pages
    path("pages/", include("skote_admin.pages.urls")),
    # Components
    path("components/", include("skote_admin.components.urls")),
    # Allauth
    path("account/", include("allauth.urls")),
    path(
        "auth-logout/",
        TemplateView.as_view(template_name="account/logout-success.html"),
        name="pages-logout",
    ),
    path(
        "auth-lockscreen/",
        TemplateView.as_view(template_name="account/lock-screen.html"),
        name="pages-lockscreen",
    ),
    # Custum change password done page redirect
    path(
        "accounts/password/change/",
        login_required(MyPasswordChangeView.as_view()),
        name="account_change_password",
    ),
    # Custum set password done page redirect
    path(
        "accounts/password/set/",
        login_required(MyPasswordSetView.as_view()),
        name="account_set_password",
    ),
    path(
        "accounts/password/reset/",
        MyPasswordResetView.as_view(),
        name="account_reset_password",
    ),

]
