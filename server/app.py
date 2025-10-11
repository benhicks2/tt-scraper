#!/usr/bin/env python3
"""
Program: ttserver

Description: A Flask REST API server to manage table tennis equipment data stored in MongoDB.

Usage: Run the included bash script to start the server.
"""
from flask import Flask
from flask_cors import CORS
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
cors = CORS(app, resources={r'/*': {'origins': config['database']['ALLOWED_ORIGINS']}})

from routes import equipment

app.register_blueprint(equipment.dp)
