'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
import hashlib
import random
import string
import uuid as uid
import re
from lxml import etree 

from impl import DBApiModule as db

from flask import render_template, flash, redirect, session, url_for, request, g, json, Response
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm  #, oid
import entries
#from werkzeug import secure_filename
import datetime
import urllib2

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
    return render_template('sign_up.html',
                           title = 'Sign Up')
    
@app.route("/submit_sign_up", methods=["GET", "POST"])
def submit_sign_up():
    userId = str(uid.uuid4())
    userName = request.form["username"]
    email = request.form["email"]
    
    pw = request.form["password"]
    pwHash = hashlib.sha256(pw).hexdigest()
    salt = hashlib.sha256(randomText()).hexdigest()
    
    conn = db.connect()
    db.insertToTable(conn, "user", id = userId, name = userName, email = email)
    
    db.insertToTable(conn, "pw_hash", user_id = userId, value = pwHash, salt = salt)
    flash("You signed up successfully.")
    return redirect(request.args.get("next") or url_for("sign_up"))

@app.route("/load_links", methods=["GET", "POST"])
@login_required
def load_links():
    return render_template('load_links.html',
                           title = 'Load links')

    
@app.route("/submit_load_links", methods=["GET", "POST"])
@login_required
def submit_load_links():
    fileName = request.files["file"]
    #jsonData = open(fileName)
    data = ""
    dataFormat = fileName.content_type 
    if dataFormat == "text/html":
        with open(fileName.filename, "r") as html:
            for line in html:
                print line
    elif fileName.content_type == "application/json":
        data = json.load(fileName)
    else:
        Exception(dataFormat+ " data formats is not supported ") 
    
    
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


# @app.route('/openid_login', methods = ['GET','POST'])
# @oid.loginhandler
# def openid_login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))
#     form = OpenIDLoginForm()
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
#     return render_template('openid_login.html',
#                            title = 'Sign In',
#                            form = form,
#                            providers = app.config['OPENID_PROVIDERS'])


@app.route("/link/add", methods=["PUT"])
@login_required
def addLink():
    linkId = str(uid.uuid4())
    kwargs ={}
    kwargs["id"] = linkId
    kwargs["user_id"] = g.user.id
    if request.form.has_key("url") :
        kwargs["url"]=request.form["url"]
        kwargs["url_hash"] = hashlib.md5(kwargs["url"]).hexdigest() 
    else:
        js = json.dumps({"message":"an url must be added"})
        #FIXME: change the return status
        return Response(js, status=400, mimetype='application/json')
    if request.form.has_key("title"): 
        kwargs["title"]=request.form["title"] 
    if request.form.has_key("description"):
        kwargs["description"]=request.form["description"]
    if request.form.has_key("typeName"):
        kwargs["type_name"]=request.form["typeName"]
    kwargs["modified_at"]=timeStamp()
    conn = db.connect()
    #FIXME: use another algorithm
    html =urllib2.urlopen(kwargs["url"]).read()
    xPath = etree.XPath("//link[@rel = 'shortcut icon']/@href")
    parsedHtml = etree.HTML(html)
    selected = xPath(parsedHtml)
    iconUrl = "not_found"
    if selected != []:
        iconUrl = selected[0]
    try:
        db.insertToTable(conn,
                     "link",
                    **kwargs)
        db.insertToTable(conn,
                         "meta_data",
                         link_id=linkId,
                         l_key="logo",
                         value=iconUrl)
    except Exception, e: 
        js = json.dumps({"message":"Error %s" %(e)})
        #FIXME: http status 401 is not the correct one. 
        resp = Response(js, status=400, mimetype='application/json')
        return resp 
    
    js = json.dumps({"message":"link added successfully"})
    resp = Response(js, status=200, mimetype='application/json')
    return resp
    
    
    
    
    

@app.route("/links", methods=["GET", "POST"])
@login_required
def getAllLinks():
    user = g.user
    conn = db.connect()
    dbLinks = db.selectFrom(conn, {"link"} ,"id", "title", "url", "modified_at", user_id=user.id)
    
    links = []
    for i in range(len(dbLinks)):
        url = dbLinks[i][2]
        m = re.search("(http(:|s:)//(.+?)/)", url)
        iconUrl =""
        if m is not None:
            iconUrl = m.group(1)+"favicon.ico"
        else:
            iconUrl = "not_found"
        links.append({"id":dbLinks[i][0],
                      "title":dbLinks[i][1] ,
                      "url":url,
                      "iconUrl":iconUrl ,
                      "modifiedAt":dbLinks[i][3]})  
    js = json.dumps(links)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/login", methods=["POST"])
def login():
    name = request.form["username"]
    user = ""
    
    try:
        user = entries.get_user_by_name(name)
    except Exception : 
        js = json.dumps({"message":"incorrect password or user name."})
        resp = Response(js, status=401, mimetype='application/json')
        return resp 

    pw = hashlib.sha256(request.form["password"]).hexdigest()
    savedPw = entries.get_pw_hash_by_user_id(user.id)
    if pw == savedPw:
        remember_me = request.form["remember"].title()
        session['remember_me'] = remember_me
        login_user(user, remember_me)
        
        js = json.dumps({"message":"Logged in successfully.", "userId":user.id})
        resp = Response(js, status=200, mimetype='application/json')
        return resp 
    else:
        js = json.dumps({"message":"incorrect password or user name."})
        resp = Response(js, status=401, mimetype='application/json')
        return resp

# @app.route("/submit_login", methods=["GET", "POST"])
# def submit_login():
#     name = request.form["username"]
#     user = entries.get_user_by_name(name)
#     
#     pw = hashlib.sha256(request.form["password"]).hexdigest()
#     savedPw = entries.get_pw_hash_by_user_id(user.id)
#     if pw == savedPw:
#         remember_me = False
#         for checkbox in request.form.getlist("remember_me"):
#             if checkbox == "on":
#                 remember_me = True
#         session['remember_me'] = remember_me
#         login_user(user, remember_me)
#         flash("Logged in successfully.")
#         return redirect(request.args.get("next") or url_for("index"))
#     else:
#         flash("incorrect password or username.")
#         render_template("login.html",
#                        title = "Login")
#     return render_template("login.html",
#                            title = "Login")
     
# @oid.after_login
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('openid_login'))
#     user = entries.get_user_by_name(resp.nickname)
#     
#     if user is None:
#         name = resp.nickname
#         if name is None or name == "":
#             name = resp.email.split('@')[0]
#         user = User(id , name ,resp.email)
#         user.add_user()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember = remember_me)
#     return redirect(request.args.get('next') or url_for('index'))
    
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
    js = json.dumps({"message":"logout was successful"})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

def timeStamp():
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(timeStamp)
    
def randomText(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

