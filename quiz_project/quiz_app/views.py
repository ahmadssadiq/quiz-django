from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Question, Answer, Quiz
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, QuizForm, QuestionFormSet, AnswerFormSet
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes,
        'user': request.user  # Pass the user object to the template
    }
    return render(request, 'index.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after sign-up
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})



def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the index page
    else:
        form = AuthenticationForm()
    return render(request, 'sign_in.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return redirect('sign_in')

@login_required
def create_quiz(request):
    if request.method == 'POST':
        # Initialize the quiz form with POST data
        quiz_form = QuizForm(request.POST)
        
        if quiz_form.is_valid():
            # Save the quiz instance but don't commit yet
            quiz = quiz_form.save(commit=False)
            quiz.owner = request.user  # Set the owner as the logged-in user
            quiz.save()

            # Loop through questions submitted in the form
            for index in range(len(request.POST.getlist('questions[0][text]'))):
                # Create a Question instance
                question = Question.objects.create(
                    quiz=quiz,
                    text=request.POST.get(f'questions[{index}][text]', ""),
                    question_type=request.POST.get(f'questions[{index}][question_type]', "text"),
                    points=request.POST.get(f'questions[{index}][points]', 0),
                )

                # Loop through answers for this question
                for answer_index in range(len(request.POST.getlist(f'questions[{index}][answers][0][text]'))):
                    Answer.objects.create(
                        question=question,
                        text=request.POST.get(f'questions[{index}][answers][{answer_index}][text]', ""),
                        is_correct=request.POST.get(f'questions[{index}][answers][{answer_index}][is_correct]', "off") == "on"
                    )

            # Redirect to the index page after successful creation
            return redirect('index')
        else:
            return render(request, 'create_quiz.html', {'quiz_form': quiz_form})

    else:
        # Initialize empty forms for GET requests
        quiz_form = QuizForm()
        return render(request, 'create_quiz.html', {'quiz_form': quiz_form})

@login_required
def play_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'play_quiz.html', context)


def check_answer(request, question_id):
    question = Question.objects.get(id=question_id)
    selected_answer_id = request.POST.get('answer')
    selected_answer = Answer.objects.get(id=selected_answer_id)
    is_correct = selected_answer.is_correct
    return JsonResponse({'correccreatet': is_correct})