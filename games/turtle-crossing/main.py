import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

FINISH_LINE_Y = 280

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move_up,  "Up")
screen.onkey(player.move_down,  "Down")

num_game_loops = 0
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    num_game_loops += 1
    if num_game_loops % 6 == 0:
        car_manager.generate_cars()
    if player.ycor() + 10 == FINISH_LINE_Y:
        player.level_up()
        car_manager.move_cars(level_up=True)
        scoreboard.update_scoreboard(update_level=True)
    else:
        car_manager.move_cars(level_up=False)
        scoreboard.update_scoreboard(update_level=False)
    for car in car_manager.car_list:
        if player.distance(car) < 18:
            game_is_on = False
            scoreboard.game_over()
screen.exitonclick()
