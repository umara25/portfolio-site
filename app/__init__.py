import os
from flask import Flask, render_template, request, abort
from dotenv import load_dotenv
from peewee import *
import datetime
import re
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route("/")
def robert():
    return render_template(
        "about-me.html",
        title="Robert Xing",
        url=os.getenv("URL"),
        picture="./static/img/robert.jpg",
        name="Robert Xing",
        travel_map="https://www.google.com/maps/d/u/0/embed?mid=1oJDJsnCdi9E7MYmkzrBWCNJ_l3Qb8cw&ehbc=2E312F",
        bio="Hi! I'm an incoming 4th year student at Western University, completing a dual degree in software engineering and Ivey HBA. "
        "I am super excited to gain some PE experience and meet some incredibly talented people through the MLH Fellowship!",
        schools=[
            {
                "school": "Western University",
                "program": "BESc Software Engineering and BA Honours Business Administration",
                "time": "Sep 2022-Apr 2027",
            }
        ],
        work_experiences=[
            {
                "title": "Research Assistant, Data Scientist",
                "company": "Ivey Business School",
                "date": "Feb 2025-present",
            },
            {
                "title": "Software Engineer Intern",
                "company": "Agora Tutoring",
                "date": "Feb 2025-Apr 2025",
            },
        ],
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title="Robert's Hobbies",
        url=os.getenv("URL"),
        name="Robert",
        hobbies=[
            {"name": "Motorsports (F1 and WEC)", "image": "./static/img/wec.jpg"},
            {
                "name": "Sports (Skiing, Golf, and Badminton)",
                "image": "./static/img/robert-ski.jpg",
            },
            {"name": "Photography", "image": "./static/img/robert-photo.jpg"},
            {"name": "Travel", "image": "./static/img/robert-travel.png"},
        ],
    )


@app.route("/timeline")
def timeline():
    post_data = get_time_line_post()
    return render_template(
        "timeline.html", title="Timeline", posts=post_data["timeline_posts"]
    )


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    content = data.get("content", "").strip()

    valid_email = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

    if len(name) == 0:
        return "Invalid name", 400
    elif not valid_email:
        return "Invalid email", 400
    elif len(content) == 0:
        return "Invalid content", 400
    else:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_time_line_post(post_id):
    deleted = TimelinePost.delete().where(TimelinePost.id == post_id).execute()
    if deleted:
        return {"message": f"Post {post_id} deleted."}, 200
    else:
        abort(404, description=f"Post {post_id} not found.")


@app.route("/api/timeline_post/testing/reset", methods=["DELETE"])
def reset_timeline_post():
    if os.getenv("TESTING") == "true":
        reset_testing_posts = TimelinePost.delete().execute()
        return f"{reset_testing_posts}", 200
    return "Not in testing mode", 403
