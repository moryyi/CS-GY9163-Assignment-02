#!/usr/bin/python3
# coding: utf-8


from flask import Flask, request, render_template, session, logging, url_for, redirect, flash
from flask import make_response
from flask_wtf.csrf import CSRFProtect
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField
import base64, hashlib, random, string
import subprocess

from src.myForms import RegisterForm, LoginForm, ContentForm


USER_DATABASE = {}

ROOT_URL = "/cs9163/hw02"

def configure_routes(app):

	# Login
	@app.route(ROOT_URL + '/login', methods=['GET', 'POST'])
	def login():
		if "log" in session and session["log"]:
			resp = make_response(redirect(url_for('spell_check')))
			return resp
		
		form = LoginForm()
		if form.validate_on_submit():
			username = form.username.data
			password = form.password.data
			phone = form.phone.data
			(ifLoginSuccess, errorMessage) = login_with_user_info(username, password, phone)
			if ifLoginSuccess:
				session["log"] = True
				flash(["result", errorMessage], "success")
				resp = make_response(redirect(url_for('spell_check')))
				return resp
			else:
				flash(["result", errorMessage], "danger")
		resp = make_response(render_template("./login.html", form=form))
		return resp


	# Logout
	@app.route(ROOT_URL + '/logout', methods=['GET'])
	def logout():
		session["log"] = False
		session.pop("username", None)
		return redirect(url_for("login"))


	# Registeration
	@app.route(ROOT_URL + '/register', methods=['GET', 'POST'])
	def register():
		if "log" in session and session["log"]:
			resp = make_response(redirect(url_for('spell_check')))
			return resp
		form = RegisterForm()
		if form.validate_on_submit():
			username = form.username.data
			password = form.password.data
			phone = form.phone.data
			(ifRegisterSuccess, errorMessage) = register_with_user_info(username, password, phone)
			if not ifRegisterSuccess:
				flash(["success", errorMessage], "danger")
			else:
				flash(["success", errorMessage], "success")
				resp = make_response(redirect(url_for('login')))
				return resp
		resp = make_response(render_template("./register.html", form=form))
		return resp


	# Spell-Check
	@app.route(ROOT_URL + '/spell_check', methods=['GET', 'POST'])
	def spell_check():
		form = ContentForm()
		if form.validate_on_submit():
			content = form.inputtext.data
			misspelled_words = check_text_spelling(content)
			response = [content, misspelled_words]			
			resp = make_response(render_template('./spell.html', response=response, form=form))
			return resp

		else:
			if "log" in session and session["log"]:
				resp = make_response(render_template('./spell.html', form=form))
				return resp
			else:
				resp = make_response(redirect(url_for('login')))
				return resp


	# Utils
	def register_with_user_info(username, password, phone):
		"""
		return ifRegisterSuccess: bool, errorMessage: string
		"""
		if username in USER_DATABASE.keys():
			# Given username has been already registered
			return (False, "failure")
		else:
			USER_DATABASE[username] = {
				"password": password,
				"phone": phone
			}
			return (True, "success")


	def login_with_user_info(username, password, phone):
		"""
		return ifLoginSuccess: bool, errorMessage: string
		"""
		if username not in USER_DATABASE.keys():
			return (False, "Incorrect")
		else:
			if password != USER_DATABASE[username]["password"]:
				return (False, "Incorrect")
			elif phone != USER_DATABASE[username]["phone"]:
				return (False, "Two-factor failure")
			else:
				return (True, "Login success")


	def gen_random_filename():
		_f = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
		return "tmp_" + base64.urlsafe_b64encode(hashlib.md5(_f.encode()).digest()).decode()


	def check_text_spelling(content):
		_tmp_filename = gen_random_filename()
		with open(_tmp_filename, "w") as fp:
			fp.write(content)
		proc = subprocess.Popen("./spell-check/a.out ./{} ./spell-check/wordlist.txt".format(_tmp_filename), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = proc.communicate()
		if err == b'':
			out = out.decode().replace('\n', ',')
		else:
			pass
		subprocess.call("rm -rf ./{}".format(_tmp_filename), shell=True)
		return out


# Create Flask app as a global variable.
# This enables app to be executed by command:
#   - export FLASK_APP=app.py
#   - flask run
app = Flask(__name__, template_folder="./templates")
app.secret_key = "CS9163Assignment02WebsiteFlaskSessionSecretKey"
app.WTF_CSRF_SECRET_KEY = "CS9163Assignment02WebsiteFlaskWTFCSRFToken"
# Random secret_key does work, but this will lose all existed sessions
# when current flask application restarts.
# app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
# app.WTF_CSRF_SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))

app.config.update(
	SESSION_COOKIE_HTTPONLY=True,
	SESSION_COOKIE_SAMESITE='Lax',
	PERMANENT_SESSION_LIFETIME=600
)
csrf = CSRFProtect(app)
configure_routes(app)

if __name__ == "__main__":
	app.run(debug=True)
