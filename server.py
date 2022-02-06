from flask import Flask
from flask_app import app
from flask_app.controladores import usuarios


if __name__ == "__main__":
    app.run( debug = True )