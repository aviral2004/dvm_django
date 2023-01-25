import xlwt
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from quiz.forms import (MultipleChoiceQuestionForm,
                        MultipleCorrectQuestionForm, NumericalQuestionForm,
                        QuestionSelectForm, TrueFalseQuestionForm)
from quiz.models import (MultipleChoice, MultipleCorrectQuestion,
                         NumericalQuestion, Question, Quiz, TrueFalseQuestion)
from users.decorators import quiz_master_required


@method_decorator([login_required, quiz_master_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz/quizmaster/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .annotate(questions_count=Count('questions', distinct=True), taken_count=Count('taken_quizzes', distinct=True))
        return queryset


@method_decorator([login_required, quiz_master_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'private', 'pin')
    template_name = 'quiz/quizmaster/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('quizmaster:quiz_change', quiz.pk)


@method_decorator([login_required, quiz_master_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'private', 'pin')
    context_object_name = 'quiz'
    template_name = 'quiz/quizmaster/quiz_change_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.all()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('quizmaster:quiz_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, quiz_master_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/quizmaster/quiz_delete_confirm.html'
    success_url = reverse_lazy('quizmaster:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

# create a function that returns an excel file with the results of the quiz
def export_quiz_results_to_excel(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{quiz.name}_quiz_results.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(quiz.name)

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Taker', 'Score', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # convert datetime object to string
    def convert_datetime_to_string(date):
        return date.strftime('%Y-%m-%d %H:%M:%S')

    xlwt.easyxf(num_format_str='YYYY-MM-DD HH:MM:SS')
    rows = quiz.taken_quizzes.select_related('taker__user').values_list('taker__user__username', 'score', 'date')
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 2:
                date = convert_datetime_to_string(row[col_num])
                ws.write(row_num, col_num, date, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@method_decorator([login_required, quiz_master_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/quizmaster/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('taker__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


def question_select(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionSelectForm(request.POST)
        question_type = form.data['question_type']
        request.session['question_type'] = question_type
        return redirect('quizmaster:question_add', pk)
    else:
        form = QuestionSelectForm()
        return render(request, 'quiz/quizmaster/question_select.html', {'form': form, 'quiz': quiz})

def get_question_form(question_type):
    if question_type == 'numerical':
        QuestionForm = NumericalQuestionForm
    elif question_type == 'multiplecorrect':
        QuestionForm = MultipleCorrectQuestionForm
    elif question_type == 'truefalse':
        QuestionForm = TrueFalseQuestionForm
    else:
        QuestionForm = MultipleChoiceQuestionForm
    return QuestionForm

@login_required
@quiz_master_required
def question_add(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)
    # get the question type from the url query string
    question_type = request.session.get('question_type')
    QuestionForm = get_question_form(question_type)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quizmaster:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'quiz/quizmaster/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@quiz_master_required
def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question_object = get_object_or_404(Question, pk=question_pk)
    question, type = question_object.TypedQuestion, question_object.type
    QuestionForm = get_question_form(type)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect('quizmaster:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'quiz/quizmaster/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
    })


@method_decorator([login_required, quiz_master_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'quiz/quizmaster/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('quizmaster:quiz_change', kwargs={'pk': question.quiz_id})
