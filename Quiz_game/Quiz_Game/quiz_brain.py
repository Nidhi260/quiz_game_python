class QuizBrain:
    def __init__(self, questions):
        self.question_number = 0
        self.score = 0
        self.questions = questions

    def still_has_questions(self):
        return self.question_number < len(self.questions)

    def next_question(self):
        current_q = self.questions[self.question_number]
        self.question_number += 1
        return current_q

    def check_answer(self, user_answer):
        correct_answer = self.questions[self.question_number - 1]["answer"]
        if user_answer == correct_answer:
            self.score += 1
            return True
        return False
