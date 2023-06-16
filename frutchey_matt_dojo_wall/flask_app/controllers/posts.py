from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models.post import Post

#! Create
@app.route("/new/post", methods=["POST"])
def user_post():
    if request.method == 'POST':
        if not Post.validate_post(request.form):
            return redirect("/wall")
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    print(data)
    # Validation goes here later (or in the model)
    Post.create_post(data)
    return redirect("/wall")

#! Delete
@app.route("/delete/post/<int:post_id>")
def delete_post(post_id):
    Post.delete_post(post_id)
    return redirect("/wall")