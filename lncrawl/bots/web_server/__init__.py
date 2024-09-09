from .flask import app

__all__ = ['flask app']


def run_server():
    app.run()