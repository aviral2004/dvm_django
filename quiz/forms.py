from django import forms
from quiz.models import answered_question, Quiz, MultipleChoice


# class TakeQuizForm(forms.ModelForm):
#     # answer = forms.ModelChoiceField(
#     #     queryset=Answer.objects.none(),
#     #     widget=forms.RadioSelect(),
#     #     required=True,
#     #     empty_label=None)

#     def __init__(self, *args, **kwargs):
#         question = kwargs.pop('question')
#         super().__init__(*args, **kwargs)
#         self.fields['answer'].choices = question.answers.order_by('text')

#     answer = forms.ChoiceField(
#         widget=forms.RadioSelect,
#         required=True,
#         empty_label=None
#     )

#     class Meta:
#         model = answered_question
#         fields = ('answer', )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoice
        fields = ('question_text', 'optionA', 'optionB', 'optionC', 'optionD', 'correct_option')
