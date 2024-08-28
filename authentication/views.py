"""
views for authentication
"""
from django.db.models import Q
from re import A
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from posts.models import ApiUser, ReferralLink
from ipware import get_client_ip
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Notification
from django import forms

from django.db.models import F


@login_required
def login_redirect(request):
    """
    function to redirect user after login
    """
    return redirect(reverse("/",))


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                print("Authentication failed")  # Add this line for debugging
        else:
            context = {'form': form}
            print(form.errors)  # Add this line for debugging
            return render(request, 'authentication/signup.html', context=context)
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'authentication/signup.html', context=context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        context = {"form":form}

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return HttpResponseRedirect(reverse('posts:index'))
            else:
                 context['error'] = "No user found with provided details"
                 return  render(request,'authentication/signin.html', context=context)
        else:
            return  render(request,'authentication/signin.html', context=context)
    else:
        login_form = LoginForm()
        context = {"form":login_form}
        return render(request,'authentication/signin.html', context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
import logging

logger = logging.getLogger(__name__)


@login_required
def user_dashboard(request):
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    api_user = None
    paidUser = False
    referralUser = False
    level = 0
    notifications = Notification.objects.all()
    unread_message_count = 0
    user = request.user
    false_count = 0

    if request.user:
        try:
            api_user = ApiUser.objects.get(user=request.user)
            level = api_user.level
            if api_user.status == 'paid':
                paidUser = True
            else:
                paidUser = False
            if api_user.status == 'referral':
                referralUser = True
            else:
                referralUser = False
        except ApiUser.DoesNotExist:
            print("happening")
            this_ip = get_client_ip(request)[0]
            api_user = ApiUser.objects.create(user=request.user)


      # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        try:
            user_notification = UserNotification.objects.get(user=user, notification=notification)
            is_read = user_notification.is_read
        except UserNotification.DoesNotExist:
            is_read = False  # Default to False if no UserNotification exists

        print(f"Notification Title: {notification.title}, Is Read: {is_read}")
        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values
        print(false_count)       
    context = {"api_user":api_user, "paidUser": paidUser, "referralUser": referralUser, "level":level, 'notifications': notifications, 'false_count': false_count}    

    if request.user.is_superuser:
        context['users'] = ApiUser.objects.all()

    return render(request, "authentication/user_dashboard.html", context=context)

@login_required
def view_files(request, category):
    api_user = None
    notifications = Notification.objects.all() 
    try:
        api_user = ApiUser.objects.get(user=request.user)
    except ApiUser.DoesNotExist:
        this_ip = get_client_ip(request)[0]
        api_user = ApiUser.objects.create(user=request.user, ip_address=this_ip)

    files = api_user.downloads.filter(category__iexact=category)

    false_count = 0

    # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        try:
            user_notification = UserNotification.objects.get(user=request.user, notification=notification)
            is_read = user_notification.is_read
        except UserNotification.DoesNotExist:
            is_read = False  # Default to False if no UserNotification exists

        print(f"Notification Title: {notification.title}, Is Read: {is_read}")
        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values

    context = {"api_user":api_user, "category":category, "files":files, 'notifications' : notifications, 'false_count' : false_count}    

    return render(request, "authentication/viewFiles.html", context=context)


@login_required
def file_manager(request):
    notifications = Notification.objects.all() 
    try:
        api_user = ApiUser.objects.get(user=request.user)
    except ApiUser.DoesNotExist:
        this_ip = get_client_ip(request)[0]
        api_user = ApiUser.objects.create(user=request.user, ip_address=this_ip)

    false_count = 0

    # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        try:
            user_notification = UserNotification.objects.get(user=request.user, notification=notification)
            is_read = user_notification.is_read
        except UserNotification.DoesNotExist:
            is_read = False  # Default to False if no UserNotification exists

        print(f"Notification Title: {notification.title}, Is Read: {is_read}")
        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values

    context = {"api_user":api_user, 'notifications' : notifications, 'false_count' : false_count}    

    return render(request, "authentication/filemanager.html", context=context)




from authentication.models import User


@login_required
def users(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = forms.Form(request.POST)
            sender_role = request.POST.get('sender_role')
            message = request.POST.get('message')

            if sender_role and message:
                sender = request.user.email
                sender_level = None

                if sender:
                    try:
                        user = User.objects.get(email=sender)  # Retrieve the User instance
                        notification = Notification(
                            sender=user,
                            sender_role=sender_role,
                            sender_level=sender_level,
                            message=message,
                        )
                        notification.save()
                    except User.DoesNotExist:
                        # Handle the case where the sender's email does not correspond to a User
                        pass

                return redirect('/users/dashboard/customers') 

        else:
            form = forms.Form()
        notifications = Notification.objects.all()    
        api_user = ApiUser.objects.get(user=request.user)

        all_user_list = ApiUser.objects.exclude(user__name='', user__email='').exclude(user__email__isnull=True).order_by('-balance', 'pk')
        free_user_list = ApiUser.objects.filter(Q(user__email='') | Q(user=None)).order_by('-balance', 'pk')

        paginator = Paginator(all_user_list, 10)  # Display 10 users per page
        free_paginator = Paginator(free_user_list, 10)  # Display 10 free users per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        free_page_number = request.GET.get('free_page')
        free_page_obj = free_paginator.get_page(free_page_number)
        

        referral_links = ReferralLink.objects.all().order_by('-clicks', 'pk')
        referral_paginator = Paginator(referral_links, 10)  # Display 5 referral links per page

        referral_page_number = request.GET.get('referral_page')
        referral_page_obj = referral_paginator.get_page(referral_page_number)


        false_count = 0

        # Iterate through the notifications and check the is_read status for the user
        for notification in notifications:
            try:
                user_notification = UserNotification.objects.get(user=request.user, notification=notification)
                is_read = user_notification.is_read
            except UserNotification.DoesNotExist:
                is_read = False  # Default to False if no UserNotification exists

            print(f"Notification Title: {notification.title}, Is Read: {is_read}")
            if not is_read:  # Check if is_read is False
                false_count += 1  # Increment the counter for False values






        context = {
            "users": page_obj,
            "free_users": free_page_obj,
            "api_user": api_user,
            'referral_links': referral_page_obj,
            'notifications': notifications,
            'false_count' : false_count,
        }
        return render(request, "authentication/userlist.html", context=context)
    return redirect("/")

from django.shortcuts import render, get_object_or_404
from .models import  UserNotification, Notification



def view_all_notifications(request):
    user = request.user  # Get the current user
    notifications = Notification.objects.all()  # Fetch all notifications from your database

    api_user = None
    false_count = 0
   

    if request.user:
        try:
            api_user = ApiUser.objects.get(user=request.user)
        except ApiUser.DoesNotExist:
            print("happening")
            this_ip = get_client_ip(request)[0]
            api_user = ApiUser.objects.create(user=request.user)

    # Create a list to store tuples of notifications and their read statuses
    notifications_with_status = []

    # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        try:
            user_notification = UserNotification.objects.get(user=user, notification=notification)
            is_read = user_notification.is_read
        except UserNotification.DoesNotExist:
            is_read = False  # Default to False if no UserNotification exists

        # Append a tuple of notification and its read status to the list
        notifications_with_status.append((notification, is_read))
        print(f"Notification Title: {notification.title}, Is Read: {is_read}")
        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values
        print(false_count)



    context = {'notifications_with_status': notifications_with_status, 'notifications' : notifications, 'api_user': api_user, 'false_count': false_count}
    return render(request, 'authentication/allNotifications.html', context)


from django.db.models import F

def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    user = request.user

    # Get or create the UserNotification for the specific notification
    user_notification, created = UserNotification.objects.get_or_create(user=user, notification=notification)

    # Mark the user's notification as read (if it's not already marked as read)
    if not user_notification.is_read:
        user_notification.is_read = True
        user_notification.save()

        # Mark all other notifications from the same user as read
        UserNotification.objects.filter(user=user, is_read=False).update(is_read=True)

    # Fetch all notifications (including updated read statuses) for rendering in the template
    notifications = Notification.objects.all()

    api_user = None
   

    if request.user:
        try:
            api_user = ApiUser.objects.get(user=request.user)
        except ApiUser.DoesNotExist:
            print("happening")
            this_ip = get_client_ip(request)[0]
            api_user = ApiUser.objects.create(user=request.user)

    return render(request, 'authentication/notification_detail.html', {'notification': notification,'api_user':api_user, 'is_read': user_notification.is_read, 'notifications': notifications})
    
    
    
    


def delete_notification(request, notification_id):
    # Get the notification object
    notification = get_object_or_404(Notification, id=notification_id)

    # Check if the sender is an administrator (you can adjust this condition as needed)
    if notification.sender_role == "Administrator" or notification.sender_role == "Leader":
        # Delete the notification
        notification.delete()
    
    # Redirect back to the notification list page
    return redirect('view_all_notifications')    
    
# views.py
import threading
import time
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages



def send_email_async(request):
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


import requests
from django.shortcuts import render
from django.http import HttpResponse


def bulk_pages(request):
    if request.method == 'POST' and request.FILES.get('bulk_keywords_file'):
        uploaded_file = request.FILES['bulk_keywords_file']
        # Process the uploaded file here
        content = uploaded_file.read().decode('utf-8')
        # Extract keywords and filters from each line
        keyword_filter_list = [line.strip().split() for line in content.split('\n') if line.strip()]
        # Print or process the keyword-filter pairs as needed
        for keyword_filter in keyword_filter_list:
            if len(keyword_filter) >= 2:
                keyword = keyword_filter[0]
                filter_text = keyword_filter[1]
                print("Keyword:", keyword)
                print("Filter:", filter_text)
                # Fetch data from the URL
                url = f"https://teleteg.com/search-results/?query={keyword}&filters={filter_text}&search-limit-range=100%3B221&extra_keywords=&members-count-range=0%3B5000&stopwords=&rating-count-range=0%3B2"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()  # Assuming the response is in JSON format
                    print(data)
                    # Process the data as needed
                else:
                    print("Error fetching data from URL:", url)

        return HttpResponse("File uploaded successfully")
    else:
        return HttpResponse("No file uploaded or invalid request")



from .models import Order, Product
def marketplace(request):
    notifications = Notification.objects.all() 
    if request.user.is_authenticated:
        try:
            api_user = ApiUser.objects.get(user=request.user)
        except ApiUser.DoesNotExist:
            # Create a new ApiUser instance if it doesn't exist
            this_ip = get_client_ip(request)[0]
            api_user = ApiUser.objects.create(user=request.user, ip_address=this_ip)
    else:
        # Handle anonymous user
        api_user = None
    false_count = 0

    # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        if request.user.is_authenticated:
            try:
                user_notification = UserNotification.objects.get(user=request.user, notification=notification)
                is_read = user_notification.is_read
            except UserNotification.DoesNotExist:
                is_read = False  # Default to False if no UserNotification exists
        else:
            # For anonymous user, set is_read to False
            is_read = False

        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values

    regular_orders = Order.objects.filter(tabs='accounts')
    database_orders = Order.objects.filter(tabs='database')
    context = {"api_user":api_user, 'notifications' : notifications, 'false_count' : false_count, 'regular_orders': regular_orders, 'database_orders': database_orders}    
    if request.user.is_authenticated:
        return render(request, 'authentication/marketplace.html', context=context)
    else:
        return render(request, 'authentication/marketplace-withoutLogin.html', context=context)

from django.http import JsonResponse
def order_details(request):
    if request.method == 'GET' and 'order_id' in request.GET:
        order_id = request.GET['order_id']
        # Fetch the order details from the database based on the order_id
        order = Order.objects.get(id=order_id)
        # Construct a dictionary containing the order details
        order_details = {
            'order_number': order.order_number,
            'name': order.productName,
            'seller': order.role,
            'price':order.price,
            'user': order.user.email,
            'file_name': order.file.name.split('/')[-1] if order.file else None,
        }
        # Return the order details as JSON response
        return JsonResponse(order_details)

from django.contrib.auth.decorators import user_passes_test


import logging
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            field = request.POST.get('field')
            new_value = request.POST.get('new_value')
            print(order_id, field, new_value)  # Add this line to print received data

            # Update the order record in the database
            order = Order.objects.get(pk=order_id)
            setattr(order, field, new_value)
            order.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})




def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        # Check the referrer URL
        referrer = request.META.get('HTTP_REFERER')
        if referrer and 'marketplace' in referrer:
            # If the referrer URL contains 'marketplace', redirect back to marketplace listings
            return HttpResponseRedirect(reverse('posts:marketplace'))
        else:
            # Otherwise, redirect to a generic listings page
            return HttpResponseRedirect(reverse('marketplaceListings'))
    except Order.DoesNotExist:
        # Handle the case where the order does not exist
        # Redirect to the appropriate page based on referrer URL
        referrer = request.META.get('HTTP_REFERER')
        if referrer and 'marketplace' in referrer:
            return HttpResponseRedirect(reverse('posts:marketplace'))
        else:
            return HttpResponseRedirect(reverse('marketplaceListings'))
    

@login_required
def save_new_order(request):
    if request.method == 'POST':
        # Extract order data from the request
        role = 'Admin Level 4'
        price = request.POST.get('price')
        productName = request.POST.get('numAccounts')
        file = request.FILES.get('productFile')
        selected_tab = request.POST.get('selectedTab')

        try:
            print(f"Creating order: Name={role}, Price={price}, ProductName={productName}, File={file}")
            # Create a new Order instance and save it to the database
            order = Order.objects.create(role=role, price=price, productName=productName, user=request.user, file=file, tabs=selected_tab)
            print("Order created successfully")
          
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderHistory
from posts.models import Download
from django.core.mail import EmailMessage
@csrf_exempt
def create_order_history_entry(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print("Received POST request to create order history entry for order ID:", order_id)  # Debug print
        try:
            if not order_id.startswith('#'):
                order_id = '#' + order_id
            order = Order.objects.get(order_number=order_id)
            print("Order found with ID:", order_id)  # Debug print
            # Create OrderHistory entry
            price = order.price
            order_history_entry = OrderHistory.objects.create(
                order_number=order_id,
                user=request.user,  # Assuming the user is authenticated
                price=price,
            )
          
            api_user = ApiUser.objects.get(user=request.user)
            file = order.file
            download = Download.objects.create(file=file, category="marketplace orders", created=order_history_entry.date)
            # Add the product's file to the ApiUser's downloads
            api_user.downloads.add(download)
            # Save the ApiUser instance
            api_user.save()
            """
             # Send email to the user with the file attached
            subject = 'Thanks for purchase!'
            message = 'Please find attached the file for your order.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]
            email = EmailMessage(subject, message, email_from, recipient_list)
            # Attach the file to the email
            email.attach_file(download.file.path)
            # Send the email
            email.send(fail_silently=False)
            """
            
            print("Order history entry created successfully")  # Debug print
            if order.tabs == 'accounts':
                order.delete()
            return JsonResponse({'success': True, 'message': 'Order history entry created successfully'})
        except Order.DoesNotExist:
            print("Order not found with ID:", order_id)  # Debug print
            return JsonResponse({'success': False, 'error': 'Order not found'})
    print("Invalid request method")  # Debug print
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
@login_required
def marketplaceListings(request):
    notifications = Notification.objects.all() 
    if request.user.is_authenticated:
        try:
            api_user = ApiUser.objects.get(user=request.user)
        except ApiUser.DoesNotExist:
            # Create a new ApiUser instance if it doesn't exist
            this_ip = get_client_ip(request)[0]
            api_user = ApiUser.objects.create(user=request.user, ip_address=this_ip)
    else:
        # Handle anonymous user
        api_user = None
    false_count = 0

    # Iterate through the notifications and check the is_read status for the user
    for notification in notifications:
        if request.user.is_authenticated:
            try:
                user_notification = UserNotification.objects.get(user=request.user, notification=notification)
                is_read = user_notification.is_read
            except UserNotification.DoesNotExist:
                is_read = False  # Default to False if no UserNotification exists
        else:
            # For anonymous user, set is_read to False
            is_read = False

        if not is_read:  # Check if is_read is False
            false_count += 1  # Increment the counter for False values

    orders = Order.objects.filter(user=request.user)
    context = {"api_user":api_user, 'notifications' : notifications, 'false_count' : false_count, 'orders': orders}    
    return render(request, 'authentication/listings.html', context=context)
