"""
module for authentication models
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from .managers import CustomUserManager
from django.conf import settings


class User(AbstractUser):
    """
    custom user model
    """
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    subscribed = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_photo_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            return "/media/profile_pictures/defaultProfile.jpg"

from posts.models import ApiUser
class Notification(models.Model):
    SENDER_ROLES = (
        ('Administrator', 'Administrator'),
        ('Leader', 'Leader'),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sender_role = models.CharField(max_length=20, choices=SENDER_ROLES)
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Add a sender_level field to store the sender's level
    sender_level = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender.email} ({self.sender_role}): {self.message}"

    def save(self, *args, **kwargs):
        # Automatically populate the sender's level when saving the notification
        if self.sender:
            try:
                api_user = ApiUser.objects.get(user__email=self.sender.email)
                self.sender_level = api_user.level
            except ApiUser.DoesNotExist:
                # Handle the case where the sender is not associated with an ApiUser
                pass

        super(Notification, self).save(*args, **kwargs)


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    



class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    productName = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    price = models.IntegerField()
    file = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TAB_CHOICES = [
        ('accounts', 'Accounts'),
        ('database', 'Database'),
    ]
    tabs = models.CharField(max_length=20, choices=TAB_CHOICES, default='accounts')

    def save(self, *args, **kwargs):
        # Generate unique order number
        if not self.order_number:
            self.order_number = self.generate_order_number()

        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Get the latest order to determine the next order number
        latest_order = Order.objects.order_by('-id').first()

        if latest_order:
            # Extract the numeric part of the order number and increment it
            last_order_number = int(latest_order.order_number[4:])  # Extract numbers after "#SK"
            next_order_number = last_order_number + 1
        else:
            next_order_number = 1  # Start from 1 if no previous orders exist

        # Format the next order number with leading zeros
        formatted_order_number = f'#SK{next_order_number:05}'  # Pad with zeros to ensure 5 digits

        return formatted_order_number

    def __str__(self):
        return self.order_number

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='order_images/')
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.name


class OrderHistory(models.Model):
    order_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ID: {self.order_number}, User ID: {self.user.id}, Price: ${self.price}"
    

class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_profile')
    telegram_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    photo_url = models.URLField(blank=True, null=True)
    auth_date = models.PositiveIntegerField(blank=True, null=True)
    hash = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username