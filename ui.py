from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler by emiliomorles")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score Label
        self.score_label = Label(text="Score: 0", fg="white", bg=THEME_COLOR, font=("Arial", 10))
        self.score_label.grid(column=1, row=0, sticky=EW)

        # Canvas Label
        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Some Question Text",
            font=("Arial", 20, "italic"),
            fill=THEME_COLOR
        )
        #  150, 125 are the positions for the text. If I do not add them, this error will occur:
        #  IndexError: tuple index out of range
        self.canvas.grid(
            column=0,
            row=1,
            columnspan=2,
            sticky=EW,
            pady=50
        )  # columnspan=2 It expands 2 columns

        #  Correct Answer Label (RIGHT)
        right_img = PhotoImage(file="images/true.png")
        # I do not need to use the self. because I am not going to use it anywhere else
        self.right_button = Button(image=right_img, highlightthickness=0, command=self.true_pressed)
        self.right_button.grid(column=0, row=2)

        #  Incorrect Answer Label (LEFT)
        wrong_img = PhotoImage(file="images/false.png")
        # I do not need to use the self. because I am not going to use it anywhere else
        self.w_button = Button(image=wrong_img, highlightthickness=0, command=self.false_pressed)
        self.w_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")  # After 1 second or 1000 milliseconds it turns back to white color
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You have reached the end of the quiz.")
            # After all the questions the canvas show an ending text.
            self.right_button.config(state="disabled")
            self.w_button.config(state="disabled")

    def true_pressed(self): # -> bool:
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self): # -> bool:
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)
