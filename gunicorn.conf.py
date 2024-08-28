# gunicorn.conf.py

# Number of Gunicorn worker processes
workers = 3

# Bind address (Unix socket or host:port)
bind = 'unix:/run/gunicorn.sock'

# Worker timeout
timeout = 7200  # Adjust as needed

