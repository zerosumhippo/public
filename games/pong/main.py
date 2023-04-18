# Breakdown
# Classes:
# paddles
# # listen to keys
# ball
# # constant movement
# # detect collision with wall and bounce
# # detect collision with paddle
# # detect non-collision (score)
# scoreboard
# screen

from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time


screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Turtle Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(r_paddle.up, "Up")
screen.onkey(r_paddle.down, "Down")
screen.onkey(l_paddle.up, "q")
screen.onkey(l_paddle.down, "a")

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move_ball()
    if ball.ycor() > 285 or ball.ycor() < -285:
        # Detect collision with wall
        ball.bounce_y()
    # Detect collision with paddles
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()
    # Detect out of bounds
    if ball.xcor() == 400:
        scoreboard.l_point()
        ball.restart_ball()
    if ball.xcor() == -400:
        scoreboard.r_point()
        ball.restart_ball()

screen.exitonclick()
