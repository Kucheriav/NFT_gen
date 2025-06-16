from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from crud.user_crud import get_user_by_username, create_user
from database import SessionLocal

bp = Blueprint('auth', __name__)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = SessionLocal()
        if get_user_by_username(db, username):
            flash("Пользователь уже существует")
            db.close()
            return redirect(url_for("auth.register"))
        create_user(db, username, generate_password_hash(password))
        flash("Успешная регистрация! Войдите.")
        db.close()
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = SessionLocal()
        user = get_user_by_username(db, username)
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            db.close()
            return redirect(url_for("nft.dashboard"))
        flash("Неверный логин или пароль")
        db.close()
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("Вы вышли из системы")
    return redirect(url_for("auth.login"))