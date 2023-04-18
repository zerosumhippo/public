from turtle import Turtle

FONT = ("Courier", 24, "normal")
GAME_OVER_FONT = ("Courier", 24, "bold")
ALIGNMENT = "left"
GAME_OVER_ALIGNMENT = "center"


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("black")
        self.penup()
        self.hideturtle()
        self.level = 1

    def update_scoreboard(self, update_level):
        self.clear()
        self.goto(-290, 250)
        if update_level:
            self.level += 1
            self.write(f"Level: {self.level}", align=ALIGNMENT, font=FONT)
        if not update_level:
            self.write(f"Level: {self.level}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=GAME_OVER_ALIGNMENT, font=GAME_OVER_FONT)
