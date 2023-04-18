from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_len=1, stretch_wid=5)
        self.color("white")
        self.goto(position)

    def up(self):
        self.sety(self.ycor() + 20)

    def down(self):
        self.sety(self.ycor() - 20)
