from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['CKEDITOR_PKG_TYPE'] = 'full'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


class AddBlogPostForm(FlaskForm):
    blog_post_title = StringField("Blog Post Title", validators=[DataRequired()])
    blog_post_subtitle = StringField("Subtitle", validators=[DataRequired()])
    blog_post_author = StringField("Author Name", validators=[DataRequired()])
    blog_post_image_url = URLField("Blog Image URL", validators=[URL()])
    blog_post_content = CKEditorField("Blog Content", validators=[DataRequired()])
    blog_post_submit = SubmitField(label="Submit Post")


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>', methods=["GET"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods=["GET", "POST"])
def add_new_post():
    form = AddBlogPostForm()
    post_added = False
    if form.validate_on_submit() and request.method == "POST":
        new_post = BlogPost(title=request.form["blog_post_title"],
                            subtitle=request.form["blog_post_subtitle"],
                            date=date.today().strftime('%B %d, %Y'),
                            body=request.form.get("blog_post_content"),
                            author=request.form["blog_post_author"],
                            img_url=request.form["blog_post_image_url"])
        db.session.add(new_post)
        db.session.commit()
        post_added = True
    return render_template("make-post.html", form=form, confirm=post_added)


@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    edit_form = AddBlogPostForm(
        blog_post_title=requested_post.title,
        blog_post_subtitle=requested_post.subtitle,
        blog_post_image_url=requested_post.img_url,
        blog_post_author=requested_post.author,
        blog_post_content=requested_post.body
    )
    if edit_form.validate_on_submit() and request.method == "POST":
        requested_post.title = request.form["blog_post_title"]
        requested_post.subtitle = request.form["blog_post_subtitle"]
        requested_post.img_url = request.form["blog_post_image_url"]
        requested_post.author = request.form["blog_post_author"]
        requested_post.body = request.form["blog_post_content"]
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("make-post.html", form=edit_form, post=requested_post, is_edit=True)


@app.route('/delete-post/<int:post_id>', methods=["GET", "POST"])
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
