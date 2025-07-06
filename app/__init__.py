import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
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

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Robert's Hobbies", url=os.getenv("URL"),
        name="Robert",
        hobbies=[
            {"name": "Motorsports (F1 and WEC)", "image": "./static/img/wec.jpg"},
            {"name": "Sports (Skiing, Golf, and Badminton)", "image": "./static/img/robert-ski.jpg"},
            {"name": "Photography", "image": "./static/img/robert-photo.jpg"},
            {"name": "Travel", "image": "./static/img/robert-travel.png"}
        ]
    )