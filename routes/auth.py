from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))  

        else:
            error = "Неверное имя пользователя или пароль."

    return render_template("login.html", error=error)


@auth.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(password) < 7:
            error = "Пароль должен содержать минимум 7 символов."

        elif User.query.filter_by(username=username).first():
            error = "Пользователь с таким именем уже существует."

        else:
            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            login_user(user)

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))

    return render_template("register.html", error=error)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))