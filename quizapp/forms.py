from django import forms
from .models import Quiz, Choice

class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for question in quiz.question_set.all():
            question_id = f"question_{question.id}"
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            self.fields[question_id] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
                label=question.text,
            )
