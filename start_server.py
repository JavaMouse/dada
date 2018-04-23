from time import sleep

from flask import Flask,render_template

from Utils.DBUtils import mysql_coon_pool as pool

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",name="tianbohao")

@app.route("/user/<name>")
def hello(name):
    db = pool.get_db_coon()
    sleep(10)
    pool.close(db)
    return "hello %s" % name

if __name__ == '__main__':
    app.run()
