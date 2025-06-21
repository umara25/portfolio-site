import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about-me.html', title="About Me", url=os.getenv("URL"),
        name="Name",
        bio="bio",
        schools=[
            {"school": "School Name", "program": "Program Name", "time": "YYYY-YYYY"}
        ],
        work_experiences=[
            {"title": "Job Title", "company": "Company Name", "date": "YYYY-YYYY"}
        ],
        hobbies=[
            {"name": "Hobby Name", "image": "./static/img/placeholder.jpg"}
        ]
    )

@app.route('/umar')
def umar():
    return render_template('umar.html', title="Umar Ahmer", url=os.getenv("URL"),
        name="Umar Ahmer",
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

