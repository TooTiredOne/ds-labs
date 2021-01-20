from flask import Flask, render_template, url_for
app = Flask(__name__, template_folder="./www/", static_folder='./www/media/')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/facts")
def facts():
    return render_template("facts.html")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)