from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from collections import defaultdict
from django.contrib import messages

from users.decorators import quiz_master_required, quiz_taker_required

from .models import Question, Quiz, TakenQuiz, answered_question
from .forms import (PinForm)

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
        queryset = Quiz.objects.annotate(questions_count=Count(
            'questions')).filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, quiz_taker_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'quiz/quiztaker/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.quiztaker.taken_quizzes.order_by(
            '-date'
        )
        return queryset

# make a leaderboard for a particular quiz by taking primary key of quiz


@method_decorator([login_required, quiz_taker_required], name='dispatch')
class LeaderBoardView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'quiz/quiztaker/leaderboard.html'

    def get_context_data(self, **kwargs):
        name = TakenQuiz.objects.filter(
            quiz__pk=self.kwargs['pk'])[0].quiz.name
        kwargs['name'] = name
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = TakenQuiz.objects.filter(
            quiz__pk=self.kwargs['pk']).order_by('-score', 'date')[:10]
        return queryset

option_dict = {
    'option1': 'A',
    'option2': 'B',
    'option3': 'C',
    'option4': 'D',
}

def convert_multiple_correct(data):
    return ''.join([option_dict[key] for key in data])

quiz_permission_cache = defaultdict(set)

@login_required
@quiz_taker_required
def quiz_pin(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = PinForm(request.POST)
        pin = request.POST.get('pin')
        if pin == quiz.pin:
            quiz_permission_cache[request.user.pk].add(quiz.pk)
            return redirect('quiztaker:take_quiz', pk=pk)
        else:
            messages.warning(request, 'Wrong pin')
            return render(request, 'quiz/quiztaker/quiz_pin.html', {'quiz': quiz, 'form': form})
    else:
        form = PinForm()
        return render(request, 'quiz/quiztaker/quiz_pin.html', {'quiz': quiz, 'form': form})

@login_required
@quiz_taker_required
def take_quiz(request, pk):

    tf_dict = {
        'true': True,
        'false': False,
    }

    quiz = get_object_or_404(Quiz, pk=pk)
    quiztaker = request.user.quiztaker
    questions = [(question.TypedQuestion, question.type) for question in quiz.questions.all()]
    ques_dic = [{'ques': ques[0], 'num': i, 'type': ques[1]}
                for ques, i in zip(questions, [i + 1 for i in range(len(questions))])]

    if quiz.private and (request.user.pk not in quiz_permission_cache or quiz.pk not in quiz_permission_cache[request.user.pk]):
        return redirect('quiztaker:quiz_pin', pk=pk)
    
    if request.method == 'POST':
        score = 0

        for i, (q, type) in enumerate(questions):
            if type == 'multiplechoice':
                score += q.get_score(option_dict[request.POST.get(str(i + 1))])
            elif type == 'truefalse':
                score += q.get_score(tf_dict[request.POST.get(str(i + 1))])
            elif type == 'numerical':
                score += q.get_score(float(request.POST.get(str(i + 1))))
            else:
                score += q.get_score(convert_multiple_correct(request.POST.getlist(str(i + 1))))

        TakenQuiz.objects.create(quiz=quiz, taker=quiztaker, score=score)
        quiz_permission_cache[request.user.pk].remove(quiz.pk)
        return redirect('quiztaker:taken_quiz_list')
    else:
        context = {
            'questions': ques_dic
        }
        return render(request, 'quiz/quiztaker/take_quiz_form.html', context)
