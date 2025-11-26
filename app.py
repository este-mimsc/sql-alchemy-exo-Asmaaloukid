"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

# These extension instances are shared across the app and models
# so that SQLAlchemy can bind to the application context when the
# factory runs.
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Application factory used by Flask and the tests.

    The optional ``test_config`` dictionary can override settings such as
    the database URL to keep student tests isolated.
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here so SQLAlchemy is aware of them before migrations
    # or ``create_all`` run. Students will flesh these out in ``models.py``.
    from models import User,Post  # noqa: F401

    @app.route("/")
    def index():
        """Simple sanity check route."""

        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    @app.route("/users", methods=["GET", "POST"])
    def users():
        if request.method=="GET":
            users=User.query.all()
            users_js = []
            for user in users:
                 users_js.append({
                    "id": user.id,
                    "username": user.username,
            })
            
            return jsonify(users_js)
        
        elif request.method == "POST":
             user_data = request.get_json()
             new_user = User(username=user_data["username"])
             db.session.add(new_user)
             db.session.commit()
             return jsonify({"id": new_user.id, "username": new_user.username})

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        if request.method=="GET":
            posts=Post.query.all()
            posts_js = []
            for post in posts:
                 posts_js.append({
                     "id": post.id,
                     "title":post.title,
                     "content":post.content,
                     "user_id":post.user_id
            })
            return jsonify(posts_js)
        elif request.method == "POST":
            post_data = request.get_json()
            new_post = Post(
                title=post_data["title"],
                content=post_data["content"],
                user_id=post_data["user_id"]
            )
            db.session.add(new_post)
            db.session.commit()
            return jsonify({
                "id": new_post.id,
                "title": new_post.title,
                "content": new_post.content,
                "user_id": new_post.user_id
            })

    return app


# Expose a module-level application for convenience with certain tools
app = create_app()


if __name__ == "__main__":
    # Running ``python app.py`` starts the development server.
    app.run(debug=True)
