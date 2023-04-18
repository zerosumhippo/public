from tkinter import *
from quiz_brain import QuizBrain


THEME_COLOR = "#375362"
WHITE = "#ffffff"
QUESTION_FONT = ("Arial", 15, "italic")


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.score_label = Label(text=f"Score: 0", font=("Arial", 15), bg=THEME_COLOR, fg=WHITE)
        self.score_label.grid(column=1, row=0)
        self.canvas = Canvas(width=300, height=250, bg=WHITE, highlightthickness=0)
        self.question_text = self.canvas.create_text(150, 125, text="Question Text", font=QUESTION_FONT,
                                                     fill=THEME_COLOR, width=280)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)
        true_img = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_img, highlightthickness=0, command=self.true_response)
        self.true_button.grid(row=2, column=0)
        false_img = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_img, highlightthickness=0, command=self.false_response)
        self.false_button.grid(row=2, column=1)
        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg=WHITE)
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_response(self):
        self.give_feedback(self.quiz.check_answer(user_answer="true"))

    def false_response(self):
        is_right = self.quiz.check_answer(user_answer="false")
        self.give_feedback(is_right)
    #     This does the exact same thing as what you see in true_response(), but it's a little more clear
    # that you are providing the answer "false" to the check_answer method in the quiz_brain and then
    # you are calling the give_feedback method from the UI and inserting the true/false returned by the
    # check_answer method in the quiz_brain.

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)
