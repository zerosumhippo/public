import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_1 = ("Ariel", 40, "italic")
FONT_2 = ("Ariel", 60, "bold")
TARGET_WORDS = {}


def generate_word_pair():
    try:
        with open("data/words_to_learn.csv") as data_file:
            data = pandas.read_csv(data_file)
            data_list = data.to_dict(orient="records")
            target_pair = random.choice(data_list)
    except FileNotFoundError:
        with open("data/spanish_words.csv") as data_file:
            data = pandas.read_csv(data_file)
            data_list = data.to_dict(orient="records")
            target_pair = random.choice(data_list)
    finally:
        return target_pair


def learned_word():
    global TARGET_WORDS
    try:
        all_words = pandas.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        all_words = pandas.read_csv("data/spanish_words.csv")
    all_words_list = all_words.to_dict(orient="records")
    all_words_list.remove(TARGET_WORDS)
    updated_data = pandas.DataFrame(all_words_list)
    updated_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global TARGET_WORDS, flip_timer
    window.after_cancel(flip_timer)
    TARGET_WORDS = generate_word_pair()
    target_lang_word = TARGET_WORDS["Spanish"]
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=target_lang_word, fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(5000, flip_card)


def flip_card():
    control_lang_word = TARGET_WORDS["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=control_lang_word, fill="white")
    canvas.itemconfig(canvas_image, image=card_back_img)


window = Tk()
window.title("Language Flashcards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(5000, flip_card)

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=FONT_1)
card_word = canvas.create_text(400, 263, text="", font=FONT_2)

x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=next_card)
x_button.grid(column=0, row=1)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=learned_word)
check_button.grid(column=1, row=1)

next_card()

window.mainloop()
