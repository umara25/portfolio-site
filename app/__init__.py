import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict



load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb 

mydb.connect()
mydb.create_tables([TimelinePost])



@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/robert')
def robert():
    return render_template('about-me.html', title="Robert Xing", url=os.getenv("URL"),
        picture="./static/img/robert.jpg",
        name="Robert Xing",
        travel_map="https://www.google.com/maps/d/u/0/embed?mid=1oJDJsnCdi9E7MYmkzrBWCNJ_l3Qb8cw&ehbc=2E312F",
        bio="Hi! I'm an incoming 4th year student at Western University, completing a dual degree in software engineering and Ivey HBA. "
        "I am super excited to gain some PE experience and meet some incredibly talented people through the MLH Fellowship!",
        schools=[
            {"school": "Western University", "program": "BESc Software Engineering and BA Honours Business Administration", "time": "Sep 2022-Apr 2027"}
        ],
        work_experiences=[
            {"title": "Research Assistant, Data Scientist", "company": "Ivey Business School", "date": "Feb 2025-present"},
            {"title": "Software Engineer Intern", "company": "Agora Tutoring", "date": "Feb 2025-Apr 2025"}
        ]
    )

@app.route('/robert-hobbies')
def robert_hobbies():
    return render_template('hobbies.html', title="Robert's Hobbies", url=os.getenv("URL"),
        name="Robert",
        hobbies=[
            {"name": "Motorsports (F1 and WEC)", "image": "./static/img/wec.jpg"},
            {"name": "Sports (Skiing, Golf, and Badminton)", "image": "./static/img/robert-ski.jpg"},
            {"name": "Photography", "image": "./static/img/robert-photo.jpg"},
            {"name": "Travel", "image": "./static/img/robert-travel.png"}
        ]
    )

@app.route('/umar')
def umar():
    return render_template('about-me.html', title="Umar Ahmer", url=os.getenv("URL"),
        name="Umar Ahmer",
        picture="./static/img/umar.jpg",
        travel_map="https://www.google.com/maps/d/u/0/embed?mid=1T0a6Ayom7RTvFHPP1N8UDydwCpS5n9E&ehbc=2E312F&noprof=1",
        bio="Hi! I am a computer science student at McMaster University going into my second year. "
        "I am passionate about PE and really excited" 
        " to be a part of the MLH Fellowship program.",
        schools=[
            {"school": "McMaster University", "program": "Bachelor of Applied Science in Computer Science", "time": "2024-2028"}
        ],
        work_experiences=[
            {"title": "Team Lead", "company": "Google Developer Groups", "date": "2024-present"},
            {"title": "Programming Instructor", "company": "Code Club Canada", "date": "2023-2024"},
            {"title": "Team Lead", "company": "3571 Mustang Robotics", "date": "2022-2024"}
        ],
        hobbies=[
            {"name": "Programming & Development", "image": "./static/img/coding.jpg"},
            {"name": "Basketball", "image": "./static/img/basketball.png"},
            {"name": "Video Games", "image": "./static/img/videogames.jpg"}
        ]
    )

@app.route('/umar-hobbies')
def umar_hobbies():
    return render_template('hobbies.html', title="Umar's Hobbies", url=os.getenv("URL"),
        name="Umar",
        hobbies=[
            {"name": "Traveling (Picture is from BC, Canada)", "image": "./static/img/travel-umar.jpg"},
            {"name": "Basketball (NBA)", "image": "static/img/basketball-umar.jpg"},
            {"name": "Video Games (Minecraft, Valorant)", "image": "./static/img/game-umar.jpg"},
            {"name": "Hiking", "image": "./static/img/hiking-umar.jpg"}
        ]
    )

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title='Timeline')

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return {'error': 'Invalid name'}, 400
    if not email or '@' not in email:
        return {'error': 'Invalid email'}, 400
    if not content:
        return {'error': 'Invalid content'}, 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
