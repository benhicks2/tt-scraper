#!/usr/bin/env python3
"""
Program: ttserver

Description: A Flask REST API server to manage table tennis equipment data stored in MongoDB.

Usage: Run the included bash script to start the server.
"""
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

from routes import equipment

app.register_blueprint(equipment.dp)
