#!/usr/bin/python3
# coding: utf-8


from flask import Flask, request, render_template, session, logging, url_for, redirect, flash
from flask import g
import base64, hashlib, random, string
import sqlite3, subprocess


app = Flask(__name__)
DATABASE = "./sqlite3/cs9163hw02.sqlite"


# Login
@app.route('/cs9163/hw02/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get("uname")
		password = request.form.get("pword")
		phone = request.form.get("2fa")
		(ifLoginSuccess, errorMessage) = login_with_user_info(username, password, phone)
		if ifLoginSuccess:
			session["log"] = True
			flash(["result", errorMessage], "success")
			return redirect(url_for("spell_check"))
		else:
			flash(["result", errorMessage], "danger")
			return render_template('./login.html')
	else:
		return render_template('./login.html')


# Logout
@app.route('/cs9163/hw02/logout', methods=['GET'])
def logout():
	session["log"] = False
	return render_template('./login.html')


# Registeration
@app.route('/cs9163/hw02/register', methods=['GET', 'POST'])
def register():
	if request.method == "POST":
		username = request.form.get("uname")
		password = request.form.get("pword")
		phone = request.form.get("2fa")
		(ifRegisterSuccess, errorMessage) = register_with_user_info(username, password, phone)
		if ifRegisterSuccess:
			flash(["success", errorMessage], "success")
			return render_template('./login.html')
		else:
			flash(["success", errorMessage], "danger")
			return render_template('./register.html')
	else:
		return render_template('./register.html')


# Spell-Check
@app.route('/cs9163/hw02/spell_check', methods=['GET', 'POST'])
def spell_check():
	if request.method == 'POST':
		content = request.form.get("inputtext")
		misspelled_words = check_text_spelling(content)
		response = [content, misspelled_words]
		return render_template('./spell.html', response=response)
	else:
		return render_template('./spell.html')


# Utils
def query_db(query, args=(), one=False):
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute(query, args)
	rv = cur.fetchall()
	conn.close()
	return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	result = None
	try:
		cur.execute(query, args)
		conn.commit()
		result = True
	except:
		conn.roolback()
		result = False
	finally:
		conn.close()
	print("insert_db -> {}".format(result))
	return result

def register_with_user_info(username, password, phone):
	"""
	return ifRegisterSuccess: bool, errorMessage: string
	"""
	# Get existed usernames
	_username = query_db('select username from User where username = ?;', [username], one=True)
	if _username is not None:
		# Given username has been already registered
		return (False, "failure")
	else:
		ifInsertSuccess = insert_db('insert into User values (null, ?,?,?);',
						[username, password, phone])
		if ifInsertSuccess:
			return (True, "success")
		else:
			return (False, "failure")

def login_with_user_info(username, password, phone):
	"""
	return ifLoginSuccess: bool, errorMessage: string
	"""
	_username = query_db('select username from User where username = ?;', [username], one=True)
	if _username is None:
		return (False, "Incorrect")
	else:
		(_password, _phone) = query_db('select password, phone from User where username = ?;', [username], one=True)
		if _password != password:
			return (False, "Incorrect")
		elif _phone != phone:
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

if __name__ == "__main__":
	app.secret_key = "CS9163Assignment02WebsiteFlaskSessionSecretKey"
	app.run(debug=True)

