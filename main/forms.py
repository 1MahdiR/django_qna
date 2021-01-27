from django import forms

from .models import Answer
from .models import Question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_username',
                  'answer_text',
        )
        labels = {
                'answer_username':'Name',
                'answer_text':'Answer',
        }
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_username',
                  'question_title',
                  'question_text',
        )
        labels = {
                'question_username':'Name',
                'question_title':'Title',
                'question_text':'Text',
        }

