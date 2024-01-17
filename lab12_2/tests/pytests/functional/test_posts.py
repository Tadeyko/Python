from extensions import db
from app.posts.models import Post, Category
import os 
from app import create_app
import pytest

@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'test_config.py'
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    c1 = Category(name="films")
    c2 = Category(name="music")
    db.session.add(c1)
    db.session.add(c2)

    db.session.commit()

    p1 = Post(
        title="p1", text="p1 text", user_id=1, category_id=c1.id
    )
    p2 = Post(
        title="p2", text="p2 text", user_id=1, category_id=c2.id
    )
    p3 = Post(
        title="p3", text="p3 text", user_id=2, category_id=c1.id
    )

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)

    db.session.commit()

    yield 

    db.drop_all() 


def test_home_page(test_client, init_database):
    response = test_client.get('/posts/')
    assert response.status_code == 200
    assert b"p1" in response.data
    assert b"p2" in response.data
    assert b"p3" in response.data

def test_home_page_post(test_client):
    response = test_client.post('/posts/')
    assert response.status_code == 405
    assert b"p1" not in response.data

def test_get_create_post_page(test_client):
    response = test_client.get("/posts/create")
    assert response.status_code == 200
    assert 'Login' in response.get_data(as_text=True)

def test_post_create_post_page(test_client, init_database):
    response = test_client.post('/posts/create', data={
        'title': 'title',
        'text': 'text',
        'user_id': 1,
        'category_id': 1
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'title' in response.data
    assert b'text' in response.data

def test_get_post_page(test_client, init_database):
    response = test_client.get("/posts/1")
    assert response.status_code == 200
    assert b"p1" in response.data

def test_get_update_post_page(test_client):
    response = test_client.get("/posts/1/update")
    assert response.status_code == 200

def test_post_update_post_page(test_client):
    test_post = Post(title="Test Post", text="Test Text", enabled=True)
    db.session.add(test_post)
    db.session.commit()

    response = test_client.post(
        f'/posts/{test_post.id}/update',
        data={
            'title': 'Updated Title',
            'text': 'Updated Text',
            'enabled': False,
        },
        follow_redirects=True
    )

    assert response.status_code == 200

def test_get_delete_post_page(test_client, init_database):
    test_post = Post(title="Test Post", text="Test Text", enabled=True)
    db.session.add(test_post)
    db.session.commit()

    response = test_client.get(f"/posts/{test_post.id}/delete")
    assert response.status_code == 302
    assert b"Test Post" not in response.data

    deleted_post = db.session.query(Post).filter(Post.id == test_post.id).first()
    assert deleted_post is None