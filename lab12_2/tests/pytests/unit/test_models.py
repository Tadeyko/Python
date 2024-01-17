from app.posts.models import Post

def test_new_post():
    post = Post(
        title="p1", text="p1 text", user_id=1, category_id=1
    )

    assert post.title == "p1"
    assert post.text == "p1 text"
    assert post.user_id == 1
    assert post.category_id == 1

def test_update_post():
    post = Post(
        title="p1", text="p1 text", user_id=1, category_id=1
    )

    post.title = "p2"
    post.text = "p2 text"

    assert post.title == "p2"
    assert post.text == "p2 text"
    assert post.user_id == 1
    assert post.category_id == 1