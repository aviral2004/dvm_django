from django.contrib import admin

# Register your models here.
from quiz.models import Quiz, Question, answered_question, TakenQuiz
from users.models import User, QuizTaker
# register the models
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(answered_question)
admin.site.register(TakenQuiz)
admin.site.register(User)
admin.site.regiseter(QuizTaker)