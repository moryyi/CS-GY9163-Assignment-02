# CS-GY9163-Assignment-02

[![Build Status](https://travis-ci.org/qb1ng/CS-GY9163-Assignment-02.svg?branch=master)](https://travis-ci.org/qb1ng/CS-GY9163-Assignment-02)

Repo for CS9163 Assignment 02

## Spell-Check Website
This website is developed with Flask, Python3, and Bootstrap.

Register, login into the website, and submit text for spell-checking.

## Install required dependencies
- Install requirements with pip

  ```sh
  pip3 install -r requirements.txt
  ```
  
## Test with pytest
- To test the service with pytest, enter the root folder of this project

  ```sh
  export PYTHONPATH="$PYTHONPATH:$PWD"
  pytest
  ```

## Start the service
- To start this Flask application
- On win10 with WSL Ubuntu:
  ```sh
  chmod +x app.py
  ./app.py
  ```

- On Ubuntu 18 Virtual Machine with Flask command:
  ```sh
  flask run
  ```

## How to use
1. Open the browser and enter URL http://127.0.0.1:5000/cs9163/hw02/
2. The URLs available are:
   1. home: http://127.0.0.1:5000/cs9163/hw02/ &larr; redirect to login page
   2. login: http://127.0.0.1:5000/cs9163/hw02/login
   3. register: http://127.0.0.1:5000/cs9163/hw02/register
   4. spell check: http://127.0.0.1:5000/cs9163/hw02/spell_check &larr; require user login

## References
Some of the source codes are learnt from this Flask project Tutorial [Youtube Video](https://www.youtube.com/watch?v=d04xxdrc7Yw).
