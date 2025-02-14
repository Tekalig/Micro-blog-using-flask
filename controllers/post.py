from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# import custom modules
from config.db import db
from models.post import PostModel
from schemas import PlainPostSchema, UpdatePostSchema

post_blueprint = Blueprint("post", __name__, description="Operation on posts")

@post_blueprint.route("/posts/")
class Post(MethodView):
    # get all posts
    @post_blueprint.response(200, PlainPostSchema(many=True))
    def get(self):
        posts = PostModel.query.all()
        return posts

    # create new post
    @post_blueprint.arguments(PlainPostSchema)
    @post_blueprint.response(201,PlainPostSchema)
    def post(self, post_data):
        post = PostModel(**post_data)
        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError as i:
            abort(400, message=str(i))
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return post

@post_blueprint.route("/post/<int:post_id")
class PostById(MethodView):
    # get specific post by id
    @post_blueprint.response(200,PlainPostSchema)
    def get(self, post_id):
        post = PostModel.query.get_or_404(post_id)

        return post

    # update specific post by id
    @post_blueprint.arguments(UpdatePostSchema)
    @post_blueprint.response(201, PlainPostSchema)
    def put(self, post_data, post_id):
        post = PostModel.query.get_or_404(post_id)
        post |= post_data
        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError as i:
            abort(400, message=str(i))
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return post

    # delete specific post by it id
    @post_blueprint.response(200, PlainPostSchema)
    def delete(self, post_id):
        post = PostModel.query.get_or_404(post_id)

        try:
            db.session.delete()
            db.session.commit()
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return {"message":"Post deleted successfully"}