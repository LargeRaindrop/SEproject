from flask import Flask, render_template, jsonify
from random import *
import requests
# cors用到的库
from flask_cors import CORS
# Build后网页存放的位置
app = Flask(__name__,
static_folder = "./dist/static",
template_folder = "./dist")
# 下面这句可以保证前端正常使用后端的api
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

# 添加新的后端api时添加在下面
@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

