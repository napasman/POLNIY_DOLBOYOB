# app_name/urls.py

from django.urls import path,  reverse_lazy
from . import views
import datetime

from django.utils import timezone


from authentication.views import marketplace as auth_marketplace
from django.contrib.auth import views as auth_views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('login/', views.signin, name="signin"),
    path('handle-telegram-auth/', views.handle_telegram_auth, name='handle_telegram_auth'),
    path('signup/', views.signup, name="signup"),
    path('blog/postcomment', views.postcomment, name="postcomment"),
    path('blog/', views.blog, name="blog"),
    path('blogs/<str:slug>', views.blog_post, name="blogpost"),
    path('contact/', views.contact, name="contact"),
    path('search/', views.search, name="search"),
    path('search-results/', views.search, name='search'),
    path('logout', views.logout_view, name="logout"),
    path('subscribe', views.subscribe_email, name="subscribe"),
    path('download/<str:filter>/', views.download, name="download"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout-test/", views.checkout_test, name="checkout_test"),
    path("payments/paypal/", views.paypal, name="paypal-payment"),
    path("helpcenter/", views.helpcenter, name="help_center"),
    path('csv/', views.read_csv_file, name="csv_file"),
    path('telegram-<str:filter_text>-search-results/<str:languageSearch>/<str:keyword>-<str:additional_keyword>', views.search_page_results_additional, name='search_page_results_additional'),
    path('telegram-<str:filter_text>-search-results/<str:keyword>-<str:additional_keyword>', views.search_page_results_additional, name='search_page_results_additional'),
    # Generic pattern
    path('telegram-<str:filter_text>-search-results/<str:languageSearch>/<str:keyword>', views.search_page_results),
    path('telegram-<str:filter_text>-search-results/<str:keyword>', views.search_page_results),


    path('process_payment/', views.process_payment, name='process_payment'),
    path('webhook/', views.webhook, name='webhook'),
    path('referral-program/', views.referral_program, name='referral_program'),
    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path('delete_referral/<int:referral_id>/', views.delete_referral, name='delete_referral'),
    path('pricing', views.pricing, name='pricing'),
    path(
        "load-more-popular-posts/<int:offset>/",
        views.load_more_popular_posts,
        name="load_more_popular_posts",
    ),
    path("blog-posts-latest/", views.latest_posts, name="latest_posts"),
    path("blog-posts-case-studies/", views.case_studies, name="case_studies"),
    path("blog-search/", views.search_posts, name="search_posts"),
    path('telegram-groups-list/<int:page>', views.telegram_groups_list, name='telegram_groups_list'),
    path('telegram-groups-list/', views.telegram_groups_list, name='telegram_groups_list_default'),
    path('telegram-channels-list/<int:page>', views.telegram_channels_list, name='telegram_channels_list'),
    path('telegram-channels-list/', views.telegram_channels_list, name='telegram_channels_list_default'),

    path('telegram-members-list/<int:page>', views.telegram_members_list, name='telegram_members_list'),
    path('telegram-members-list/', views.telegram_members_list, name='telegram_members_list_default'),

    path('telegram-admins-list/<int:page>', views.telegram_admins_list, name='telegram_admins_list'),
    path('telegram-admins-list/', views.telegram_admins_list, name='telegram_admins_list_default'),
    path('all_items/', views.custom_404_handler, name='custom_404_all_items'),  # SEO HANDLER
    path('blogs/spam-in-telegram-doesnt-work/', views.custom_404_handler, name='custom_404_all_items'),  # SEO HANDLER
    path('blogs/${post.slug}/', views.custom_404_handler, name='custom_404_all_items'), # SEO HANDLER
    path('download//', views.custom_404_handler, name='custom_404_all_items'), # SEO HANDLER
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="smtp/password_reset_form.html"), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='smtp/password_reset_done.html'), name='password_reset_done'),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('password_reset_complete'), template_name="smtp/password_reset_change.html"),
        name="password_reset_confirm",
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='smtp/password_reset_complete.html'
        ),
        name='password_reset_done'
    ),
    
    #path('subscribe/', views.subscribe_view, name='posts:subscribe'),
    #path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('fetch-search-results/', views.fetch_search_results, name='fetch_search_results'),
    path('marketplace/', auth_marketplace, name='marketplace'),
    #path('unsubscribe/<uidb64>/', views.unsubscribe_view, name='unsubscribe'),



]




