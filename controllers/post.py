import datetime

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# import custom modules
from config.db import db
from models.post import PostModel
from schemas import PostSchema, UpdatePostSchema, PlainCommentSchema

post_blueprint = Blueprint("post", __name__, description="Operation on posts")

@post_blueprint.route("/posts/")
class Post(MethodView):
    # get all posts
    @post_blueprint.response(200, PostSchema(many=True))
    def get(self):
        posts = PostModel.query.all()
        return posts

    # create new post
    @post_blueprint.arguments(PostSchema)
    @post_blueprint.response(201,PostSchema)
    def post(self, post_data):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        post = PostModel(**post_data, posted_date=date)
        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError as i:
            abort(400, message=str(i))
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return post

@post_blueprint.route("/post/<int:post_id>/")
class PostById(MethodView):
    # get specific post by id
    @post_blueprint.response(200,PostSchema)
    def get(self, post_id):
        post = PostModel.query.get_or_404(post_id)

        return post

    # update specific post by id
    @post_blueprint.arguments(UpdatePostSchema)
    @post_blueprint.response(201, PostSchema)
    def put(self, post_data, post_id):
        post = PostModel.query.get(post_id)
        updated_date = datetime.datetime.now().strftime("%Y-%m-%d")
        print(post)
        try:
            if post:
                post.title = post_data["title"] if "title" in post_data else post.title
                post.content = post_data["content"] if "content" in post_data else post.content
                post.updated_date = updated_date
            else:
                post = PostModel(id=post_id, **post_data, posted_date=updated_date)

            db.session.add(post)
            db.session.commit()
        except IntegrityError as i:
            abort(400, message=str(i))
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return post

    # delete specific post by it id
    @post_blueprint.response(200, PostSchema)
    def delete(self, post_id):
        post = PostModel.query.get_or_404(post_id)

        try:
            db.session.delete(post)
            db.session.commit()
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return {"message":"Post deleted successfully"}

@post_blueprint.route("/post/<int:post_id>/comments")
class CommentByPostId(MethodView):
    # get all posts
    @post_blueprint.response(200, PlainCommentSchema(many=True))
    def get(self, post_id):
        post = PostModel.query.get_or_404(post_id)
        return post.comments