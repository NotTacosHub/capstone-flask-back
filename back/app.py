from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os
import fbgraph

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(420), unique=True)
    title = db.Column(db.String(420), unique=True)
    author = db.Column(db.String(69), unique=False)
    published_date = db.Column(db.String(20), unique=False)
    content = db.Column(db.String(6969), unique=False)

    def __init__(self, slug, title, author, published_date, content):
        self.slug = slug
        self.title = title
        self.author = author
        self.published_date = published_date
        self.content = content


class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'slug', 'title', 'author', 'published_date', 'content')


blog_post_schema = BlogPostSchema()
blog_posts_schema = BlogPostSchema(many=True)


@app.route('/api/facebook/getposts')
@cross_origin()
def api_facebook_get_posts():
    return fbgraph.getposts()


@app.route('/api/facebook/getpostinfo/<postid>')
# @cross_origin()
def api_facebook_get_post_info(postid):
    return fbgraph.getpostinfo(postid)


@app.route('/api/blog/create', methods=["POST"])
# @cross_origin()
def api_blog_create():
    slug = request.json['slug']
    title = request.json['title']
    author = request.json['author']
    published_date = request.json['published_date']
    content = request.json['content']
    new_post = BlogPost(slug, title, author, published_date, content)

    db.session.add(new_post)
    db.session.commit()

    post = BlogPost.query.get(new_post.id)

    return blog_post_schema.jsonify(post)


@app.route('/api/blog/read', methods=["POST"])
# @cross_origin()
def api_blog_read():
    slug = request.json['slug']
    post = BlogPost.query.filter_by(slug=slug).one()
    return blog_post_schema.jsonify(post)


@app.route('/api/blog/getid', methods=["POST"])
# @cross_origin()
def api_blog_getid():
    slug = request.json['slug']
    post = BlogPost.query.filter_by(slug=slug).one()
    obj = {"id": post.id}
    return jsonify(obj)


@app.route('/api/blog/update', methods=["POST"])
# @cross_origin()
def update_blog_by_id():
    id = request.json['id']
    slug = request.json['slug']
    title = request.json['title']
    author = request.json['author']
    published_date = request.json['published_date']
    content = request.json['content']

    existing_post = BlogPost.query.get(id)
    existing_post.slug = slug
    existing_post.title = title
    existing_post.author = author
    existing_post.published_date = published_date
    existing_post.content = content

    db.session.commit()

    return blog_post_schema.jsonify(existing_post)


@app.route('/api/blog/delete', methods=["DELETE"])
# @cross_origin()
def api_blog_delete():
    slug = request.json['slug']
    post = BlogPost.query.filter_by(slug=slug).one()
    db.session.delete(post)
    db.session.commit()
    return "Post was deleted successfully"


@app.route('/api/blog/list', methods=["GET"])
def api_blog_list():
    posts = BlogPost.query.all()
    return blog_posts_schema.jsonify(posts)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8082)
