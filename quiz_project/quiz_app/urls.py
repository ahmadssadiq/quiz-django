from django.urls import path
from .views import sign_up, sign_in, sign_out, create_quiz, play_quiz, check_answer, index

# Initialize urlpatterns as a list
urlpatterns = [
    path('', index, name='index'),  # Root view for the app
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='sign_out'),
    path('create_quiz/', create_quiz, name='create_quiz'),
    path('play_quiz/<int:quiz_id>/', play_quiz, name='play_quiz'),
    path('check_answer/<int:question_id>/', check_answer, name='check_answer'),
]