from flask import Flask
import random

app = Flask(__name__)
NUMBER_TO_GUESS = random.randint(0, 9)
COLOR_LIST = ["red", "blue", "green", "yellow", "orange", "purple"]


@app.route("/")
def home_page():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media1.giphy.com/media/4JVTF9zR9BicshFAb7/200.webp?cid" \
           "=ecf05e470fomnf641kinaln47o4tdc07rsa0y430eeq648i2&ep=v1_gifs_search&rid=200.webp&ct=g'> "


@app.route("/<int:number>")
def number_page(number):
    header_color = random.choice(COLOR_LIST)
    if number == NUMBER_TO_GUESS:
        return f"<h1 style='color:{header_color}'>You guessed it!</h1>" \
               "<img src= 'https://media1.giphy.com/media/5DQdk5oZzNgGc/200.webp?cid" \
               "=ecf05e47ep04gsazy29go0ov64xx0waawmyzjf52vv85if9d&ep=v1_gifs_search&rid=200.webp&ct=g'> "
    elif number < NUMBER_TO_GUESS:
        return f"<h1 style='color:{header_color}'>{number} is too low. Try again.</h1>" \
               "<img src= 'https://media0.giphy.com/media/4UJyRK2TXNhgk/200.webp?cid" \
               "=ecf05e47ep04gsazy29go0ov64xx0waawmyzjf52vv85if9d&ep=v1_gifs_search&rid=200.webp&ct=g'> "
    else:
        return f"<h1 style='color:{header_color}'>{number} is too high. Try again.</h1>" \
               "<img src= 'https://media2.giphy.com/media/l396BoOTIFem9xqQU/200w.webp?cid" \
               "=ecf05e47ep04gsazy29go0ov64xx0waawmyzjf52vv85if9d&ep=v1_gifs_search&rid=200w.webp&ct=g'> "


if __name__ == "__main__":
    app.run()
