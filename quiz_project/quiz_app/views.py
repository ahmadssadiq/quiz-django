from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Question, Answer, Quiz, QuizAttempt
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, QuizForm, QuestionFormSet, AnswerFormSet
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    quizzes = Quiz.objects.all()
    context = {
        "quizzes": quizzes,
        "user": request.user,  # Pass the user object to the template
    }
    return render(request, "index.html", context)


def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after sign-up
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "sign_up.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")  # Redirect to the index page
    else:
        form = AuthenticationForm()
    return render(request, "sign_in.html", {"form": form})


@login_required
def sign_out(request):
    logout(request)
    return redirect("sign_in")


@login_required
def create_quiz(request):
    if request.method == "POST":
        print(request.POST)  # Debugging: Print all POST data

        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            # Save the quiz
            quiz = quiz_form.save(commit=False)
            quiz.owner = request.user
            quiz.save()

            # Loop through the questions provided in the form
            question_index = 0
            while f"questions[{question_index}][text]" in request.POST:
                question_text = request.POST.get(f"questions[{question_index}][text]")
                print(f"Question: {question_text}")  # Debugging

                # Create a new question
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    question_type=request.POST.get(
                        f"questions[{question_index}][question_type]", "text"
                    ),
                    points=int(
                        request.POST.get(f"questions[{question_index}][points]", 0)
                    ),
                )

                # Loop through answers for the question
                answer_index = 0
                while (
                    f"questions[{question_index}][answers][{answer_index}][text]"
                    in request.POST
                ):
                    answer_text = request.POST.get(
                        f"questions[{question_index}][answers][{answer_index}][text]"
                    )
                    is_correct = (
                        request.POST.get(
                            f"questions[{question_index}][answers][{answer_index}][is_correct]",
                            "off",
                        )
                        == "on"
                    )
                    print(
                        f"Answer {answer_index}: {answer_text}, Is Correct: {is_correct}"
                    )  # Debugging

                    # Create the answer
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=is_correct,
                    )
                    answer_index += 1

                question_index += 1

            return redirect("index")  # Redirect to the homepage
    else:
        # Load an empty quiz form for GET requests
        quiz_form = QuizForm()
    return render(request, "create_quiz.html", {"quiz_form": quiz_form})


@login_required
def play_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Fetch the quiz
    questions = quiz.questions.all()  # Get all questions for the quiz

    context = {
        "quiz": quiz,
        "questions": questions,  # Pass all questions to the template
    }
    return render(request, "play_quiz.html", context)


def check_answer(request, question_id):
    question = Question.objects.get(id=question_id)
    selected_answer_id = request.POST.get("answer")
    selected_answer = Answer.objects.get(id=selected_answer_id)
    is_correct = selected_answer.is_correct
    return JsonResponse({"correccreatet": is_correct})


@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Get all questions for the quiz
    total_questions = questions.count()
    correct_answers = 0

    # Calculate the score based on user responses
    for question in questions:
        user_answer_id = request.POST.get(
            f"question_{question.id}"
        )  # Fetch user's answer for this question
        if user_answer_id:
            user_answer = Answer.objects.filter(id=user_answer_id).first()
            if user_answer and user_answer.is_correct:
                correct_answers += 1

    # Save the attempt
    QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=correct_answers,
        time_taken=0,  # Placeholder for future time tracking
    )

    # Redirect to results page
    return redirect(
        "quiz_results", quiz_id=quiz.id, score=correct_answers, total=total_questions
    )


@login_required
def quiz_results(request, quiz_id, score, total):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        "quiz": quiz,
        "score": score,
        "total": total,
    }
    return render(request, "quiz_results.html", context)
