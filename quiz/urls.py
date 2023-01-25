from django.urls import path, include
from .views import home, QuizListView, TakenQuizListView, LeaderBoardView, take_quiz, quiz_pin
import quiz.quizmaster_views as quizmaster_views

urlpatterns = [
    path('', home, name='quiz-home'),

    path('quiztaker/', 
        include(
            ([
                path('', QuizListView.as_view(), name='quiz_list'),
                path('taken/', TakenQuizListView.as_view(), name='taken_quiz_list'),
                path('quiz/<int:pk>/', take_quiz, name='take_quiz'),
                path('leaderboard/<int:pk>/', LeaderBoardView.as_view(), name='leaderboard'),
                path('pin/<int:pk>', quiz_pin, name='quiz_pin'),

        ], 'quiz'), 
        namespace='quiztaker'),
    ),

    path('quizmaster/',
        include(
            ([
                path('', quizmaster_views.QuizListView.as_view(), name='quiz_change_list'),
                path('add/', quizmaster_views.QuizCreateView.as_view(), name='quiz_add'),
                path('<int:pk>/change/', quizmaster_views.QuizUpdateView.as_view(), name='quiz_change'),
                path('<int:pk>/delete/', quizmaster_views.QuizDeleteView.as_view(), name='quiz_delete'),
                path('<int:pk>/results/', quizmaster_views.QuizResultsView.as_view(), name='quiz_results'),
                path('<int:pk>/download/', quizmaster_views.export_quiz_results_to_excel, name='results_download'),
                path('<int:pk>/question/add-select/', quizmaster_views.question_select, name='question_select'),
                path('<int:pk>/question/add/', quizmaster_views.question_add, name='question_add'),
                path('<int:quiz_pk>/question/<int:question_pk>/', quizmaster_views.question_change, name='question_change'),
                path('<int:quiz_pk>/question/<int:question_pk>/delete/', quizmaster_views.QuestionDeleteView.as_view(), name='question_delete'),
            ], 'quiz'),
            namespace='quizmaster'),
    ),
]