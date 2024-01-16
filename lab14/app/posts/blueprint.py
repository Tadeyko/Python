from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from .forms import PostForm, CategoryForm
from .models import Post, Category
import secrets
import os
from flask_login import current_user

postsBp = Blueprint('posts', __name__, template_folder="templates/posts", static_folder="static")

per_page = 5

@postsBp.route('/', methods=['GET'])
def posts():
    current_page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.created.desc()).paginate(page=current_page, per_page=per_page)
    post_list = pagination.items
    return render_template("posts.html", post_list=post_list, pagination=pagination)

@postsBp.route('/<int:id>', methods=['GET'])
def post(id):
    post = db.session.query(Post).filter(Post.id == id).first()
    return render_template("post.html", post=post)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(posts.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@postsBp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    categories_list = db.session.query(Category).all()
    form.category.choices = [(category.id, category.name) for category in categories_list]

    if form.validate_on_submit():
        file_url=None
        if form.image.data:
            file_url = save_picture(form.image.data)

        newPost = Post(
            title=form.title.data, 
            text=form.text.data, 
            image=file_url, 
            enabled=form.enabled.data, 
            user_id=current_user.get_id(), 
            category_id=form.category.data
        )
        db.session.add(newPost)
        db.session.commit()

        return redirect(url_for('posts.posts'))

    return render_template("create_post.html", form=form, categories=categories_list)

@postsBp.route("/<int:id>/delete")
def delete_post(id):
    deleted_post = db.session.query(Post).filter(Post.id == id).first()
    db.session.delete(deleted_post)
    db.session.commit()
    return redirect(url_for("posts.posts"))

@postsBp.route('/<int:id>/update', methods=["POST", "GET"])
def update_post(id):
    form = PostForm()
    updated_post = db.session.query(Post).filter(Post.id == id).first()
    categories_list = db.session.query(Category).all()
    form.category.choices = [(category.id, category.name) for category in categories_list]

    if form.validate_on_submit():
        updated_post.title = form.title.data
        updated_post.text = form.text.data
        updated_post.enabled = form.enabled.data

        if form.image.data:
            updated_post.image = save_picture(form.image.data)

        db.session.commit()

        return redirect(url_for('posts.post', id=updated_post.id))

    return render_template("update_post.html", form=form, post=updated_post, categories=categories_list)

@postsBp.route('/categories', methods=['GET'])
def categories():
    categories_list = db.session.query(Category).all()
    return render_template("categories.html", categories_list=categories_list)

@postsBp.route('/categories/<int:id>', methods=['GET'])
def category(id):
    category = db.session.query(Category).filter(Category.id == id).first()
    return render_template("category.html", category=category)

@postsBp.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()

    if form.validate_on_submit():
        name=form.name.data
        new_сategory = Category(name=name)
        db.session.add(new_сategory)
        db.session.commit()

        return redirect(url_for('posts.categories'))
    
    return render_template("create_category.html", form=form)

@postsBp.route("/categories/<int:id>/delete")
def delete_category(id):
    deleted_category = db.session.query(Category).filter(Category.id == id).first()
    db.session.delete(deleted_category)
    db.session.commit()
    return redirect(url_for("posts.categories"))

@postsBp.route('/categories/<int:id>/update', methods=["POST", "GET"])
def update_category(id):
    form = CategoryForm()
    updated_category = db.session.query(Category).filter(Category.id == id).first()

    if form.validate_on_submit():
        updated_category.name = form.name.data
        db.session.commit()

        return redirect(url_for('posts.categories'))

    return render_template("update_category.html", form=form, category=updated_category)