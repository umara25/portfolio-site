import unittest
import os

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # Clear timeline posts in between tests
    def tearDown(self):
        self.client.delete("/api/timeline_post/testing/reset")

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<header class="nav-bar">' in html
        assert '<div class="profile">' in html

    def test_timeline(self):

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        post_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "content": "Hi, I'm John Doe!",
        }
        post = self.client.post("/api/timeline_post", json=post_data)
        assert post.status_code == 200
        new_post = self.client.get("/api/timeline_post")
        new_post_json = new_post.get_json()
        assert len(new_post_json["timeline_posts"]) == 1
        first_post = new_post_json["timeline_posts"][0]
        assert first_post["name"] == "John Doe"
        assert first_post["email"] == "johndoe@example.com"
        assert first_post["content"] == "Hi, I'm John Doe!"

        # test html separately
        html_response = self.client.get("/timeline")
        assert html_response.status_code == 200
        timeline_posts_html = html_response.get_data(as_text=True)
        assert '<header class="nav-bar">' in timeline_posts_html
        assert "<h2>New post</h2>" in timeline_posts_html
        assert '<form id="post-form">' in timeline_posts_html
        assert "<h2>Robert's Timeline</h2>" in timeline_posts_html
        assert '<div id="post-list">' in timeline_posts_html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
