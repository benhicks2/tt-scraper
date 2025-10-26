#!/usr/bin/env python3
"""
Program: ttserver

Description: A Flask REST API server to manage table tennis equipment data stored in MongoDB.
             This is the development server. For production, use wsgi.py.

Usage: Run the included bash script to start the server.
"""
from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': os.getenv('ALLOWED_ORIGINS')}})

from routes import equipment

app.register_blueprint(equipment.dp)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

# Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
