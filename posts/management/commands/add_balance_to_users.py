# myapp/management/commands/add_balance_to_users.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from posts.models import ApiUser
import schedule
import time

class Command(BaseCommand):
    help = 'Add balance to users'

    def handle(self, *args, **options):
        self.stdout.write("Scheduling add_balance_to_users task to run daily at 2 AM...")

        # Define the job to run your task
        def run_task():
            self.stdout.write("add_balance_to_users task started!")
            users = ApiUser.objects.all()
            for user in users:
                if user.user is not None:
                    if user.status != 'paid' and user.status != 'referral':
                        user.balance = 50
                else:
                    if user.status != 'paid' and user.status != 'referral':
                        user.balance = 50
                user.save()
            self.stdout.write("add_balance_to_users task completed")

        # Schedule the task to run daily at 2 AM
        schedule.every().day.at("02:00").do(run_task)
        
        # Keep the script running to execute scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(1)
