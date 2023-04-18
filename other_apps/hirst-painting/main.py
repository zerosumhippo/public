# import colorgram
#
# colors = colorgram.extract('hirst_dots.jpg', 20)
# rgb_colors = []
#
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r, g, b)
#     rgb_colors.append(new_color)
# print(rgb_colors)

# painting with 10 x 10 rows of spots
# dots 20 in size
# spaced apart by 50 paces

from turtle import Turtle, Screen
import turtle
import random

turtle.colormode(255)
color_list = [(132, 166, 204), (220, 148, 108), (197, 135, 148), (32, 41, 61), (163, 59, 49), (41, 106, 155),
              (141, 183, 162), (237, 211, 92), (148, 61, 68), (214, 83, 72), (35, 61, 56), (52, 111, 91),
              (170, 29, 33), (158, 33, 30), (234, 167, 158), (17, 97, 71)]
hirst = Turtle()
hirst.speed(0)
hirst.hideturtle()


def row_beginning():
    hirst.penup()
    hirst.setx(-200)


def draw_circle_row():
    for _ in range(10):
        selected_color = random.choice(color_list)
        hirst.color(selected_color)
        hirst.pendown()
        hirst.dot(20, selected_color)
        hirst.penup()
        hirst.fd(50)


def move_up():
    hirst.penup()
    hirst.sety(hirst.ycor() + 50)


def get_your_paint_on():
    hirst.penup()
    hirst.sety(-200)
    for _ in range(10):
        row_beginning()
        draw_circle_row()
        move_up()

get_your_paint_on()
screen = Screen()
screen.exitonclick()
