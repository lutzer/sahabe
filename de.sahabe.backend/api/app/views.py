'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import hashlib
import random
import string
import uuid as uid
import re

from impl import DBApiModule as db

from flask import render_template, flash, redirect, session, url_for, request, g, json
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, oid
from forms import SignUpForm, LoginForm, OpenIDLoginForm, LoadForm
from entries import User
import entries
from werkzeug import secure_filename
import datetime

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = g.user
    conn = db.connect()
    dbLinks = db.selectFrom(conn, {"link"} ,"title", "url", "id", user_id=user.id)
    
    links = []
    for link in dbLinks:
        uri = link[1].decode('utf-8')
        m = re.search("(http(:|s:)//(.+?)/)", uri)
        iconUri = m.group(1)+"favicon.ico"
        #logo = db.selectFrom(conn, {"meta_data"}, "value", link_id=link[2], l_key="logo")
        links.append({"title":link[0].decode('utf-8') , "uri":uri, "logo":iconUri})

    return render_template('index.html',
                           title = 'Home',
                           user = user,
                           links = links)
    
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        userId = str(uid.uuid4())
        userName = form.username.data
        email = form.email.data
        
        pw = form.password.data
        pwHash = hashlib.sha256(pw).hexdigest()
        salt = hashlib.sha256(randomText()).hexdigest()
        
        conn = db.connect()
        db.insertToTable(conn, "user", id = userId, name = userName, email = email)
        
        db.insertToTable(conn, "pw_hash", user_id = userId, value = pwHash, salt = salt)
        flash("You signed up successfully.")
        return redirect(request.args.get("next") or url_for("sign_up"))
    return render_template('sign_up.html',
                           title = 'Sign Up',
                           form = form)
    
@app.route("/load_links", methods=["GET", "POST"])
@login_required
def load_links():
    form = LoadForm()
    
    if form.validate_on_submit():
        fileName = form.filename.data
        #jsonData = open(fileName)
        data = json.load(fileName)
        
        linksData = data["children"][0]["children"]
        count = 0
        links = []
        for i in range(4, len(linksData)):
            if linksData[i].has_key("title") and linksData[i].has_key("uri"): 
                title =  linksData[i]["title"].replace("'", "")
                uri = linksData[i]["uri"]
                modified = linksData[i]["lastModified"]/1000000
                formated_modified = str(datetime.datetime.fromtimestamp(modified))
                
                m = re.search("(http(:|s:)//(.+?)/)", uri)
                iconUri = m.group(1)+"favicon.ico"
                
                links.append({"title" :title , "uri":uri, "logo":iconUri})
                conn = db.connect()
                linkId = str(uid.uuid4())
                db.insertToTable(conn, "link",
                                 id = linkId,
                                 user_id = g.user.id,
                                 title = title,
                                 url = uri,
                                 url_hash = hashlib.md5(uri).hexdigest(),
                                 modified_at = formated_modified)
                count += 1
        user = g.user
        flash(str(count) + " links were added.")
        return render_template('index.html',
                                title = 'Home',
                                user = user,
                                links = links)
                
    return render_template('load_links.html',
                           title = 'Load links',
                           form = form)

@app.route('/openid_login', methods = ['GET','POST'])
@oid.loginhandler
def openid_login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = OpenIDLoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('openid_login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        user = entries.get_user_by_name(name)
        
        pw = hashlib.sha256(form.password.data).hexdigest()
        savedPw = entries.get_pw_hash_by_user_id(user.id)
        
        if pw == savedPw:
            remember_me = form.remember_me.data
            session['remember_me'] = form.remember_me.data
        
            login_user(user, remember = remember_me)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("incorrect password or username.")
            render_template("login.html",
                           title = "Login",
                           form = form)
    return render_template("login.html",
                           title = "Login",
                           form = form)
     
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('openid_login'))
    user = entries.get_user_by_name(resp.nickname)
    
    if user is None:
        name = resp.nickname
        if name is None or name == "":
            name = resp.email.split('@')[0]
        user = User(id , name ,resp.email)
        user.add_user()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
    
@lm.user_loader
def load_user(_id):
    return entries.get_user_by_id(_id)


#When the log in view is redirected to, it will have a next variable in the query string,
#which is the page that the user was trying to access.
#If you would like to customize the process further.
#@lm.unauthorized_handler
#def unauthorized():
#    flash("bla")
#    return redirect(url_for('openid_login'))

@app.before_request
def before_request():
    g.user = current_user
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    
def randomText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

