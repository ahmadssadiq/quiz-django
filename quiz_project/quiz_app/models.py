"""
Author: Ahmad Sadiq U37206345
File: models.py

description: this files define the database models for the Quiz application. These models represent
    the core entities and their relationships, including quizzes, questions, answers, 
    and user attempts. The models leverage Django's ORM to interact with the database,
    ensuring efficient data management and querying.

1. Quiz:
        - Represents a quiz created by a user.
        - Fields:
            - title: The title of the quiz.
            - description: A brief description of the quiz.
            - category: The category to which the quiz belongs (e.g., Science, Math).
            - difficulty: The difficulty level of the quiz (e.g., Easy, Medium, Hard).
            - owner: The user who created the quiz (ForeignKey to Django's User model).
            - created_at: The timestamp for when the quiz was created.
        - Relationships:
            - One-to-Many with the Question model.
2. Question:
        - Represents individual questions within a quiz.
        - Fields:
            - quiz: The quiz to which this question belongs (ForeignKey to Quiz).
            - text: The question text/content.
            - question_type: The type of question (e.g., Multiple Choice, True/False).
            - points: The number of points awarded for correctly answering the question.
        - Relationships:
            - One-to-Many with the Answer model.
3. Answer:
        - Represents possible answers to a specific question.
        - Fields:
            - question: The question to which this answer belongs (ForeignKey to Question).
            - text: The content of the answer.
            - is_correct: Boolean indicating whether this answer is correct.
        - Relationships:
            - Belongs to a single Question.
4. QuizAttempt:
        - Tracks individual user attempts at taking a quiz.
        - Fields:
            - user: The user who attempted the quiz (ForeignKey to Django's User model).
            - quiz: The quiz that was attempted (ForeignKey to Quiz).
            - score: The score achieved by the user for the attempt.
            - time_taken: The time (in seconds) the user took to complete the quiz.
            - completed_at: The timestamp for when the quiz attempt was completed.
        - Relationships:
            - Belongs to a single User and a single Quiz.

"""
from django.db import models
from django.contrib.auth.models import User
