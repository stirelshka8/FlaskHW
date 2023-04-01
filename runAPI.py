import test_connect
from flask import Flask, render_template

app = Flask(__name__, template_folder='template')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    if test_connect.postgres_test():
        app.run()
    else:
        raise ConnectionError("Database connection error, please check your input")
