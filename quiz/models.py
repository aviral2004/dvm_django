from django.db import models
from users.models import User, QuizTaker

# Create your models here.

class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TakenQuiz(models.Model):
    taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    def __str__(self):
        return self.question_text

class MultipleChoice(Question):
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    
    CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    correct_option = models.CharField(max_length=200, choices=CHOICES, default='A')

class answered_question(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    taken_quiz = models.ForeignKey(TakenQuiz, on_delete=models.CASCADE)
    answer = models.CharField('Answer', max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer