from flask import Flask, render_template
from redis import Redis, RedisError
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)
app = Flask(__name__, template_folder="./www/", static_folder='./www/media/')

@app.route("/")
def index():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "X"

    return render_template('index.html', visits=visits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')