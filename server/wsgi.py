#!/usr/bin/env python3
"""
Program: ttserver

Description: A WSGI server to run the Flask application.
"""
from app import app

if __name__ == '__main__':
    app.run()
