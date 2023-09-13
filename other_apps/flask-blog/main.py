from flask import Flask, render_template
import requests


app = Flask(__name__)


JSON_BLOG_ENDPOINT = "https://api.npoint.io/5a0b315b05367f00e757"


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


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<post_id>')
def post(post_id):
    posts = pull_posts()
    return render_template("post.html", post_id=int(post_id), posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
