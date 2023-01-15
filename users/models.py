from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_quiz_taker = models.BooleanField(default=False)
    is_quiz_master = models.BooleanField(default=False)

class QuizTaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField('quiz.Quiz', through='quiz.TakenQuiz', related_name='taken_by')

    def __str__(self):
        return self.user.email