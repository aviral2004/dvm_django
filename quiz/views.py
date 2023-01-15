from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from users.decorators import quiz_master_required, quiz_taker_required

from .models import Question, Quiz, TakenQuiz, answered_question

# from quiz.forms import TakeQuizForm

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_quiz_taker:
            return redirect('quiztaker:quiz_list')
        elif request.user.is_quiz_master:
            return redirect('quizmaster:quiz_change_list')
    else:
        return render(request, 'quiz/home.html')

@method_decorator([login_required, quiz_taker_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz/quiztaker/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.quiztaker
        # taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.annotate(questions_count=Count('questions')).filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, quiz_taker_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'quiz/quiztaker/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.quiztaker.taken_quizzes.order_by('quiz__name')
        return queryset

@login_required
@quiz_taker_required
def take_quiz(request, pk):
    option_dict = {
        'option1': 'A',
        'option2': 'B',
        'option3': 'C',
        'option4': 'D',
    }

    quiz = get_object_or_404(Quiz, pk=pk)
    quiztaker = request.user.quiztaker
    questions = quiz.questions.all()
    ques_dic = [{'ques': ques, 'num': i} for ques, i in zip(questions,[i + 1 for i in range(len(questions))])]
    if request.method == 'POST':
        score = 0

        for i, q in enumerate(questions):
            if q.multiplechoice.correct_option == option_dict[request.POST.get(str(i + 1))]:
                score+=1

        TakenQuiz.objects.create(quiz=quiz, taker=quiztaker, score=score)
        return redirect('quiztaker:quiz_list')
    else:
        context = {
            'questions':ques_dic
        }
        return render(request,'quiz/quiztaker/take_quiz_form.html',context)