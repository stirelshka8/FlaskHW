import os

from flask import Flask, render_template, url_for
import test_connect
import advert
import users

app = Flask(__name__, template_folder='template')
app.secret_key = 'Jc({@~Q,^E*[xGx~;[_<i@XwU*=9F<EB8LBf:4_=oeG939NRoR_b`7Tv`X@@#R'
app.register_blueprint(advert.bp)
app.register_blueprint(users.bp)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='image/favicon.ico')


if __name__ == '__main__':
    if test_connect.postgres_test():
        app.run(port=5051)
    else:
        raise ConnectionError("Database connection error, please check your input")
