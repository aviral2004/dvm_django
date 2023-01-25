from django.urls import path, include
from .views import QuizTakerSignUpView, QuizMasterSignUpView, SignUp, google_register
from django.contrib.auth import views as auth_views
# create a django url pattern for all the urls in the users app
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', SignUp, name='signup-select'),
    path('signup/quiztaker', QuizTakerSignUpView.as_view(), name='quiztaker-signup'),
    path('signup/quizmaster', QuizMasterSignUpView.as_view(), name='quizmaster-signup'),
    path('googleregister', google_register, name='googleregister'),
]