from webbrowser import get
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth import get_user_model
import os
# from referral.models import Campaign
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=300)
    phone = models.CharField(max_length=30)
    desc = models.CharField(max_length=3000)

    def __str__(self):
        return self.name


from django.db.models import ManyToManyField
from ckeditor.fields import RichTextField


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    description = RichTextUploadingField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)
    slug = models.CharField(max_length=33, unique=True)
    short_description = models.TextField(max_length=400)
    publish_on = models.DateTimeField()
    heading_image = models.ImageField(
        blank=True, default="profile_pictures/images_3.jpg"
    )
    featured = models.BooleanField(default=False)
    case_study = models.BooleanField(default=False)
    tags = ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title + " by " + self.author.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    comment = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "... " + " by " + self.user.username


class EmailSubscriptions(models.Model):
    email = models.CharField(max_length=1028)

    def __str__(self):
        return self.email


class Download(models.Model):
    file = models.FileField()
    category = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.file.name)


class LevelThreshold(models.Model):
    level = models.IntegerField(unique=True)
    credits_threshold = models.IntegerField()
    token = models.CharField(max_length=20, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return f"Level {self.level}: {self.credits_threshold} credits. ${self.price} : Token {self.token}:"

    class Meta:
        ordering = ["level"]


class ApiUser(models.Model):
    ip_address = models.CharField(max_length=20, blank=True)
    balance = models.IntegerField(default=0)
    status = models.CharField(max_length=20, blank=True)
    level = models.IntegerField(default=0)
    totalCredits = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="api_users"
    )
    last_api_call = models.DateTimeField(null=True, blank=True)
    downloads = models.ManyToManyField(Download, blank=True)

    def __str__(self):
        if self.user:
            return self.user.email
        else:
            return self.ip_address


@receiver(pre_save, sender=ApiUser)
def update_user_level(sender, instance, **kwargs):
    # Get the level thresholds and corresponding credit amounts from the LevelThreshold model
    level_thresholds = LevelThreshold.objects.order_by("level")

    # Iterate through the thresholds in reverse order
    for level_threshold in reversed(level_thresholds):
        if instance.totalCredits >= level_threshold.credits_threshold:
            instance.level = level_threshold.level
            break


class SearchItem(models.Model):
    url = models.URLField()
    filter = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    additional_keyword = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    data = models.JSONField()
    user = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)


class Group(SearchItem):
    pass

    def __str__(self):
        return self.url


class Channel(SearchItem):
    pass

    def __str__(self):
        return self.url


class Member(SearchItem):
    pass

    def __str__(self):
        return self.url


class Admin(SearchItem):
    pass

    def __str__(self):
        return self.url


class ReferralLink(models.Model):
    order_id = models.CharField(max_length=10)
    date_generated = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)
    link_code = models.TextField()
    referral_pattern = models.CharField(max_length=255)
    user_id = models.PositiveIntegerField()
    user_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.referral_pattern

    def save(self, *args, **kwargs):
        try:
            user = User.objects.get(id=self.user_id)
            self.user_email = user.email
        except User.DoesNotExist:
            self.user_email = None
        super().save(*args, **kwargs)


class AdLink(models.Model):
    position = models.IntegerField(default=1)
    link = models.URLField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    members = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Position: {self.position}, Title: {self.title}, Link: {self.link}"
