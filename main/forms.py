from django import forms
from django.contrib.auth.models import User

from .models import Answer
from .models import Question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_text',
        )
        labels = {
                'answer_text':'Answer',
        }
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_title',
                  'question_text',
        )
        labels = {
                'question_title':'Title',
                'question_text':'Text',
        }

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password',
				widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password',
				widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name')
		
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	
