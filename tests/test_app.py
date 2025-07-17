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
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<header class="nav-bar">', html)
        self.assertIn('<div class="profile">', html)

    def test_timeline(self):

        response = self.client.get("/api/timeline_post")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json = response.get_json()
        self.assertIn("timeline_posts", json)
        self.assertEqual(len(json["timeline_posts"]), 0)

        post_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "content": "Hi, I'm John Doe!",
        }
        post = self.client.post("/api/timeline_post", json=post_data)
        self.assertEqual(post.status_code, 200)
        new_post = self.client.get("/api/timeline_post")
        new_post_json = new_post.get_json()
        self.assertEqual(len(new_post_json["timeline_posts"]), 1)
        first_post = new_post_json["timeline_posts"][0]
        self.assertEqual(first_post["name"], "John Doe")
        self.assertEqual(first_post["email"], "johndoe@example.com")
        self.assertEqual(first_post["content"], "Hi, I'm John Doe!")

        # test html separately
        html_response = self.client.get("/timeline")
        self.assertEqual(html_response.status_code, 200)
        timeline_posts_html = html_response.get_data(as_text=True)
        self.assertIn('<header class="nav-bar">', timeline_posts_html)
        self.assertIn("<h2>New post</h2>", timeline_posts_html)
        self.assertIn('<form id="post-form">', timeline_posts_html)
        self.assertIn("<h2>Robert's Timeline</h2>", timeline_posts_html)
        self.assertIn('<div id="post-list">', timeline_posts_html)

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn("Invalid name", html)

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn("Invalid content", html)

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn("Invalid email", html)
