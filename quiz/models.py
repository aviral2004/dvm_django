from django.db import models
from users.models import User, QuizTaker

# Create your models here.

class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    pin =  models.CharField(max_length=4, default=0)

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
    correct_score = models.FloatField(default=1.0)
    incorrect_score = models.FloatField(default=0.0)
    def __str__(self):
        return self.question_text

    @property
    def TypedQuestion(self):
        try:
            return self.multiplechoice
        except MultipleChoice.DoesNotExist:
            pass
        try:
            return self.truefalsequestion
        except TrueFalseQuestion.DoesNotExist:
            pass
        try:
            return self.numericalquestion
        except NumericalQuestion.DoesNotExist:
            pass
        try:
            return self.multiplecorrectquestion
        except MultipleCorrectQuestion.DoesNotExist:
            pass
    
    @property
    def type(self):
        try:
            self.multiplechoice
            return 'multiplechoice'
        except MultipleChoice.DoesNotExist:
            pass
        try:
            self.truefalsequestion
            return 'truefalse'
        except TrueFalseQuestion.DoesNotExist:
            pass
        try:
            self.numericalquestion
            return 'numerical'
        except NumericalQuestion.DoesNotExist:
            pass
        try:
            self.multiplecorrectquestion
            return 'multiplecorrect'
        except MultipleCorrectQuestion.DoesNotExist:
            pass

    def get_score(self, answer):
        if answer == self.TypedQuestion.answer:
            return self.correct_score
        else:
            return -1*self.incorrect_score

class NumericalQuestion(Question):
    answer = models.FloatField()

class TrueFalseQuestion(Question):
    answer = models.BooleanField()

class MultipleCorrectQuestion(Question):
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    
    CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('AB', 'A,B'),
        ('AC', 'A,C'),
        ('AD', 'A,D'),
        ('BC', 'B,C'),
        ('BD', 'B,D'),
        ('CD', 'C,D'),
        ('ABC', 'A,B,C'),
        ('ABD', 'A,B,D'),
        ('ACD', 'A,C,D'),
        ('BCD', 'B,C,D'),
        ('ABCD', 'A,B,C,D'),
    ]

    answer = models.CharField(max_length=200, choices=CHOICES, default='A')

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

    answer = models.CharField(max_length=200, choices=CHOICES, default='A')

class answered_question(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    taken_quiz = models.ForeignKey(TakenQuiz, on_delete=models.CASCADE)
    answer = models.CharField('Answer', max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer