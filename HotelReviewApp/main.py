from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)