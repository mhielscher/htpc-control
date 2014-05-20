#!/usr/bin/python

import time
import subprocess
import netifaces
import json

import os
time.sleep(3);
os.environ['HOME'] = "/home/restorer"
os.environ['DISPLAY'] = ":0.0"

from pymouse import PyMouse
#from jinja2 import Template
from flask import Flask, redirect, Response
app = Flask(__name__)

from local_settings import *

video_extensions = ('avi', 'mkv', 'mov', 'mpg', 'mp4', 'mpeg', 'wmv', 'rmvb', '3gp', 'ogm')

####
# Utility functions
####

def get_ips():
    ips = []
    for interface in netifaces.interfaces():
        if 2 in netifaces.ifaddresses(interface):
            for addr in netifaces.ifaddresses(interface)[2]:
                if not addr['addr'].startswith("127."):
                    ips.append(addr['addr'])
    return ips

def proc_is_running(proc):
    s = subprocess.Popen("ps xw -o comm".split(' '), stdout=subprocess.PIPE)
    procs = s.stdout.read().split('\n')
    print procs
    return proc in procs

####
# PC controls and navigation
####

@app.route("/")
def main_index():
    global template_dir
    #template = Template(open(template_dir+'/index.html', 'r').read())
    #return template.render()
    return open(template_dir+'/index.html', 'r').read()

@app.route("/vnc")
def vnc():
    global template_dir
    if not proc_is_running("x11vnc"):
        print "Starting VNC"
        if not subprocess.call("x11vnc -display :0 -scale 0.5 -wait 1000 -wait_ui 6.0 -shared -once -allow 192.168,127.0.0.1 -input MB -nopw -users restorer -logfile /home/restorer/htpc-vnc.log -quiet -bg -threads".split(' ')):
            return redirect("/")
    return open(template_dir+'/vnc.html', 'r').read()

@app.route("/netflix")
def netflix_index():
    global template_dir
    return open(template_dir+'/netflix.html', 'r').read()

@app.route("/vlc")
def vlc_index():
    global template_dir
    return open(template_dir+'/vlc.html', 'r').read()
    #return redirect("//:htpc:8080/")

@app.route("/shutdown", methods=['POST'])
def shutdown():
    subprocess.call(['shutdown', '-h', 'now'])
    return redirect("/")

@app.route("/netflix/hidemouse", methods=['POST'])
def netflix_hide_mouse():
    m = PyMouse()
    m.move(299, 0)
    m.move(300, 0)
    return ""

@app.route("/netflix/continueplaying", methods=['POST'])
def netflix_continue():
    m = PyMouse()
    x, y = m.screen_size()
    m.click(x/2, y/2-60)
    time.sleep(0.33)
    m.move(x/2, 0)
    return ""

@app.route("/netflix/play", methods=['POST'])
def netflix_play():
    m = PyMouse()
    m.move(150, 640)
    time.sleep(0.25)
    m.click(150, 640)
    m.move(300, 0)
    return ""

@app.route("/netflix/closetransition", methods=['POST'])
def netflix_close_transition():
    m = PyMouse()
    m.click(870, 675)
    time.sleep(5)
    m.click(1230, 55)
    return ""

@app.route("/netflix/nexteptrans", methods=['POST'])
def netflix_next_episode_trans():
    m = PyMouse()
    m.click(900, 550)
    time.sleep(1)
    m.move(300, 0)
    return ""

@app.route("/vlc/listdir/", defaults={'path': '.'})
@app.route("/vlc/listdir/<path:path>")
def vlc_listdir(path='.'):
    dirs, files = [sorted(l) for l in os.walk(os.path.join(file_manager_base_dir, path)).next()[1:3]]
    files = filter(lambda s: s.endswith(video_extensions), files)
    ls = json.dumps([dirs, files])
    return Response(ls, mimetype="text/json")

@app.route("/vlc/loadvideo/<path:path>", methods=['POST'])
def vlc_load_video(path):
    subprocess.call(["sudo", "-u", "restorer", "vlc", "-d", os.path.join(file_manager_base_dir, path)])
    return ""


if __name__ == "__main__":
    app.run(host=get_ips()[0], port=80, debug=True)


# x11vnc -display :0 -scale 0.5 -wait 1000 -wait_ui 6.0 -shared -once -allow 192.168 -input MB -nopw -users restorer -logfile /home/restorer/htpc-vnc.log -quiet -bg -threads
