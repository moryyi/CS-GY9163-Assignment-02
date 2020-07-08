#!/usr/bin/python3
# coding: utf-8

from flask import Flask

from src.app import configure_routes

ROOT_URL = "/cs9163/hw02"

def test_home_route():
  app = Flask(__name__, template_folder='../src/templates')
  configure_routes(app)
  app.testing = True
  client = app.test_client()

  url = ROOT_URL + "/"
  response = client.get(url)
  # code 302 -> redirect
  assert response.status_code == 302


def test_login_route():
  app = Flask(__name__, template_folder='../src/templates')
  configure_routes(app)
  app.testing = True
  client = app.test_client()

  url = ROOT_URL + "/login"
  response = client.get(url)
  assert response.status_code == 200


def test_register_route():
  app = Flask(__name__, template_folder='../src/templates')
  configure_routes(app)
  app.testing = True
  client = app.test_client()

  url = ROOT_URL + "/register"
  response = client.get(url)
  assert response.status_code == 200