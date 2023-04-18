from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Brush Script MT", 20, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        with open("data.txt") as high_score_file:
            self.high_score = high_score_file.read()
        self.score = 0
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, 270)
        self.write(arg=f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def update_score(self):
        self.clear()
        self.score += 1
        if self.score > int(self.high_score):
            with open("data.txt", mode="w") as file:
                file.write(str(self.score))
        with open("data.txt") as high_score_file:
            self.high_score = high_score_file.read()
        self.write(arg=f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write(arg="GAME OVER", align=ALIGNMENT, font=FONT)
