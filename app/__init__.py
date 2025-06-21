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
