import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Initialize Django
django.setup()

# Import the cache module
from django.core.cache import cache

# Clear the cache
cache.clear()
# Print success message
print("Cache cleared successfully!")