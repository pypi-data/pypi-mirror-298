from flask import Config, Flask, flash, redirect, render_template, request, url_for
from flask_crud.dbutil import DBController
from flask_mysqldb import MySQL
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
DBController.mysql = mysql

login_manager = LoginManager()
login_manager.init_app(app)

class Usuario:
    def __init__(self, *args) -> None:
        pass
@app.route("/perfil")
@login_required
def perfil():
    return f"Usuario logueado: {current_user.toStr()}"

@login_manager.user_loader
def load_user(user_id):
    user = Usuario.getById(user_id)
    return Usuario(user)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Usuario.login(username, password)
        user = Usuario(user)
        print(user)
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))