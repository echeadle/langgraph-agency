```python
# test_app.py
import pytest
from app import app, db
from models import Post

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Blog' in response.data

def test_create_post_get(client):
    response = client.get('/post/new')
    assert response.status_code == 200
    assert b'Create a New Post' in response.data

def test_create_post_post(client):
    response = client.post('/post/new', data={
        'title': 'Test Title',
        'content': 'Test Content'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the Blog' in response.data
    with app.app_context():
        post = Post.query.filter_by(title='Test Title').first()
        assert post is not None
        assert post.content == 'Test Content'

def test_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert b'Blog Posts' in response.data
```