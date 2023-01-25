from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from .forms import QuizTakerSignUpForm, QuizMasterSignUpForm, GenericSignUp
from .models import User


# Create your views here.
def SignUp(request):
    return render(request, 'users/signup.html')

class QuizTakerSignUpView(CreateView):
    model = User
    form_class = QuizTakerSignUpForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Quiz Taker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('quiztaker:quiz_list')

class QuizMasterSignUpView(CreateView):
    model = User
    form_class = QuizMasterSignUpForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Quiz Master'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('quizmaster:quiz_change_list')

def google_register(request):
    if request.method == 'POST':
        form = GenericSignUp(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            login(request, user)
            return redirect('quiz-home')
    else:
        form = GenericSignUp()
    return render(request, 'users/google_register.html', {'form': form})