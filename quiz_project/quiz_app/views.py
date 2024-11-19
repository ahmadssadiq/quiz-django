from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Question, Answer, Quiz
from django.contrib.auth.decorators import login_required

def index(request):
    quizzes = Quiz.objects.all()
    return render(request, 'index.html', {'quizzes': quizzes})


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    return render(request, 'sign_up.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'sign_in.html')


@login_required
def sign_out(request):
    logout(request)
    return redirect('sign_in')

@login_required
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        difficulty = request.POST['difficulty']
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            owner=request.user
        )
        return redirect('index')
    return render(request, 'create_quiz.html')

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