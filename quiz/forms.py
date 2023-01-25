from django import forms
from quiz.models import answered_question, Quiz, MultipleChoice, NumericalQuestion, TrueFalseQuestion, MultipleCorrectQuestion


# create a basic form to select type of question from dropdown
class QuestionSelectForm(forms.Form):
    question_type = forms.ChoiceField(
        choices = (
            ('numerical', 'Numerical'),
            ('truefalse', 'True/False'),
            ('multiplecorrect', 'Multiple Correct'),
            ('multiplechoice', 'Multiple Choice'),
        ),
        required = True,
    )


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoice
        fields = ('question_text', 'correct_score', 'incorrect_score', 'optionA', 'optionB', 'optionC', 'optionD', 'answer')
        labels = {
            'correct_score': 'Points for correct answer',
            'incorrect_score': 'Penalty for incorrect answer',
        }

# make form for numerical question
class NumericalQuestionForm(forms.ModelForm):
    class Meta:
        model = NumericalQuestion
        fields = ('question_text', 'correct_score', 'incorrect_score', 'answer')
        labels = {
            'correct_score': 'Points for correct answer',
            'incorrect_score': 'Penalty for incorrect answer',
        }

# make form for true/false question
class TrueFalseQuestionForm(forms.ModelForm):
    # make a dropdown selecting true or false for answer field
    answer = forms.ChoiceField(
        choices = (
            ('True', 'True'),
            ('False', 'False'),
        ),
        required = True,
    )
    class Meta:
        model = TrueFalseQuestion
        fields = ('question_text', 'correct_score', 'incorrect_score', 'answer')
        labels = {
            'correct_score': 'Points for correct answer',
            'incorrect_score': 'Penalty for incorrect answer',
        }

# make form for multiple correct question
class MultipleCorrectQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleCorrectQuestion
        fields = ('question_text', 'correct_score', 'incorrect_score', 'optionA', 'optionB', 'optionC', 'optionD', 'answer')
        labels = {
            'correct_score': 'Points for correct answer',
            'incorrect_score': 'Penalty for incorrect answer',
        }

# make for for entering pin
class PinForm(forms.Form):
    pin = forms.CharField(max_length=4, required=True)