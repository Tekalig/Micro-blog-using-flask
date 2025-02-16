from config.db import db

class CommentModel(db.Model):
    __tablename__="comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    commented_date = db.Column(db.Date, nullable=False)
    updated_date = db.Column(db.Date, nullable=True)
    posts = db.relationship("PostModel", back_populates="comments")