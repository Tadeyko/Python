import enum
from extensions import db
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

class EnumPostType(enum.Enum):
    news = 'news'
    publication = 'publication'
    other = 'other'

class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(1000))
    image = db.Column(db.String, default='postdefault.jpg')
    created = db.Column(db.DateTime, default=datetime.utcnow())
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    type = db.Column(db.Enum(EnumPostType), default=EnumPostType.other.value)
    post_tags = db.relationship('PostTag', backref='post', cascade='all, delete, delete-orphan')
    tags = association_proxy('post_tags', 'tag')

    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}')"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    posts = db.relationship('Post', backref='category')

class Tag(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    post_tags = db.relationship('PostTag', backref='tag', cascade='all, delete, delete-orphan')
    posts = association_proxy('post_tags', 'post')

class PostTag(db.Model, SerializerMixin):
    serialize_rules = ('-post', '-tag',)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)