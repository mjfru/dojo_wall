from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#! Home Page / Login
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/wall")
def show_wall():
    if 'user_id' in session:
        all_posts = Post.get_all_posts()
        return render_template("wall.html", all_posts = all_posts)
    else:
        return redirect("/")

#! Create 
@app.route("/create/user", methods = ["POST", "GET"])
def create_user():
    if request.method == "POST":
        if not User.validate(request.form):
            return redirect("/")
    pw_hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hashed
    }
    id = User.create_user(data)
    session['user_id'] = id
    session['name'] = request.form['first_name']
    return redirect("/wall")

#! Read
@app.route("/login", methods = ["POST"])
def login():
    data = {
        'email': request.form['email']
    }
    valid_user = User.get_user_by_email(data)
    if not valid_user:
        flash('Invalid email and/or password.', category='login')
        return redirect("/")
    if not bcrypt.check_password_hash(valid_user.password, request.form['password']):
    # if valid_user.password != request.form['password']:
        flash('Invalid email and/or password.', category='login')
        return redirect("/")
    session['user_id'] = valid_user.id
    session['name'] = valid_user.first_name
    return redirect("/wall")

#! Update
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")