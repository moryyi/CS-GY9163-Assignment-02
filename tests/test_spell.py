#!/usr/bin/python3
# coding: utf-8

from flask import Flask

from src.app import configure_routes

ROOT_URL = "/cs9163/hw02"


def test_spell_with_login_post():
  app = Flask(__name__, template_folder='../src/templates')
  app.secret_key = "CS9163Assignment02WebsiteFlaskSessionSecretKeyForPytestOnly"
  configure_routes(app)
  app.testing = True
  client = app.test_client()

  url = ROOT_URL + "/register"
  response = client.post(url, data={"uname": "testusername", "pword": "testpassword", "2fa": "testnumber"})
  url = ROOT_URL + "/login"
  response = client.post(url, data={"uname": "testusername", "pword": "testpassword", "2fa": "testnumber"}, follow_redirects=True)

  url = ROOT_URL + "/spell_check"
  text2check = "Take a sad sogn and make it better. Remember to let her under your (skyn),.! then you b3gin to make it betta."
  response = client.post(url, data={"inputtext": text2check})

  assert response.status_code == 200
  assert b"textout" in response.data
  assert b"misspelled" in response.data