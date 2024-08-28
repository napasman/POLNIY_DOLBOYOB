from authentication.models import Order, OrderHistory, Product
import logging
from django.http import Http404
from posts.models import Tag
from requests.exceptions import ConnectionError
from authentication.models import User
from django.urls import resolve
from .models import Group, Channel, Member, Admin
from itertools import chain
from django.core.paginator import Paginator, EmptyPage
from authentication.models import Order
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render
from authentication.models import Notification, TelegramProfile
from cmath import isnan
from email.policy import strict
from re import T
from io import BytesIO
from PIL import Image
import csv
import uuid
import glob
import datetime
from django.conf import settings
import time
import hmac
from django.core.files.storage import FileSystemStorage
from time import gmtime, strftime
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
    reverse,
    HttpResponseRedirect,
)
from django.http import HttpResponse
from psycopg2 import Time
from .models import (
    Contact,
    Post,
    BlogComment,
    EmailSubscriptions,
    ApiUser,
    Download,
    Group,
    Channel,
    Member,
    Admin,
    ReferralLink,
    AdLink,
    LevelThreshold,
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.forms import RegistrationForm, LoginForm
from .forms import SubscripeForm
import requests
from .ws_client import test
import asyncio
import json
from ipware import get_client_ip
from django.utils import timezone
import datetime
from pathlib import Path
import os
import uuid
from django.core.files.base import File, ContentFile
from django.http import FileResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Post
from django.contrib.auth.decorators import login_required
import random
import pandas as pd
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
import base64
import json
import hashlib
import requests
from referral.models import Campaign, Referrer, UserReferrer
from authentication.models import Notification, UserNotification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import dns.resolver
import re
from django.core.exceptions import ValidationError

BASE_DIR = Path(__file__).resolve().parent.parent
User = get_user_model()


def index(request):
    BASE_URL = "http://38.242.240.7"

    data = {
        "limit": 10,
        "chat_type": "supergroup",
        "lang": [],
        "members_count": 0,
        "keywords": ["monaco"],
        "additional_words": [],
        "stopwords": [],
        "dc_id": 0,
    }
    # response = requests.post(url = f"{BASE_URL}/search", json = data)
    # context = {
    #     "table_results":response.json()["result"]
    # }
    context = {}
    return render(request, "blog/index.html", context=context)


def about(request):
    return render(request, "blog/about.html")


def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                login(request, user)
                return HttpResponseRedirect(reverse("posts:index"))
            else:
                context["error"] = "No user found with provided details"
                return render(request, "authentication/signin.html", context=context)
        else:
            return render(request, "authentication/signin.html", context=context)
    else:
        login_form = LoginForm()
        context = {"form": login_form}
        return render(request, "authentication/signin.html", context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("posts:index"))


# Get the logger defined in settings
view_logger = logging.getLogger('view_logger')


def validate_email_with_mx(email):
    # Basic format check
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("Invalid email format.")
    domain = email.split('@')[1]
    try:
        # Check for MX records
        answers = dns.resolver.resolve(domain, 'MX')
        if not answers:
            raise ValidationError("Domain has no MX records.")
        view_logger.debug("Email's domain has MX records. Likely a valid domain.")
        print("Email's domain has MX records. Likely a valid domain.")
    except Exception as e:
        raise ValidationError(f"Domain validation error: {str(e)}")


"""
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            view_logger.debug("Email's domain: %s", email) 
            try:
                validate_email_with_mx(email)
            except ValidationError as e:
                form.add_error('email', e.message)
                context = {"form": form}
                return render(request, "authentication/signup.html", context=context)
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until they confirm their email
            user.save()

            # Send confirmation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('smtp/account_activation_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return render(request, 'smtp/account_activation_sent.html')
        else:
            context = {"form": form}
            print("Form is not valid:", form.errors)  # Add this line for debugging
            return render(request, "authentication/signup.html", context=context)
    else:
        form = RegistrationForm()

    context = {"form": form}

    return render(request, "authentication/signup.html", context=context)

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.subscribed = True 
        user.save()
        return render(request, 'smtp/activation_success.html')
    else:
        return render(request, 'smtp/activation_failure.html') 

def unsubscribe_view(request, uidb64):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.subscribed = False
        user.save()
        return render(request, 'smtp/unsubscribe.html')
    else:
        return render(request, 'smtp/unsubscribe_failure.html')
"""


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            view_logger.debug("Email's domain: %s", email)

            # Directly save the user as active, bypassing email verification
            user = form.save(commit=False)
            user.is_active = True  # Activate the user immediately
            user.subscribed = True  # Set subscribed to True if applicable
            user.save()
            
            if user:
                user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                login(request, user)
                return HttpResponseRedirect(reverse("posts:index"))
                
                

            # Redirect to the login page after successful signup
            return redirect('login')  # Assumes 'login' is the name of your login URL pattern
        else:
            context = {"form": form}
            print("Form is not valid:", form.errors)  # Add this line for debugging
            return render(request, "authentication/signup.html", context=context)
    else:
        form = RegistrationForm()

    context = {"form": form}

    return render(request, "authentication/signup.html", context=context)


def contact(request):
    if request.method == "GET":
        return render(request, "blog/contact.html")
    else:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        contact = Contact(name=name, phone=phone, email=email, desc=desc)
        contact.save()
        messages.success(request, "Your message has been sent!")
        return render(request, "blog/contact.html")


# creating telegram log for user
logger = logging.getLogger(__name__)


@csrf_exempt
def handle_telegram_auth(request):
    if request.method == 'POST':
        try:
            user_data = json.loads(request.body)
            email = f"{user_data['username']}@telegram.local"
            user, created = User.objects.get_or_create(email=email)

            if created:
                TelegramProfile.objects.create(
                    user=user,
                    telegram_id=user_data.get('id'),
                    first_name=user_data.get('first_name'),
                    username=user_data.get('username'),
                    photo_url=user_data.get('photo_url'),
                    auth_date=user_data.get('auth_date'),
                    hash=user_data.get('hash')
                )

                user.set_unusable_password()
                user.save()

            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)

            return JsonResponse({'status': 'success', 'message': 'User logged in', 'user': user_data})
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
### END OF TELEGRAM  LOGIN ###


def blog(request):
    all_posts = Post.objects.all().order_by("-publish_on")

    try:
        latest_posts = all_posts[0:3]
    except IndexError:
        latest_posts = []
        print(latest_posts)
    try:
        featured = all_posts.filter(featured=True)[0]
    except IndexError:
        featured = []
    popular_stories = all_posts.order_by("-publish_on")

    try:
        popular_stories_top = popular_stories[0:2]
    except IndexError:
        popular_stories_top = []

    try:
        popular_posts = popular_stories[2:5]
    except IndexError:
        popular_posts = []

    case_studies = all_posts.filter(case_study=True)

    subscribeForm = SubscripeForm()
    tags = Tag.objects.all()
    print(tags)
    for post in all_posts:
        print(post.author)
        try:
            role = Notification.objects.get(sender__email=post.author)
            print(role.sender_role)
            print(role.sender_level)
            level = role.sender_level
            sender_role = role.sender_role
        except:
            level = 4
            sender_role = "Administrator"
    return render(
        request,
        "blog/blog.html",
        {
            "all_posts": all_posts,
            "latest": latest_posts,
            "featured": featured,
            "case_studies": case_studies,
            "popular_stories_top": popular_stories_top,
            "popular_posts": popular_posts,
            "subscribeForm": subscribeForm,
            "role": sender_role,
            "level": level,
            "tags": tags,
        },
    )


def latest_posts(request):
    all_posts = Post.objects.all().order_by("-publish_on")

    for post in all_posts:
        print(post.author)
        try:
            role = Notification.objects.get(sender__email=post.author)
            print(role.sender_role)
            print(role.sender_level)
            level = role.sender_level
            sender_role = role.sender_role
        except:
            level = 4
            sender_role = "Administrator"

    return render(
        request,
        "blog/latest_posts.html",  # Replace with the actual template path
        {"all_posts": all_posts, "role": sender_role, "level": level},
    )


def case_studies(request):
    all_posts = Post.objects.all().order_by("-publish_on")

    for post in all_posts:
        print(post.author)
        try:
            role = Notification.objects.get(sender__email=post.author)
            print(role.sender_role)
            print(role.sender_level)
            level = role.sender_level
            sender_role = role.sender_role
        except:
            level = 4
            sender_role = "Administrator"

    return render(
        request,
        "blog/case_studies.html",  # Replace with the actual template path
        {"all_posts": all_posts, "role": sender_role, "level": level},
    )


def load_more_popular_posts(request, offset):
    # Assuming you want to load posts in chunks of 2
    chunk_size = 3
    start = int(offset)
    end = start + chunk_size

    popular_stories = Post.objects.order_by("-publish_on")
    popular_posts = popular_stories[start:end]

    data = []
    for post in popular_posts:
        data.append(
            {
                "title": post.title,
                "content": post.title,  # Adjust this field based on what you need
                "slug": post.slug,
                "heading_image": post.heading_image.url,
                "short_description": post.short_description,
                "author": {
                    "username": post.author.username,
                    "email": post.author.email,
                    # Add other user fields you want to include
                },
                "role": "Administrator",  # Adjust this based on your logic
                "level": 4,  # Adjust this based on your logic
                "publish_on": post.publish_on.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),  # Adjust the date format
                # Add other fields you want to include
            }
        )

    return JsonResponse(data, safe=False)


def custom_404_handler(request):
    # Your custom logic here, for example, redirect to the home page
    return redirect('/')  # Change 'home' to the name of your home page URL pattern


def blog_post(request, slug):
    special_slugs = ['sss', 'aaa', 'affff#!', '$%7Bpost.slug%7D', 'www',
                     'Telegram Search Engine', 'Telegram Search Engine#!', 'new-post#!']

    if slug in special_slugs:
        # Redirect to the home page or another URL of your choice
        return redirect('/')
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    all_posts = Post.objects.all().order_by("-publish_on")
    latest_posts = all_posts[0:3]
    subscribeForm = SubscripeForm()

    try:
        role = Notification.objects.get(sender__email=post.author)
        print(role.sender_role)
        print(role.sender_level)
        level = role.sender_level
        sender_role = role.sender_role
    except:
        level = 4
        sender_role = "Administrator"

    return render(
        request,
        "blog/blog-post.html",
        {
            "post": post,
            "latest": latest_posts,
            "subscribeForm": subscribeForm,
            "level": level,
            "role": sender_role,
        },
    )


def search_posts(request):
    query = request.GET.get("q", "")
    print(f"Search Query: {query}")

    # Load all posts if no search query
    if not query:
        all_posts = Post.objects.all().order_by("-publish_on")
        context = {
            "all_posts": all_posts,
            "search_query": "",
            "level": 4,
            "role": "Administrator",
        }
        return render(request, "blog/all_posts.html", context)

    search_results = Post.objects.filter(description__icontains=query).order_by("-publish_on")

    context = {
        "search_query": query,
        "search_results": search_results,
        "level": 4,
        "role": "Administrator",
    }

    return render(request, "blog/all_posts.html", context)


def postcomment(request):
    # allpost = Post.objects.all()
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        post = Post.objects.get(id=postSno)

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your Comment has been sucessfully commented")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "Your Reply has been posted sucessfully")
    return redirect(f"/blog/{post.slug}")


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def load_blacklist(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            blacklist = [line.strip() for line in file]
        return blacklist
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except UnicodeDecodeError as e:
        print(f"Error decoding file '{file_path}': {e}")
        return []


def full_lang(language_code, file_path='posts/templates/blog/languages.txt'):
    try:
        language_map = {}
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().startswith("<option"):
                    parts = line.strip().split(">")
                    if len(parts) >= 2:
                        code = parts[0].split("'")[1]
                        name = parts[1].split("<")[0]
                        language_map[code] = name
        print(language_code)
        if isinstance(language_code, list):
            language_code = language_code[0]

        if language_code in language_map:
            return language_map[language_code]
        else:
            return ""

    except Exception as e:
        print("Error loading language map:", str(e))
        return ""


def search(request):
    query = request.GET.get("query").strip()
    # browser_language = request.GET.get('browser_language').strip()
    filter = request.GET.get("filters")
    testFilter = request.GET.get("filters")
    lang = request.GET.getlist("lang")
    search_limit = request.GET.get("search-limit-range", "").split(";")[0]
    extra_keywords = request.GET.getlist("extra_keywords")
    stopwords = request.GET.getlist("stopwords")
    members_count = request.GET.get("members-count-range", "").split(";")[0]
    creation_count_range = request.GET.get("creation-count-range", "").split(";")
    rating_last_date = request.GET.get("rating-last-date", "").split(";")
    online_count_range = request.GET.get("online-count-range", "").split(";")
    rating_by_messages = request.GET.get("rating-by-messages", "").split(";")
    rating_count_range = request.GET.get("rating-count-range", "").split(";")
    search_type = request.GET.get("search_type")
    chat_type = request.GET.get("chat_type")
    print(chat_type)
    formatted_extra_keywords = []

    # Split each extra keyword into individual words
    for keyword in extra_keywords:
        formatted_extra_keywords.extend(keyword.split())

    # Convert all words to lowercase
    formatted_extra_keywords = [word.lower() for word in formatted_extra_keywords]

    # Assign the formatted_extra_keywords to extra_keywords
    extra_keywords = formatted_extra_keywords

    creation_count_range = [int(value) for value in creation_count_range if value]
    rating_last_date = [int(value) for value in rating_last_date if value]
    rating_count_range = [float(value) for value in rating_count_range if value]
    online_count_range = [float(value) for value in online_count_range if value]
    rating_by_messages = [float(value) for value in rating_by_messages if value]

    results_count = None
    results_load_time = None
    allpost = []
    BASE_URL = "http://65.109.63.135"
    split_query = query.split(" ")
    api_table_results = []
    table = None
    convert_rating = None
    convert_date = None
    converted_date = None
    convert_rating_by_messages = None
    convert_online = None
    hide_results = False
    paidUser = False
    referralUser = False
    level = 0

    # Check Browser Language
    # if browser_language != "":
    #     lang_result = [str(browser_language)[:2]]
    # else:
    #     lang_result = [].extend(lang)

    blacklist_file_path = 'posts/templates/blog/blacklist-words.txt'
    blacklist = load_blacklist(blacklist_file_path)

    if not lang:
        lang = []
    if extra_keywords == [""]:
        extra_keywords = []
    if stopwords == [""]:
        stopwords = []
    if not rating_count_range or rating_count_range[0] == 0.0:
        rating_count_range = [0]
    if not online_count_range or online_count_range[0] == 0.0:
        online_count_range = [0]
    if not creation_count_range or creation_count_range[0] == 378687600000:
        creation_count_range = [0]
    if not rating_by_messages or rating_by_messages[0] == 0.0:
        rating_by_messages = [0]
    if not rating_last_date or rating_last_date[0] == 378687600000:
        rating_last_date = [0]
    if chat_type is None:
        chat_type = ""

    if request.user.is_authenticated:
        user, _ = ApiUser.objects.get_or_create(user=request.user)
        print(user.status)
        level = user.level
        if user.status == "paid":
            paidUser = True
        else:
            paidUser = False

        if user.status == "referral":
            referralUser = True
        else:
            referralUser = False
        balance = user.balance
        userInfo = user.user.email
    else:
        try:
            this_ip = get_client_ip(request)[0]
            user = ApiUser.objects.get(ip_address=this_ip)
            balance = 50
            userInfo = this_ip
        except ApiUser.DoesNotExist:
            this_ip = get_client_ip(request)[0]
            balance = 50
            userInfo = this_ip

    if not search_limit.isnumeric():
        search_limit = 0
    if not members_count.isnumeric():
        members_count = 0

    if query and filter and not search_limit:
        search_limit = 10
    print(search_limit)
    level_thresholds = {
        1: LevelThreshold.objects.get(level=1).token,
        2: LevelThreshold.objects.get(level=2).token,
        3: LevelThreshold.objects.get(level=3).token,
        4: LevelThreshold.objects.get(level=4).token,
    }

    token = level_thresholds.get(level, "")

    words = query.split()
    # Extract the first word as the primary keyword
    split_query = [words[0]] if words else []

    if extra_keywords == [""]:
        # Extract additional words if there are more than one
        extra_keywords = words[1:] if len(words) > 1 else []

    if not request.user.is_authenticated:
        extra_keywords = words[1:] if len(words) > 1 else []
        search_type = "title_username"
        members_count = 100

    if filter == "Blog" or filter is None:
        allpost = Post.objects.filter(description__icontains=query)

    elif filter == "members":
        table = "users"

        if chat_type == "private_chat":
            to_use = "private_chat"
        else:
            to_use = "supergroup"

        if members_count == '0' or members_count == 0 or members_count is None:
            members_count = 100
            search_type = 'title_username'

        data = {
            "limit": search_limit or 0,
            "chat_type": to_use.lower(),
            "lang": lang,
            "members_count": int(members_count),
            "keywords": split_query,
            "additional_words": extra_keywords,
            "stopwords": stopwords,
            "dc_id": 0,
            "search_type": search_type,
            "token": token,
            "rating": rating_count_range,
            "online": online_count_range,
            "creation_date": creation_count_range,
            "rating_by_messages": rating_by_messages,
            "rating_last_date": rating_last_date,
        }

        try:
            response = requests.post(url=f"{BASE_URL}/users", json=data)
            print("/search members", data)
        except TimeoutError:
            response = []

        results = []

        result = response.json()["users"]
        results_count = response.json()["count"]

        if results_count != 0:
            results_count = random.randint(375, 1327)
            results_load_time = str(random.uniform(0.24, 0.54))[:4]

        if result is not None:
            results = response.json()["users"]
            api_table_results = results

        if request.user.is_authenticated:
            user, _ = ApiUser.objects.get_or_create(user=request.user)
            if user.status == "paid":
                paidUser = True
            else:
                paidUser = False
            balance = user.balance
            userInfo = user.user.email
        else:
            try:
                this_ip = get_client_ip(request)[0]
                user = ApiUser.objects.get(ip_address=this_ip)
                balance = 50
                userInfo = this_ip
            except ApiUser.DoesNotExist:
                this_ip = get_client_ip(request)[0]
                balance = 50
                userInfo = this_ip
        keyword = str(query.split()[0]).lower() if query else ""
        if len(api_table_results) > 9 and len(keyword) > 2 and keyword.isalpha():
            if not paidUser:
                filter_text = testFilter if testFilter else "default"
                keyword = str(query.split()[0]).lower() if query else ""
                additional_keyword = str(extra_keywords[0]).lower() if extra_keywords else ""

                if lang:
                    languageSearch = str(lang[0])
                else:
                    languageSearch = ""  # Set languageSearch to an empty string if lang is empty

                languageSearch = full_lang(languageSearch).lower()

                if languageSearch:
                    languageSearch = f"{languageSearch}/"  # Add a slash only if languageSearch is not empty

                if additional_keyword:
                    url = f"https://teleteg.com/telegram-{filter_text}-search-results/{languageSearch}{keyword.lower()}-{additional_keyword.lower()}"
                else:
                    url = f"https://teleteg.com/telegram-{filter_text}-search-results/{languageSearch}{keyword.lower()}"
                languageSearch = languageSearch.rstrip('/')

                if not keyword.isdigit() and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                    search_page = Member.objects.filter(
                        filter=filter_text,
                        keyword=keyword,
                        language=languageSearch,
                        additional_keyword=additional_keyword,
                    ).first()
                    if not search_page and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                        search_page = Member.objects.create(
                            url=url,
                            filter=filter_text,
                            keyword=keyword,
                            additional_keyword=additional_keyword,
                            language=languageSearch,
                            data=api_table_results[:10],
                            user=userInfo,
                            balance=balance,
                        )

    elif filter == "channels" or filter == "groups":
        table = "channels"
        to_use = filter
        if to_use == "groups":
            to_use = "supergroup"
        else:
            to_use = "channel"
        if chat_type == "private_chat":
            to_use = "private_chat"

        if members_count == '0' or members_count == 0 or members_count is None:
            members_count = 100
            search_type = 'title_username'

        data = {
            "limit": search_limit or 0,
            "chat_type": to_use.lower(),
            "lang": lang,
            "members_count": int(members_count),
            "keywords": split_query,
            "additional_words": extra_keywords,
            "stopwords": stopwords,
            "dc_id": 0,
            "search_type": search_type,
            "token": token,
            "rating": rating_count_range,
            "online": online_count_range,
            "creation_date": creation_count_range,
            "rating_by_messages": rating_by_messages,
            "rating_last_date": rating_last_date,
        }

        try:
            response = requests.post(url=f"{BASE_URL}/search", json=data)
            print("/search groups", data)

        except TimeoutError:
            response = []

        results = []
        result_filter = []
        result = response.json()["result"]
        results_count = response.json()["count"]

        if results_count != 0:
            results_count = random.randint(375, 1327)
            results_load_time = str(random.uniform(0.24, 0.54))[:4]

        # Check if result is not empty and filter it
        if result is not None:
            for x in result:
                if x["rating"] is not None:
                    convert_rating = str(x["rating"])[:4]

                if x["creation_date"] is not None:
                    convert_date = pd.to_timedelta(
                        int(x["creation_date"]), unit="s"
                    ) + pd.to_datetime("1960-1-1")
                    converted_date = (
                        str(convert_date)[5:7] + "/" + str(convert_date)[:4]
                    )

                if x["rating_by_messages"] is not None:
                    convert_rating_by_messages = str(x["rating_by_messages"])[:4]

                if x["online"] is not None:
                    convert_online = str(x["online"])[:4]
                item = {
                    "username": x["username"] if x["username"] is not None else "none",
                    "link": "https://t.me/" + x["username"]
                    if x["username"] is not None
                    else "none",
                    "title": x["title"] if x["title"] is not None else "none",
                    "members_count": x["members_count"]
                    if x["members_count"] is not None
                    else "none",
                    "description": x["description"]
                    if x["description"] is not None
                    else "none",
                    "can_send_messages": str(x["can_send_messages"]).lower()
                    if x["can_send_messages"] is not None
                    else "none",
                    "can_send_media_messages": str(x["can_send_media_messages"]).lower()
                    if x["can_send_media_messages"] is not None
                    else "none",
                    "can_send_other_messages": str(x["can_send_other_messages"]).lower()
                    if x["can_send_other_messages"] is not None
                    else "none",
                    "can_send_polls": str(x["can_send_polls"]).lower()
                    if x["can_send_polls"] is not None
                    else "none",
                    "can_add_web_page_previews": str(
                        x["can_add_web_page_previews"]
                    ).lower()
                    if x["can_add_web_page_previews"] is not None
                    else "none",
                    "can_invite_users": str(x["can_invite_users"]).lower()
                    if x["can_invite_users"] is not None
                    else "none",
                    "rating": convert_rating if convert_rating is not None else "none",
                    "creation_date": converted_date
                    if converted_date is not None
                    else "none",
                    "rating_by_messages": convert_rating_by_messages
                    if convert_rating_by_messages is not None
                    else "none",
                    "online": convert_online if convert_online is not None else "none",
                }

                result_filter.append(item)
                (
                    convert_rating,
                    convert_date,
                    converted_date,
                    convert_rating_by_messages,
                    convert_online,
                ) = (None, None, None, None, None)

            results = result_filter
            api_table_results = results

        if request.user.is_authenticated:
            user, _ = ApiUser.objects.get_or_create(user=request.user)
            if user.status == "paid":
                paidUser = True
            else:
                paidUser = False
            balance = user.balance
            userInfo = user.user.email
        else:
            try:
                this_ip = get_client_ip(request)[0]
                user = ApiUser.objects.get(ip_address=this_ip)
                balance = 50
                userInfo = this_ip
            except ApiUser.DoesNotExist:
                this_ip = get_client_ip(request)[0]
                balance = 50
                userInfo = this_ip
        keyword = str(query.split()[0]).lower() if query else ""
        if len(api_table_results) > 9 and len(keyword) > 2 and keyword.isalpha():
            if not paidUser:
                filter_text = testFilter if testFilter else "default"
                keyword = str(query.split()[0]).lower() if query else ""
                additional_keyword = str(extra_keywords[0]).lower() if extra_keywords else ""
                if lang:
                    languageSearch = str(lang[0])
                else:
                    languageSearch = ""  # Set languageSearch to an empty string if lang is empty
                languageSearch = full_lang(languageSearch).lower()

                if languageSearch:
                    languageSearch = f"{languageSearch}/"  # Add a slash only if languageSearch is not empty

                if additional_keyword:
                    url = f"https://teleteg.com/telegram-{filter_text}-search-results/{languageSearch}{keyword.lower()}-{additional_keyword.lower()}"
                else:
                    url = f"https://teleteg.com/telegram-{filter_text}-search-results/{languageSearch}{keyword.lower()}"

                if not keyword.isdigit() and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                    if filter == "channels":
                        search_page = Channel.objects.filter(
                            filter=filter_text,
                            keyword=keyword,
                            additional_keyword=additional_keyword,
                            language=languageSearch,
                        ).first()
                        if not search_page and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                            search_page = Channel.objects.create(
                                url=url,
                                filter=filter_text,
                                keyword=keyword,
                                additional_keyword=additional_keyword,
                                data=api_table_results[:10],
                                language=languageSearch,
                                user=userInfo,
                                balance=balance,
                            )
                    elif filter == "groups":
                        search_page = Group.objects.filter(
                            filter=filter_text,
                            keyword=keyword,
                            additional_keyword=additional_keyword,
                            language=languageSearch,
                        ).first()
                        if not search_page and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                            search_page = Group.objects.create(
                                url=url,
                                filter=filter_text,
                                keyword=keyword,
                                additional_keyword=additional_keyword,
                                data=api_table_results[:10],
                                language=languageSearch,
                                user=userInfo,
                                balance=balance,
                            )

    elif filter == "messages":
        result = asyncio.run(test())

    elif filter == "user":
        table = "channels"

        if chat_type == "private_chat":
            to_use = "private_chat"
        else:
            to_use = "supergroup"

        data = {
            "limit": search_limit or 0,
            "chat_type": to_use.lower(),
            "lang": lang,
            "members_count": int(members_count),
            "keywords": split_query,
            "additional_words": extra_keywords,
            "stopwords": stopwords,
            "dc_id": 0,
            "search_type": search_type,
            "token": token,
            "rating": rating_count_range,
            "online": online_count_range,
            "creation_date": creation_count_range,
            "rating_by_messages": rating_by_messages,
            "rating_last_date": rating_last_date,
        }

        try:
            response = requests.post(url=f"{BASE_URL}/user", json=data)
            print("/search user", data)
        except TimeoutError:
            response = []

        results = []

        try:
            result = response.json()["result"]
            result_filter = []
            results_count = response.json()["count"]

        except:
            result = None

        # Check if result is not empty and filter it
        if result is not None:
            for x in result:
                if x["rating"] is not None:
                    convert_rating = str(x["rating"])[:4]

                if x["creation_date"] is not None:
                    convert_date = pd.to_timedelta(
                        int(x["creation_date"]), unit="s"
                    ) + pd.to_datetime("1960-1-1")
                    converted_date = (
                        str(convert_date)[5:7] + "/" + str(convert_date)[:4]
                    )

                if x["rating_by_messages"] is not None:
                    convert_rating_by_messages = str(x["rating_by_messages"])[:4]

                if x["online"] is not None:
                    convert_online = str(x["online"])[:4]
                item = {
                    "username": x["username"] if x["username"] is not None else "none",
                    "link": "https://t.me/" + x["username"]
                    if x["username"] is not None
                    else "none",
                    "title": x["title"] if x["title"] is not None else "none",
                    "members_count": x["members_count"]
                    if x["members_count"] is not None
                    else "none",
                    "description": x["description"]
                    if x["description"] is not None
                    else "none",
                    "can_send_messages": str(x["can_send_messages"]).lower()
                    if x["can_send_messages"] is not None
                    else "none",
                    "can_send_media_messages": str(x["can_send_media_messages"]).lower()
                    if x["can_send_media_messages"] is not None
                    else "none",
                    "can_send_other_messages": str(x["can_send_other_messages"]).lower()
                    if x["can_send_other_messages"] is not None
                    else "none",
                    "can_send_polls": str(x["can_send_polls"]).lower()
                    if x["can_send_polls"] is not None
                    else "none",
                    "can_add_web_page_previews": str(
                        x["can_add_web_page_previews"]
                    ).lower()
                    if x["can_add_web_page_previews"] is not None
                    else "none",
                    "can_invite_users": str(x["can_invite_users"]).lower()
                    if x["can_invite_users"] is not None
                    else "none",
                    "rating": convert_rating if convert_rating is not None else "none",
                    "creation_date": converted_date
                    if converted_date is not None
                    else "none",
                    "rating_by_messages": convert_rating_by_messages
                    if convert_rating_by_messages is not None
                    else "none",
                    "online": convert_online if convert_online is not None else "none",
                }

                result_filter.append(item)
                (
                    convert_rating,
                    convert_date,
                    converted_date,
                    convert_rating_by_messages,
                    convert_online,
                ) = (None, None, None, None, None)
            results = result_filter
            api_table_results = results

            if request.user.is_authenticated:
                user, _ = ApiUser.objects.get_or_create(user=request.user)
            else:
                try:
                    user = ApiUser.objects.get(ip_address=this_ip)
                except ApiUser.DoesNotExist:
                    user = ApiUser(ip_address=this_ip, balance=50, status="normal")
                    user.last_api_call = timezone.now()
                    user.save()
            hide_results = True

    elif filter == "admins":
        table = "users"

        if chat_type == "private_chat":
            to_use = "private_chat"
        else:
            to_use = "supergroup"

        if members_count == '0' or members_count == 0 or members_count is None:
            members_count = 100
            search_type = 'title_username'
        data = {
            "limit": search_limit or 0,
            "chat_type": to_use.lower(),
            "lang": lang,
            "members_count": int(members_count),
            "keywords": split_query,
            "additional_words": extra_keywords,
            "stopwords": stopwords,
            "dc_id": 0,
            "search_type": search_type,
            "token": token,
            "rating": rating_count_range,
            "online": online_count_range,
            "creation_date": creation_count_range,
            "rating_by_messages": rating_by_messages,
            "rating_last_date": rating_last_date,
        }
        try:
            response = requests.post(url=f"{BASE_URL}/admins", json=data)
            print("/search admins", data)
        except TimeoutError:
            response = []

        results = []

        result = response.json()["users"]
        results_count = response.json()["count"]

        if results_count != 0:
            results_count = random.randint(375, 1327)
            results_load_time = str(random.uniform(0.24, 0.54))[:4]

        if result is not None:
            for user in result:
                convert_rating = (
                    str(user["rating"])[:4] if user["rating"] is not None else "none"
                )
                item = {
                    "username": user["username"]
                    if user["username"] is not None
                    else "none",
                    "first_name": user["first_name"]
                    if user["first_name"] is not None
                    else "none",
                    "last_name": user["last_name"]
                    if user["last_name"] is not None
                    else "none",
                    "user_id": user["user_id"]
                    if user["user_id"] is not None
                    else "none",
                    "rating": convert_rating,
                }
                results.append(item)
            api_table_results = results

        if request.user.is_authenticated:
            user, _ = ApiUser.objects.get_or_create(user=request.user)
            if user.status == "paid":
                paidUser = True
            else:
                paidUser = False
            balance = user.balance
            userInfo = user.user.email
        else:
            try:
                this_ip = get_client_ip(request)[0]
                user = ApiUser.objects.get(ip_address=this_ip)
                balance = 50
                userInfo = this_ip
            except ApiUser.DoesNotExist:
                this_ip = get_client_ip(request)[0]
                balance = 50
                userInfo = this_ip
        keyword = str(query.split()[0]).lower() if query else ""
        if len(api_table_results) > 9 and len(keyword) > 2 and keyword.isalpha():
            if not paidUser:
                filter_text = testFilter if testFilter else "default"
                keyword = str(query.split()[0]).lower() if query else ""
                additional_keyword = str(extra_keywords[0]).lower() if extra_keywords else ""

                if lang:
                    languageSearch = str(lang[0])
                else:
                    languageSearch = ""  # Set languageSearch to an empty string if lang is empty

                languageSearch = full_lang(languageSearch).lower()

                if languageSearch:
                    languageSearch = f"{languageSearch}/"  # Add a slash only if languageSearch is not empty

                if additional_keyword:
                    url = f"https://teleteg.com/telegram-{filter_text}-search-results/{languageSearch}{keyword.lower()}-{additional_keyword.lower()}"
                else:
                    url = f"https://teleteg.com/telegram-{filter_text}-search-results/{languageSearch}{keyword.lower()}"

                if not keyword.isdigit() and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                    search_page = Admin.objects.filter(
                        filter=filter_text,
                        keyword=keyword,
                        language=languageSearch,
                        additional_keyword=additional_keyword,
                    ).first()
                    if not search_page and not any(item in keyword for item in blacklist) and not any(item in additional_keyword for item in blacklist):
                        search_page = Admin.objects.create(
                            url=url,
                            filter=filter_text,
                            keyword=keyword,
                            additional_keyword=additional_keyword,
                            language=languageSearch,
                            data=api_table_results[:10],
                            user=userInfo,
                            balance=balance,
                        )

    this_ip = get_client_ip(request)[0]

    user = None

    if request.user.is_authenticated:
        user, _ = ApiUser.objects.get_or_create(user=request.user)
        if user.status == "paid":
            paidUser = True
        else:
            paidUser = False
    else:
        try:
            user = ApiUser.objects.get(ip_address=this_ip)
        except ApiUser.DoesNotExist:
            user = ApiUser(ip_address=this_ip, balance=50, status="normal")
            user.last_api_call = timezone.now()
            user.save()

    new_list = []

    user_balance = user.balance

    if chat_type == "private_chat":
        for item in api_table_results:
            if user_balance == 0:
                break
            new_list.append(item)
            user_balance = user_balance - 5
    else:
        for item in api_table_results:
            if user_balance == 0:
                break
            new_list.append(item)
            user_balance = user_balance - 1

    user.balance = user_balance

    user.save()

    api_table_results = new_list
    user.last_api_call = timezone.now()
    user.save()

    ad_links = AdLink.objects.exclude(link="").order_by("position")

    if not request.user.is_authenticated or filter == "Blog":
        return render(
            request,
            "blog/free-results.html",
            {
                "allposts": allpost,
                "query": query,
                "table_results": new_list,
                "table": table,
                "api_user": user,
                "testFilter": testFilter,
                "hide_results": hide_results,
                "paidUser": paidUser,
                "ad_links": ad_links,
                "filter": filter,
                "results_count": results_count,
                "results_load_time": results_load_time,
                "role": "Administrator",
            },
        )
    else:
        return render(
            request,
            "blog/blog-search.html",
            {
                "allposts": allpost,
                "query": query,
                "table_results": new_list,
                "table": table,
                "api_user": user,
                "testFilter": testFilter,
                "hide_results": hide_results,
                "paidUser": paidUser,
                "referralUser": referralUser,
                "level": level,
                "ad_links": ad_links,
                "filter": filter,
                "results_count": results_count,
                "results_load_time": results_load_time,
                "role": "Administrator",
            },
        )


def handleSignup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        # checks?
        if pass1 != pass2:
            messages.error(request, "Password does'nt match")
            return redirect("/")
        #    Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your MyBlog account sucessfully created")
        return HttpResponseRedirect(reverse("posts:index"))
    else:
        return HttpResponse("404 Not Found")


def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        user = authenticate(username=username, password=pass1)
        if user is not None:
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)
            messages.success(request, "You are sucessfully Login")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credients")
            return redirect("/")
    else:
        return HttpResponse("404 Not Found")


def handleLogout(request):
    logout(request)
    messages.success(request, "You are successfuly Logout")
    return redirect("/")


def subscribe_email(request):
    if request.method == "POST":
        form = SubscripeForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def download(request, filter):
    if request.method == "POST":
        data = request.POST.get("results", "")
        more = data.replace("'", '"').replace("None", '"None"')
        json_data = json.loads(data, strict=False)

        api_user = ApiUser.objects.get(user=request.user)

        read = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
        download = Download.objects.create(
            file=ContentFile(read, name=f"{uuid.uuid4()}-{filter}.json"),
            category=filter,
        )
        api_user.downloads.add(download)

        # Redirect to the file manager URL after saving the data
        return redirect("file_manager")

    # Handle GET request or other methods
    return HttpResponseNotAllowed(["POST"])


def download_file(request, file_id):
    try:
        file = Download.objects.get(id=file_id)
    except Download.DoesNotExist:
        return HttpResponse("file not found")

    # get absolute path of the file
    absolute_file_path = file.file.path

    # get the file name and extension of the file
    file_name, file_extension = os.path.splitext(file.file.name)

    # create response object
    response = FileResponse(open(absolute_file_path, "rb"))

    # add content disposition header
    response["Content-Disposition"] = 'attachment; filename= "{}"'.format(
        f"{file_name.split('/')[-1]}{file_extension}"
    )

    return response


def download_excel(request, file_id):
    try:
        file = Download.objects.get(id=file_id)
    except Download.DoesNotExist:
        return HttpResponse("File not found")

    # Get the absolute path of the file
    absolute_file_path = file.file.path

    with open(absolute_file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Create a temporary file path for the Excel file
    excel_file_path = os.path.join(settings.MEDIA_ROOT, f"{uuid.uuid4()}.xlsx")

    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)

    # Convert DataFrame to Excel format and save to file
    df.to_excel(excel_file_path, index=False)

    # Create the response object
    response = FileResponse(open(excel_file_path, "rb"))

    # Set the content type as Excel
    response[
        "Content-Type"
    ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Set the content disposition header to force download
    response["Content-Disposition"] = 'attachment; filename="data.xlsx"'

    # Delete the temporary Excel file
    os.remove(excel_file_path)

    return response


def handler404(request, template_name="404.html"):
    return render(request, "404.html", {})


# def handler500(request, template_name='500.html'):
#     return render(request,'500.html', {})


@login_required
def checkout(request):

    price_discounts = LevelThreshold.objects.all()
    orders_prices = Order.objects.all()
    price_discounts_data = serializers.serialize("json", price_discounts)
    orders_prices_data = serializers.serialize("json", orders_prices)

    return render(
        request,
        "blog/checkout.html",
        {"user": request.user, "price_discounts_data": price_discounts_data, "orders_prices_data": orders_prices_data},
    )


@login_required
def checkout_test(request):
    return render(request, "blog/checkout_test.html", {})


@csrf_exempt
@login_required
def paypal(request):
    api_user, _ = ApiUser.objects.get_or_create(user=request.user)
    data = json.loads(request.body)
    print(data)
    if data.get("marketplaceflag", False):
        return JsonResponse({"success": True, "redirect_url": "/"})

    api_user.balance = api_user.balance + data["points"]
    api_user.status = "paid"
    api_user.totalCredits += data["points"]
    api_user.save()

    return JsonResponse({"success": True, "balance": api_user.balance})


def helpcenter(request):
    return render(request, "blog/help-center.html")


def read_csv_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES["csv_file"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        file = open(os.path.join(settings.MEDIA_ROOT, filename))
        reader = csv.reader(file)
        for _ in range(1):
            next(file)

        for row in reader:
            title = row[0]
            author = request.user
            views = row[2]
            description = row[3]
            timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            slug = row[5]
            short_description = row[6]
            publish_on = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            row_9 = str(row[9])
            row_10 = row[10]
            csv_image = row[8]

            if row_9 == "TRUE":
                featured = True
            if row_9 == "FALSE":
                featured = False

            if row_10 == "TRUE":
                case_study = True
            if row_10 == "FALSE":
                case_study = False

            create_blog = Post(
                title=title,
                author=author,
                views=views,
                description=description,
                timestamp=timestamp,
                slug=slug,
                short_description=short_description,
                publish_on=publish_on,
                heading_image=csv_image,
                featured=featured,
                case_study=case_study,
            ).save()

    return render(request, "blog/upload_blogs.html")


def search_page_results(request, filter_text, keyword, languageSearch=""):
    data = []
    print(filter_text)

    # Determine the value of the table variable based on the filter
    if filter_text == "channels":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "channels"
        search_page = Channel.objects.filter(
            filter=filter_text, keyword=keyword, language=languageSearch2
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    elif filter_text == "groups":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "channels"
        search_page = Group.objects.filter(
            filter=filter_text, keyword=keyword, language=languageSearch2
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    elif filter_text == "members":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "users"
        search_page = Member.objects.filter(
            filter=filter_text, keyword=keyword, language=languageSearch
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    elif filter_text == "admins":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "users"
        search_page = Admin.objects.filter(
            filter=filter_text, keyword=keyword, language=languageSearch2
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    else:
        table = None
    # Pass the data to the template
    context = {
        "data": data,
        "table": table,
        "table_results": data,
        "language": languageSearch,
        "keyword": keyword,
        "filter": filter_text,
    }
    return render(request, "blog/search_page_results.html", context)


def search_page_results_additional(
    request, filter_text, keyword, additional_keyword, languageSearch=""
):
    data = []
    # Extract the keyword (always the first word)
    keyword_parts = keyword.split('-')
    keyword = keyword_parts[0].lower()  # Ensure keyword is lowercase

    # Extract additional keywords (if any) from URL
    additional_keywords_from_url = keyword_parts[1:]  # Extract words after the first hyphen
    # Ensure all additional keywords are lowercase
    additional_keywords_from_url = [word.lower() for word in additional_keywords_from_url]

    # Extract additional keywords (if any) from additional_keyword parameter
    additional_keywords_from_param = additional_keyword.split('-')
    # Ensure all additional keywords are lowercase
    additional_keywords_from_param = [word.lower() for word in additional_keywords_from_param]

    # Combine additional keywords from URL and additional_keyword parameter
    additional_keywords = additional_keywords_from_url + additional_keywords_from_param

    # Format additional keywords as a comma-separated string
    additional_keywords_formatted = ','.join(additional_keywords)

    # Determine the value of the table variable based on the filter
    if filter_text == "channels":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "channels"
        search_page = Channel.objects.filter(
            filter=filter_text,
            keyword=keyword,
            additional_keyword=additional_keywords_formatted,
            language=languageSearch2,
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    elif filter_text == "groups":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "channels"
        search_page = Group.objects.filter(
            filter=filter_text,
            keyword=keyword,
            additional_keyword=additional_keywords_formatted,
            language=languageSearch2,
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    elif filter_text == "members":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "users"
        search_page = Member.objects.filter(
            filter=filter_text,
            keyword=keyword,
            additional_keyword=additional_keywords_formatted,
            language=languageSearch2,
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    elif filter_text == "admins":
        languageSearch2 = languageSearch
        if languageSearch:
            languageSearch2 += '/'
        table = "users"
        search_page = Admin.objects.filter(
            filter=filter_text,
            keyword=keyword,
            additional_keyword=additional_keywords_formatted,
            language=languageSearch2,
        ).first()
        if search_page is None or search_page.data is None:
            raise Http404("No data found")
        data = search_page.data
    else:
        table = None
    # Pass the data to the template
    data = search_page.data
    additional_keywords_formatted = ' '.join(additional_keywords)
    context = {
        "data": data,
        "table": table,
        "table_results": data,
        "language": languageSearch,
        "keyword": keyword,
        "filter": filter_text,
        "additional_keyword": additional_keywords_formatted,
    }
    return render(request, "blog/search_page_results.html", context)


def telegram_groups_list(request, page=None):
    if page is None:
        return redirect('posts:telegram_groups_list', page=1)

    item_type = 'Groups'
    # Assuming _common_items_view returns an HttpResponse
    return _common_items_view(request, Group, page, item_type)


def telegram_channels_list(request, page=None):
    if page is None:
        return redirect('posts:telegram_channels_list_default')

    item_type = 'Channels'
    return _common_items_view(request, Channel, page, item_type)


def telegram_members_list(request, page=None):
    if page is None:
        return redirect('posts:telegram_members_list_default')

    item_type = 'Members'
    return _common_items_view(request, Member, page, item_type)


def telegram_admins_list(request, page=None):
    if page is None:
        return redirect('posts:telegram_admins_list_default')

    item_type = 'Admins'
    return _common_items_view(request, Admin, page, item_type)


blacklist_file_path = 'posts/templates/blog/blacklist-words.txt'


def append_to_blacklist(keyword_string):
    # Append the keyword to the blacklist file on a new line
    with open(blacklist_file_path, 'a', encoding='utf-8') as blacklist_file:
        blacklist_file.write(keyword_string + '\n')


def _common_items_view(request, model, page, item_type):
    items_per_page = 50
    items = model.objects.order_by("id")
    paginator = Paginator(items, items_per_page)
    page_number = int(page) if page else 1

    if page_number < 1 or page_number > paginator.num_pages:
        raise Http404("Invalid page number")

    try:
        current_page = paginator.page(page_number)
    except EmptyPage:
        raise Http404("Invalid page number")

    resolved_view_name = resolve(request.path_info).url_name

    if request.method == 'POST' and request.user.is_superuser:
        # Handle item deletion
        item_id = request.POST.get('item_id')
        if item_id:
            item = get_object_or_404(model, id=item_id)
            keyword = item.keyword
            additional = item.additional_keyword
            if additional:  # Check if additional is not empty
                keyword += '-' + additional

            append_to_blacklist(keyword)
            item.delete()
            # Redirect to the same page after deletion
            return redirect('posts:' + resolved_view_name, page=page_number)

    return render(
        request,
        "blog/all_items.html",
        {
            "all_page": current_page,
            "page_number": page_number,
            "item_type": item_type,
            "view_name": resolved_view_name,
        },
    )


# Get the logger defined in settings
view_logger = logging.getLogger('view_logger')


def process_payment(request):
    if request.method == "POST":
        try:
            credits_threshold = LevelThreshold.objects.get(price=request.POST.get("amount")).credits_threshold
        except:
            credits_threshold = 0

        user_email = request.POST.get("user_email")
        marketplace_flag = request.POST.get("marketplace_flag")
        marketplace_order_id = request.POST.get("marketplace_order_id")

        data = {
            "amount": request.POST.get("amount"),
            "currency": "USD",
            "network": "tron",  # Update with the actual network value
            "order_id": request.POST.get("order_id"),
            "url_return": "https://teleteg.com/users/dashboard/",
            "url_callback": "https://teleteg.com/webhook/",  # Update with your return URL
            "additional_data": json.dumps({
                "user_email": user_email,
                "marketplace_flag": marketplace_flag,
                "marketplace_order_id": marketplace_order_id,
                "credits_threshold": credits_threshold,
            }),
        }

        API_KEY = "sqNliA4ZQH4MgZVmAzbdiHHlXVYL7bPqSDosnvwCOFaXzJIBww1iGkyewipcS5R52pshTTjU9F7XevWevAN073GZSUED8hYdhdbvDe0JK57HsCot6Xm2QRE9eNJcHNXs"
        MERCHANT_ID = "b6a66031-349c-4f98-8034-c944328a1fc4"

        json_data = json.dumps(data)
        base64_data = base64.b64encode(json_data.encode()).decode()

        signature_data = base64_data + API_KEY
        sign = hashlib.md5(signature_data.encode()).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "merchant": MERCHANT_ID,
            "sign": sign,
        }

        response = requests.post(
            "https://api.cryptomus.com/v1/payment", data=json_data, headers=headers
        )
        api_response = response.json()        
        view_logger.info("API Response: %s", api_response)

        if "result" in api_response and api_response["result"] is not None:
            payment_url = api_response["result"]["url"]
            return redirect(payment_url)
        else:
            # Print the api_response content as a message on the site
            error_message = json.dumps(
                api_response, indent=4
            )  # Convert JSON to a readable string
            return JsonResponse(
                {
                    "message": f"Payment URL not available. API Response:\n{error_message}"
                }
            )

    return JsonResponse({"message": "Invalid request method"})


@csrf_exempt
def webhook(request):
    if request.method == "POST":

        data = json.loads(request.body)        
        view_logger.info("Received webhook data: %s", data)

        if data.get("status") == "paid" or data.get("status") == "paid_over":
            additional_data = json.loads(data.get("additional_data"))
            user_email = additional_data.get("user_email")
            marketplace_flag = additional_data.get("marketplace_flag")
            marketplace_order_id = additional_data.get("marketplace_order_id")
            credits_threshold = additional_data.get("credits_threshold")

            # Now you can use user_email and marketplace_flag as needed
            if marketplace_flag == "true":
                try:
                    if not marketplace_order_id.startswith("#"):
                        marketplace_order_id = "#" + marketplace_order_id
                    order = Order.objects.get(order_number=marketplace_order_id)
                    user = User.objects.get(email=user_email)
                    order_history_entry = OrderHistory.objects.create(
                        order_number=marketplace_order_id,
                        user=user,  # Assuming the user is authenticated
                        price=order.price,
                    )
                    api_user = ApiUser.objects.get(user__email=user_email)
                    file = order.file
                    download = Download.objects.create(
                        file=file, category="marketplace orders", created=order_history_entry.date)
                    # Add the product's file to the ApiUser's downloads
                    api_user.downloads.add(download)
                    # Save the ApiUser instance
                    api_user.save()
                    # Send email to the user with the file attached
                    subject = 'Thanks for purchase!'
                    message = 'Please find attached the file for your order.'
                    email_from = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [user_email]
                    email = EmailMessage(subject, message, email_from, recipient_list)
                    # Attach the file to the email
                    email.attach_file(download.file.path)
                    # Send the email
                    email.send(fail_silently=False)

                    if order.tabs == 'accounts':
                        order.delete()

                    return redirect('file_manager')

                except Order.DoesNotExist:
                    # Handle the case where order_number does not exist                    
                    return JsonResponse({"success": False, "message": "Order not found"})

            if user_email:
                try:
                    api_user = ApiUser.objects.get(user__email=user_email)
                    original_amount = float(data.get("amount"))
                    try:
                        credits_threshold = int(credits_threshold)
                    except:
                        credits_threshold = 0
                    if credits_threshold > 0:
                        payer_amount = credits_threshold
                    else:
                        payer_amount = int(original_amount / 0.025)

                    api_user.balance += payer_amount
                    api_user.status = (
                        "paid"  # You can set this to 'paid_over' if needed
                    )
                    api_user.totalCredits += payer_amount
                    api_user.save()

                except ApiUser.DoesNotExist:
                    return JsonResponse({"success": False, "message": "User not found"})

                return JsonResponse(
                    {"success": True, "message": "Webhook data processed successfully"}
                )

    return JsonResponse({"success": False, "message": "Invalid webhook data"})


def referral_program(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        pattern = request.POST.get("pattern")

    referral_code = request.GET.get("referral_code")
    if referral_code:
        try:
            referral_link = ReferralLink.objects.get(referral_pattern=referral_code)

            # Check if the user's IP or cookie has been tracked before
            tracking_key = f"referral_click_{referral_code}"
            if tracking_key not in request.session:
                # Increment the clicks count and set the tracking session
                referral_link.clicks += 1
                referral_link.save()
                request.session[tracking_key] = True

                # Update ApiUser's balance
                if referral_link.user_id:
                    try:
                        api_user = ApiUser.objects.get(user_id=referral_link.user_id)
                        api_user.balance += 1  # Update the user's balance
                        api_user.status = "referral"
                        api_user.save()
                    except ApiUser.DoesNotExist:
                        pass

        except ReferralLink.DoesNotExist:
            pass

        # Redirect to the home page when referral_code parameter is present
        return redirect("/")

    referral_links = ReferralLink.objects.filter(user_id=request.user.id)

    false_count = 0
    notifications = Notification.objects.all()
    # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        if request.user.is_authenticated:
            try:
                user_notification = UserNotification.objects.get(
                    user=request.user, notification=notification
                )
                is_read = user_notification.is_read
            except UserNotification.DoesNotExist:
                is_read = False  # Default to False if no UserNotification exists
        else:
            return redirect('login')

        print(f"Notification Title: {notification.title}, Is Read: {is_read}")
        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values

    if request.user.is_authenticated:
        try:
            api_user = ApiUser.objects.get(user=request.user)
            if api_user.status == "paid":
                paidUser = True
            else:
                paidUser = False
        except ApiUser.DoesNotExist:
            print("happening")
            this_ip = get_client_ip(request)[0]
            api_user = ApiUser.objects.create(user=request.user)

    return render(
        request,
        "blog/referral_program.html",
        {
            "user": request.user,
            "referral_links": referral_links,
            "api_user": api_user,
            "notifications": notifications,
            "false_count": false_count,
        },
    )


def generate_unique_pattern():
    return str(uuid.uuid4())[
        :6
    ]  # Generate a UUID and use the first 6 characters as the pattern


def create_campaign(request):
    if request.method == "POST":
        user_id = request.user.id if request.user.is_authenticated else None

        # Get the last referral link associated with the user
        last_referral_link = (
            ReferralLink.objects.filter(user_id=user_id).order_by("-order_id").first()
        )

        # Extract the numeric part and increment it by 1
        if last_referral_link:
            last_order_numeric_part = int(
                last_referral_link.order_id[3:]
            )  # Assuming the format is "#RLXX"
            next_order_id = f"#RL{last_order_numeric_part + 1:02d}"
        else:
            next_order_id = (
                "#RL01"  # Default if there are no existing orders for the user
            )

        unique_pattern = (
            generate_unique_pattern()
        )  # Implement a function to generate unique patterns

        # Create the referral link with the generated order_id
        referral_link = ReferralLink.objects.create(
            order_id=next_order_id,
            clicks=0,
            link_code=f"http://{request.get_host()}/referral-program/?referral_code={unique_pattern}",
            referral_pattern=unique_pattern,
            user_id=user_id,
        )

        return redirect("posts:referral_program")  # Redirect to home page

    referral_links = ReferralLink.objects.all()
    return render(
        request,
        "blog/referral_program.html",
        {"user": request.user, "referral_links": referral_links},
    )


def delete_referral(request, referral_id):
    referral = get_object_or_404(ReferralLink, id=referral_id)
    referral.delete()
    return redirect(
        "posts:referral_program"
    )  # Redirect back to the referral program page


def pricing(request):
    return render(request, "blog/pricing.html")


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the home page on successful form submission
            return redirect('posts:index')  # Replace 'home' with the actual name of your home URL pattern
    else:
        form = SubscribeForm()

    return render(request, 'blog.html', {'subscribeForm': form})


logging.basicConfig(filename='debug.log', level=logging.DEBUG)
logger = logging.getLogger('view_logger')


def create_and_save_instance(model_class, data):
    # Remove unexpected keyword arguments
    data.pop('username', None)
    # Create and save the instance
    instance = model_class.objects.create(**data)
    instance.save()


def fetch_search_results(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            requestData = data.get('requestData')
            if not requestData:
                return HttpResponseBadRequest("Invalid requestData")
            keywords = requestData.get('keywords', [])
            additional_keywords = requestData.get('additionalKeywords', [])
            filters = requestData.get('filters', [])
            languages = requestData.get('languages', [])
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
            logger.info(f"user agent: {user_agent}")

            stopwords = []
            delay_between_requests = 0.5

            BASE_URL = "http://65.109.63.135"

            # Initialize results variables
            results = []
            results_count = 0

            # Process the keywords data
            for keyword, additional_keyword, filter, language in zip(keywords, additional_keywords, filters, languages):
                # Process the corresponding elements together
                if keyword is None:
                    print("Keyword is None")
                elif additional_keyword is None:
                    print("Additional Keyword is None")
                elif filter is None:
                    print("Filter is None")
                elif language is None:
                    print("Language is None")
                else:
                    # Process the corresponding elements together
                    print(
                        f"Keyword: {keyword}, Additional Keyword: {additional_keyword}, Filter: {filter}, Language: {language}")
                if not language:
                    language = []
                else:
                    language = [language]
                to_use = filter
                if filter == 'groups':
                    to_use = "supergroup"
                elif filter == 'members':
                    to_use = "supergroup"
                elif filter == 'admins':
                    to_use = "supergroup"
                elif filter == 'channels':
                    to_use = "channel"

                if not additional_keyword:
                    additional_keyword = []
                else:
                    additional_keyword = additional_keyword.split()
                if filter == 'admins' or filter == 'members' and not stopwords:
                    stopwords = []
                logger.info(
                    f"Processing keyword: {keyword}, additional_keyword: {additional_keyword}, filter: {filter}, language: {language}")

                try:
                    data = {
                        "limit": 10,
                        "chat_type": to_use.lower(),  # Assuming a default chat type
                        "lang": language,
                        "members_count": 100,  # Assuming a default members count
                        "keywords": additional_keyword,  # Process one keyword at a time
                        "additional_words": [keyword],
                        "stopwords": stopwords,
                        "dc_id": 0,
                        "search_type": "title_username",
                        'token': 'GW56DDnw7BsVwF==',
                        "rating": [0],  # Default rating count range
                        "online": [0],  # Default online count range
                        "creation_date": [0],  # Default creation date range
                        "rating_by_messages": [0],  # Default rating by messages range
                        "rating_last_date": [0],  # Default rating last date range
                    }
                    keyword_results = None
                    # Determine the model class based on the filter
                    model_class = None
                    if filter == 'groups':
                        response = requests.post(url=f"{BASE_URL}/search", json=data)
                        model_class = Group
                        keyword_results = response.json()["result"]
                    elif filter == 'members':
                        response = requests.post(url=f"{BASE_URL}/users", json=data)
                        model_class = Member
                        keyword_results = response.json()["users"]
                    elif filter == 'admins':
                        response = requests.post(url=f"{BASE_URL}/admins", json=data)
                        model_class = Admin
                        keyword_results = response.json()["users"]
                    elif filter == 'channels':
                        response = requests.post(url=f"{BASE_URL}/search", json=data)
                        model_class = Channel
                        keyword_results = response.json()["result"]

                    print("Search", data)
                    logger.error(f"Search response data: {data}")

                    if keyword_results is None:
                        logger.error(f"Empty API response for keyword: {keyword}")

                        continue

                    if language == []:
                        language = ''
                    if isinstance(language, list) and len(language) == 1:
                        language = language[0]

                    language = full_lang(language).lower()
                    if language:
                        language = f"{language}/"  # Add a slash only if languageSearch is not empty

                    if additional_keyword:
                        additional_keywords_str = "-".join([word.lower() for word in additional_keyword])
                        url = f"https://teleteg.com/telegram-{filter}-search-results/{language}{keyword.lower()}-{additional_keywords_str}"
                    else:
                        url = f"https://teleteg.com/telegram-{filter}-search-results/{language}{keyword.lower()}"

                    if additional_keyword == []:
                        additional_keyword = ''
                    elif isinstance(additional_keyword, list) and len(additional_keyword) == 1:
                        additional_keyword = additional_keyword[0]
                    else:
                        additional_keyword = ','.join(additional_keyword)

                    existing_instance = model_class.objects.filter(
                        filter=filter,
                        keyword=keyword,
                        language=language,
                        additional_keyword=additional_keyword
                    ).first()

                    # Create and save model instances based on the results
                    if not existing_instance and len(keyword_results) > 9 and len(keyword) > 2 and keyword.isalpha():
                        create_and_save_instance(model_class, {
                            'url': url,
                            'filter': filter,
                            'keyword': keyword,
                            'additional_keyword': additional_keyword,
                            'language': language,  # Assuming language is provided
                            'data':  keyword_results[:10],  # Assuming you want to store only the first 10 results
                            'user': "bulkpages",  # Assuming the current user is associated with this data
                            'balance': 10,  # Assuming balance is related to the user
                        })

                except ConnectionError as e:
                    logger.error(f"ConnectionError occurred while processing keyword '{keyword}': {e}")
                    time.sleep(1)
                    # Handle the error gracefully (e.g., log the error, continue to the next keyword)
                    continue

                except Exception as e:
                    logger.exception(f"An error occurred while processing keyword '{keyword}': {e}")
                    # Handle exceptions here
                    print(f"Error fetching results for keyword '{keyword}': {str(e)}")

            return redirect('/users/dashboard/customers')
        except json.JSONDecodeError:
            logger.exception("Invalid JSON data in request body")
            return JsonResponse({"error": "Invalid JSON data in request body"})
    else:
        return JsonResponse({"error": "Invalid request method"})
