#!/usr/bin/python
# coding: utf-8
from flask import Flask, flash, redirect, render_template, request, session, abort

import os
import shotgun_api3
import pprint

app = Flask(__name__)
SERVER_PATH ="https://xxxxx.shotgunstudio.com/" 
SCRIPT_NAME = 'xxxxx'
SCRIPT_KEY = "xxxxx"

sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

ID_PROJECT = xx

filters =[ ['project', 'is', {'type': 'Project', 'id': ID_PROJECT}] ]
fields=["code","image","id","sg_category","description","tags","created_at"]

assets= sg.find("Asset",filters,fields)
#pprint.pprint(assets)
cat = []
for a in assets:
   if a["sg_category"] is not None:
   	cat.append(a["sg_category"].replace(" ","_").upper())
   	a["sg_category"] =a["sg_category"].replace(" ","_").upper()

cat = set(cat)

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
    	return render_template("index.html",assets=assets,cat=cat)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)

 