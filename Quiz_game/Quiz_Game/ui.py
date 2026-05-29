import customtkinter as ctk
from quiz_brain import QuizBrain
from tkinter import messagebox
import random
from quiz_data import fetch_quiz_data  # keep the function import

class QuizInterface:
    def __init__(self, quiz: QuizBrain):
        self.quiz = quiz
        self.timer_seconds = 10
        self.timer_id = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Quiz Game ")
        self.window.geometry("600x520")

        # Score label
        self.score_label = ctk.CTkLabel(master=self.window, text=f"Score: {self.quiz.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

        # Timer label
        self.timer_label = ctk.CTkLabel(master=self.window, text=f"Time Left: {self.timer_seconds}s", font=("Arial", 16, "bold"), text_color="#FFB86C")
        self.timer_label.pack(pady=5)

        # Question Frame
        self.question_frame = ctk.CTkFrame(master=self.window, width=500, height=200, corner_radius=10)
        self.question_frame.pack(pady=15)
        self.question_label = ctk.CTkLabel(master=self.question_frame, text="", wraplength=450, justify="center", font=("Arial", 18))
        self.question_label.pack(pady=20)

        # Option Buttons
        self.option_buttons = []
        for _ in range(4):
            btn = ctk.CTkButton(master=self.window, text="", width=400, command=lambda b=_: self.check_answer(b))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        # Restart Button
        self.restart_btn = ctk.CTkButton(master=self.window, text="🔄 Restart Quiz", command=self.restart_quiz)
        self.restart_btn.pack(pady=20)

        self.get_next_question()
        self.window.mainloop()

    def start_timer(self):
        self.timer_label.configure(text=f"Time Left: {self.timer_seconds}s")
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.window.after(1000, self.start_timer)
        else:
            self.time_up()

    def reset_timer(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
        self.timer_seconds = 10
        self.start_timer()

    def time_up(self):
        for btn in self.option_buttons:
            btn.configure(state="disabled", fg_color="#44475A")
        self.timer_label.configure(text="⏰ Time’s up!", text_color="#FF5555")
        self.window.after(1200, self.get_next_question)

    def get_next_question(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        if self.quiz.still_has_questions():
            q = self.quiz.next_question()
            self.question_label.configure(text=q["question"])
            for i, opt in enumerate(q["options"]):
                self.option_buttons[i].configure(text=opt, state="normal", fg_color="#1F6AA5")
            self.reset_timer()
        else:
            messagebox.showinfo("Quiz Completed", f"🎉 Final Score: {self.quiz.score}/{len(self.quiz.questions)}")
            for btn in self.option_buttons:
                btn.configure(state="disabled")
            self.question_label.configure(text="Thanks for playing!")
            self.timer_label.configure(text="Game Over", text_color="#8BE9FD")

    def check_answer(self, idx):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        user_answer = self.option_buttons[idx].cget("text")
        correct = self.quiz.check_answer(user_answer)

        if correct:
            self.option_buttons[idx].configure(fg_color="green")
        else:
            self.option_buttons[idx].configure(fg_color="red")

        self.score_label.configure(text=f"Score: {self.quiz.score}")
        self.window.after(800, self.get_next_question)

    def restart_quiz(self):
        """Fetch new dynamic quiz data and restart."""
        new_quiz_data = fetch_quiz_data(amount=10)  # fetch fresh questions
        random.shuffle(new_quiz_data)
        self.quiz = QuizBrain(new_quiz_data)
        self.score_label.configure(text="Score: 0")
        self.get_next_question()

