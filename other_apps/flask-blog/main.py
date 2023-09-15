from flask import Flask, render_template, request
import requests
import os
import smtplib


app = Flask(__name__)

JSON_BLOG_ENDPOINT = "https://api.npoint.io/5a0b315b05367f00e757"
CONTACT_ME_EMAIL = os.environ.get("CONTACT_ME_EMAIL")
CONTACT_ME_EMAIL_PW = os.environ.get("CONTACT_ME_EMAIL_PW")


def pull_posts():
    blog_text_response = requests.get(JSON_BLOG_ENDPOINT)
    blog_text_response.raise_for_status()
    posts = blog_text_response.json()
    return posts


@app.route('/')
def home():
    posts = pull_posts()
    return render_template("index.html", blog_posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        h1_message = "Contact Me"
        return render_template("contact.html", h1_message=h1_message)
    elif request.method == 'POST':
        h1_message = "Your message has been sent!"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=CONTACT_ME_EMAIL, password=CONTACT_ME_EMAIL_PW)
            connection.sendmail(
                from_addr=CONTACT_ME_EMAIL,
                to_addrs=CONTACT_ME_EMAIL,
                msg=f"Subject:Blog | Contact Me\n\n"
                    f"Name: {request.form['name']}\n"
                    f"Email: {request.form['email']}\n"
                    f"Phone Number: {request.form['phone']}\n"
                    f"Message: {request.form['message']}"
            )
        return render_template("contact.html", h1_message=h1_message)


@app.route('/post/<post_id>')
def post(post_id):
    posts = pull_posts()
    return render_template("post.html", post_id=int(post_id), posts=posts)


if __name__ == "__main__":
    app.run()
