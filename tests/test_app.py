# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html

        # TODO Add more tests relating to the home page

        assert "<title>MLH Fellow</title>" in html

        assert "MAPBOX_API_TOKEN" not in html  
        assert "initial_content" not in html  

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # TODO Add more tests relating to the /api/timeline_post GET and POST apis

        post1 = {
        "name": "Bob",
        "email": "bob@gmail.com",
        "content": "Hello from Bob"
        }

        response = self.client.post("/api/timeline_post", data=post1)
        assert response.status_code == 200
        created_post1 = response.get_json()
        assert created_post1["name"] == post1["name"]
        assert created_post1["email"] == post1["email"]
        assert created_post1["content"] == post1["content"]
        assert "id" in created_post1

        post2 = {
        "name": "Azam",
        "email": "Azam@example.com",
        "content": "Hello from Azam"
    }
        response = self.client.post("/api/timeline_post", data=post2)
        assert response.status_code == 200

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json["timeline_posts"]) == 2

        assert json["timeline_posts"][1]["name"] == "Bob"
        assert json["timeline_posts"][1]["email"] == "bob@gmail.com"
        assert json["timeline_posts"][1]["content"] == "Hello from Bob"

        assert json["timeline_posts"][0]["name"] == "Azam"
        assert json["timeline_posts"][0]["email"] == "Azam@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello from Azam"

        # TODO Add more tests relating to the timeline page

        response = self.client.get("/timeline")
        self.assertEqual(response.status_code, 200)

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html