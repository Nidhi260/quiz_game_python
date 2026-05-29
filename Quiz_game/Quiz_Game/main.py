from quiz_data import fetch_quiz_data
from ui import QuizInterface
from quiz_brain import QuizBrain

quiz_data = fetch_quiz_data(amount=10, difficulty="medium")

quiz = QuizBrain(quiz_data)
quiz_ui = QuizInterface(quiz)

