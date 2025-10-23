from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask 环境已配置成功！"

if __name__ == '__main__':
    app.run(debug=True)
