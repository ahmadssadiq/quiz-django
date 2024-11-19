from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Quiz, Question, Answer
from django.forms import inlineformset_factory

# Custom user creation form for signing up users
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Custom authentication form for user login
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# Form for Quiz model
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'difficulty']

# Form for Question model
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'points']

# Form for Answer model
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

# Formset for Questions in a Quiz
QuestionFormSet = inlineformset_factory(
    Quiz, Question, 
    form=QuestionForm, 
    fields=('text', 'question_type', 'points'), 
    extra=1,  # Start with one empty question form
    can_delete=True
)

# Formset for Answers in a Question
AnswerFormSet = inlineformset_factory(
    Question, Answer, 
    form=AnswerForm, 
    fields=('text', 'is_correct'), 
    extra=2,  # Start with two empty answer forms
    can_delete=True
)