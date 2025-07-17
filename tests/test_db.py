# test_db.py

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe',
            email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe',
            email='jame@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2
        # TODO: Get timeline posts and assert that they are correct

        posts = list(TimelinePost.select().order_by(TimelinePost.id))
        self.assertEqual(len(posts), 2)

        self.assertEqual(posts[0].name, 'John Doe', "The name is incorrect")
        self.assertEqual(posts[0].email, 'john@example.com', "The email is incorrect")
        self.assertEqual(posts[0].content, 'Hello world, I\'m John!', "The message is incorrect")

        self.assertEqual(posts[1].name, 'Jane Doe', "The name is incorrect")
        self.assertEqual(posts[1].email, 'jame@example.com', "The email is incorrect")
        self.assertEqual(posts[1].content, 'Hello world, I\'m Jane!', "The message is incorrect")
