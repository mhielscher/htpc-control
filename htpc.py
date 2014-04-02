import time
import os
os.environ['DISPLAY'] = ":0.0"

from pymouse import PyMouse
from jinja2 import Template
from flask import Flask, redirect
app = Flask(__name__)

template_dir = './templates'

@app.route("/")
def index():
    global template_dir
    #template = Template(open(template_dir+'/index.html', 'r').read())
    #return template.render()
    return open(template_dir+'/index.html', 'r').read()

@app.route("/hidemouse")
def netflix_hide_mouse():
    m = PyMouse()
    m.move(299, 0)
    m.move(300, 0)
    return redirect("/")

@app.route("/continueplaying")
def netflix_continue():
    m = PyMouse()
    x, y = m.screen_size()
    m.click(x/2, y/2-60)
    time.sleep(0.33)
    m.move(x/2, 0)
    return redirect("/")

@app.route("/play")
def netflix_play():
    m = PyMouse()
    m.click(275, 640)
    m.move(300, 0)
    return redirect("/")

@app.route("/closetransition")
def netflix_close_transition():
    m = PyMouse()
    m.click(870, 675)
    time.sleep(5)
    m.click(1230, 55)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="192.168.1.5", port=80)
