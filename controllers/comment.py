import datetime

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# import custom modules
from config.db import db
from models.comment import CommentModel
# from schemas import PlainCommentSchema, UpdateCommentSchema

comment_blueprint = Blueprint("comment", __name__, description="Operation on comments")

@comment_blueprint.route("/comment/")
class NewCommentLists(MethodView):
    #
    def get(self):
        return CommentModel.query.all()

    #
    def comment(self, comment_data):
        commented_date = datetime.datetime.now().strftime("%Y-%m-%d")
        comment = CommentModel(**comment_data, commented_date=commented_date)

        try:
            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return comment

@comment_blueprint.route("/comment/<int:comment_id>/")
class CommentById(MethodView):
    #
    def get(self, comment_id):
        comment = CommentModel.query.get_or_404(comment_id)

        return comment

    #
    def put(self, comment_data, comment_id):
        comment = CommentModel.query.get()
        updated_date = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            if comment:
                comment.comment = comment_data["comment"] if "comment" in comment_data else comment.comment
                comment.updated_date = updated_date
            else:
                comment = CommentModel(id=comment_id, **comment_data, commented_date=updated_date)

            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return comment

    #
    def delete(self, comment_id):
        comment = CommentModel.query.get_or_404(comment_id)

        try:
            db.session.delete(comment)
            db.session.commit()
        except SQLAlchemyError as s:
            abort(500, message=str(s))

        return {"message":"Comment deleted successfully"}