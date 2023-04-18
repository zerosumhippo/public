from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 5  # How much faster the cars should go after each level up.


class CarManager:

    def __init__(self):
        self.car_list = []
        self.generate_cars()
        self.current_speed = STARTING_MOVE_DISTANCE

    def generate_cars(self):
        car = Turtle("square")
        car.color(random.choice(COLORS))
        car.shapesize(stretch_len=2, stretch_wid=1)
        car.penup()
        car.setheading(180)
        car.goto(300, random.randint(-250, 250))
        self.car_list.append(car)

    def move_cars(self, level_up):
        if not level_up:
            for car_object in self.car_list:
                car_object.forward(self.current_speed)
        if level_up:
            self.current_speed += MOVE_INCREMENT
            for car_object in self.car_list:
                car_object.forward(self.current_speed)





# Create cars that are 20px high by 40px wide that are randomly generated along the y-axis and move
# to the left edge of the screen. No cars should be generated in the top and bottom 50px of the screen
# (think of it as a safe zone for our little turtle). Hint: generate a new car only every 6th time the game loop runs.
# If you get stuck, check the video walkthrough in Step 4.