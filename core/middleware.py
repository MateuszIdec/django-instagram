from django.contrib.auth import login, get_user_model

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            User = get_user_model()
            user = User.objects.get(username="testUser")
            login(request, user)

        return self.get_response(request)