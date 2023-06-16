from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash
import datetime #!

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']

#! Create
    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        result = connectToMySQL('dojo_wall').query_db(query, data)
        return result
    
#! Read
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;;"
        #! STUDY
        #? FROM the table you're in, JOIN the table you want to connect to, ON the current table's foreign key EQUALS the other table's primary key
        #! STUDY
        results = connectToMySQL('dojo_wall').query_db(query)
        print(results)
        all_posts = []
        for result in results:
            poster = User({
                "id": result['user_id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": result['password'],
                "created_at": result['users.created_at'], #? Needed to refer to users specifically since they both share a created_at
                "updated_at": result['users.updated_at']
            })
            created_at = datetime.datetime.strptime(str(result['created_at']), "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y, %H:%M")

            one_post = Post({
                "id": result["id"],
                "content": result['content'],
                "created_at": created_at, #result['created_at'],
                "updated_at": result['updated_at'],
                "user": poster
            })
            all_posts.append(one_post)
            # print("@@@@@@@@@@@@@@@@@@@@", all_posts)
        return all_posts

#! Delete
    @classmethod
    def delete_post(cls, post_id):
        query = "DELETE FROM posts WHERE id = %(post_id)s;"
        data = {
            "post_id": post_id
        }
        return connectToMySQL('dojo_wall').query_db(query, data)
    
#! Validation
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 1:
            flash("Surely you can type just one letter to post...", category = 'post_content')
            is_valid = False
        return is_valid