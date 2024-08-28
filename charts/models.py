from django.db import models

# Create your models here.


class WordChart(models.Model):
    MONTH_CHOICES = [
        ('May-22', 'May-22'),
        ('Jun-22', 'Jun-22'),
        ('Jul-22', 'Jul-22'),
        ('Aug-22', 'Aug-22'),
        ('Sep-22', 'Sep-22'),
        ('Oct-22', 'Oct-22'),
        ('Nov-22', 'Nov-22'),
        ('Dec-22', 'Dec-22'),
        ('Jan-23', 'Jan-23'),
        ('Feb-23', 'Feb-23'),
        ('Mar-23', 'Mar-23'),
        ('Apr-23', 'Apr-23'),
    ]

    wordName = models.CharField(max_length=100)
    wordMention_May_22 = models.IntegerField(default=0)
    wordMention_Jun_22 = models.IntegerField(default=0)
    wordMention_Jul_22 = models.IntegerField(default=0)
    wordMention_Aug_22 = models.IntegerField(default=0)
    wordMention_Sep_22 = models.IntegerField(default=0)
    wordMention_Oct_22 = models.IntegerField(default=0)
    wordMention_Nov_22 = models.IntegerField(default=0)
    wordMention_Dec_22 = models.IntegerField(default=0)
    wordMention_Jan_23 = models.IntegerField(default=0)
    wordMention_Feb_23 = models.IntegerField(default=0)
    wordMention_Mar_23 = models.IntegerField(default=0)
    wordMention_Apr_23 = models.IntegerField(default=0)

    class Meta:
        app_label = 'charts'
