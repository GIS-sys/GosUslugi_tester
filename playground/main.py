from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return """<div><p><span class="a b">QQQ</span><span class="a c">WWW</span></p></div>"""

if __name__ == "__main__":
    app.run(port=8080)

