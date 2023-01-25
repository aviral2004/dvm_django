from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from users.models import QuizTaker, User

class QuizTakerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    # transaction.atomic to make sure those three operations are done in a single database transaction and avoid data inconsistencies in case of error
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_quiz_taker = True
        user.save()
        quiz_taker = QuizTaker.objects.create(user=user)
        return user

class QuizMasterSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_quiz_master = True
        if commit:
            user.save()
        return user

class GenericSignUp(UserCreationForm):
    # add a dropdown field for selecting type of user
    user_type = forms.ChoiceField(choices=[('quiz_taker', 'Quiz Taker'), ('quiz_master', 'Quiz Master')], required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['user_type'] == 'quiz_taker':
            user.is_quiz_taker = True
            quiz_taker = QuizTaker.objects.create(user=user)
        elif self.cleaned_data['user_type'] == 'quiz_master':
            user.is_quiz_master = True
        if commit:
            user.save()
        return user