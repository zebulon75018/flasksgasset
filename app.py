#!/usr/bin/python
# coding: utf-8
from flask import Flask, flash, redirect, render_template, request, session, abort

import os
import shotgun_api3 
import pprint

app = Flask(__name__)

SERVER_PATH ="https://xxxx.shotgunstudio.com/" 
SCRIPT_NAME = 'xxxxxx'
SCRIPT_KEY = "xxxxxxxxxxxxxx"

sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

filters =[ ['project', 'is', {'type': 'Project', 'id': xx}] ]
fields=["code","image","id","sg_category","sg_asset_type","description","tags","created_at","sg_published_files"]

assets= sg.find("Asset",filters,fields)
idxasset = {}
cat = []
for a in assets:
   if a["sg_asset_type"] is not None:
   	cat.append(a["sg_asset_type"].replace(" ","_").upper())
   	a["sg_category"] =a["sg_asset_type"].replace(" ","_").upper()
	idxasset[a["id"]]=a

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

@app.route('/asset/<id>')
def asset(id): 
    filters =[ ['entity', 'is', {'type': 'Asset', 'id': int(id)}] ]
    #fields=["code","image","id"]
    #pf= sg.find("PublishedFile",filters,fields)
    fields=["code","image","entity","id","sg_uploaded_movie_webm","sg_uploaded_movie_mp4","sg_uploaded_movie_frame_rate"]
    pf= sg.find("Version",filters,fields)
    pprint.pprint(pf)
    return render_template("asset.html", pf=pf,asset=idxasset[int(id)])


@app.route('/')
def home():
    #if not session.get('logged_in'):
    #    return render_template('login.html')
    #else:
    return render_template("index.html",assets=assets,cat=cat)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True, port=5005)

 
