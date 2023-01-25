from .models import User, QuizTaker
from django.urls import reverse
from django.shortcuts import redirect


# TODO: fix this
class QuizUserRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.user.is_authenticated and not request.user.is_superuser:
            if request.user.is_quiz_taker == False and request.user.is_quiz_master == False:
                if request.path == reverse('googleregister'):
                    return None
                elif request.path == reverse('logout'):
                    return None
                return redirect('googleregister')
        return None