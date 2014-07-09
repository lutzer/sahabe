'''
Created on Jul 4, 2014

@author: Maan Al Balkhi
'''
from flaskext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, FileField
from wtforms.validators import Required

class SignUpForm(Form):
    username = TextField("username", validators = [Required()])
    email = TextField("email", validators = [Required()])
    password =  PasswordField("password", validators = [Required()])
    
class LoginForm(Form):
    username = TextField("username", validators = [Required()])
    password =  PasswordField("password", validators = [Required()])
    remember_me = BooleanField("remember_me", default = False)
    
class OpenIDLoginForm(Form):
    openid = TextField("openid", validators = [Required()])
    remember_me = BooleanField("remember_me", default = False)
    
class LoadForm(Form):
    filename = FileField("filename", validators = [Required()])