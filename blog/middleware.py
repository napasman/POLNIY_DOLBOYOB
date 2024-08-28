from django.http import HttpResponseRedirect

class RestrictToSuperuserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude the password change view from the superuser check
        if request.path.startswith("/skote/accounts/password/change/"):
            return self.get_response(request)

        # Check for superuser access for other views
        if request.path.startswith("/skote/") and not request.user.is_superuser:
            # Redirect to the home page
            return HttpResponseRedirect('/')
        
        return self.get_response(request)
