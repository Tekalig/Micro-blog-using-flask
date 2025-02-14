from config.db import db

class PostModel(db.Model):
    __tablename__="posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    posted_date = db.Column(db.Date, nullable=False)
    updated_date = db.Column(db.Date, nullable=True)
    comments = db.relationship("CommentModel", back_populates="posts", lazy="dynamic")