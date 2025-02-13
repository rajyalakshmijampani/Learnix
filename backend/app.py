from application import app
from flask import Flask, request, jsonify
from flask_cors import CORS

CORS(app)


if(__name__=='__main__'):
    app.run(debug=True)