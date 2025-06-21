import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/robert')
def robert():
    return render_template('about-me.html', title="Robert Xing", url=os.getenv("URL"),
        image="./static/img/robert.jpg",
        name="Robert Xing",
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
            {"name": "Travel", "image": "./static/img/robert-travel.jpg"}
        ]
    )

@app.route('/umar')
def umar():
    return render_template('about-me.html', title="Umar Ahmer", url=os.getenv("URL"),
        name="Umar Ahmer",
        picture="./static/img/umar.jpg",
        bio="Hey! I am a computer science student at McMaster University going into my second year. "
        "I am passionate about PE and really excited" 
        " to be a part of the MLH Fellowship program.",
        schools=[
            {"school": "McMaster University", "program": "Bachelor of Applied Science in Computer Science", "time": "2024-2028"}
        ],
        work_experiences=[
            {"title": "Team Member", "company": "Google Developer Student Clubs", "date": "2024-present"},
            {"title": "Programming Instructor", "company": "Code Club Canada", "date": "2023-2024"},
            {"title": "Team Lead", "company": "3571 Mustang Robotics", "date": "2022-2024"}
        ],
        hobbies=[
            {"name": "Programming & Development", "image": "./static/img/coding.jpg"},
            {"name": "Basketball", "image": "./static/img/basketball.png"},
            {"name": "Video Games", "image": "./static/img/videogames.jpg"}
        ]
    )

