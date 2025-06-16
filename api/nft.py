from flask import Blueprint, request, jsonify, session, redirect, render_template, url_for, flash
from services.nft_generator import generate_image
from crud.nft_crud import *
from database import SessionLocal

bp = Blueprint('nft', __name__, url_prefix='/nft')

@bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    db = SessionLocal()
    # Получить все картинки всех пользователей с их username
    images = get_all_nft_images_with_users(db)
    db.close()
    for img in images:
        img["image_url"] = url_for('static', filename='generated/' + img["filename"])
    return render_template("dashboard.html", images=images)

@bp.route("/generate", methods=["POST", "GET"])
def generate_nft():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if "nft_id" in request.form:
            # Это попытка переименовать уже существующую NFT
            nft_id = int(request.form["nft_id"])
            new_title = request.form["title"].strip()
            db = SessionLocal()
            nft = update_nft_title(db, nft_id, session["user_id"], new_title)
            db.close()
            if nft:
                flash("Название сохранено!")
                return redirect(url_for("nft.nft_result", nft_id=nft.id))
            else:
                flash("Ошибка при сохранении названия.", "error")
                return redirect(url_for("nft.dashboard"))
        else:
            # Это генерация новой NFT через POST (если вдруг что-то отправили)
            filename, layers, auto_title = generate_image()
            db = SessionLocal()
            nft = create_nft_image(db, session["user_id"], filename, layers, auto_title)
            db.close()
            return redirect(url_for("nft.nft_result", nft_id=nft.id))
    else:
        # GET: сразу генерируем и редиректим на результат, как раньше
        filename, layers, auto_title = generate_image()
        db = SessionLocal()
        nft = create_nft_image(db, session["user_id"], filename, layers, auto_title)
        db.close()
        return redirect(url_for("nft.nft_result", nft_id=nft.id))

@bp.route("/nft/<int:nft_id>", methods=["GET"])
def nft_result(nft_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    db = SessionLocal()
    nft = get_nft_by_id(db, nft_id, session["user_id"])
    db.close()
    if not nft:
        flash("NFT не найден.")
        return redirect(url_for("nft.dashboard"))
    image_url = url_for('static', filename='generated/' + nft.filename)
    return render_template("nft_result.html", nft=nft, image_url=image_url)


@bp.route("/history", methods=["GET", "POST"])
def nft_history():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    db = SessionLocal()
    if request.method == "POST":
        nft_id = int(request.form["nft_id"])
        new_title = request.form["title"].strip()
        update_nft_title(db, nft_id, session["user_id"], new_title)
        db.close()
        flash("Название обновлено!")
        return redirect(url_for("nft.nft_history"))
    images = get_user_nft_images(db, session["user_id"])
    db.close()
    for img in images:
        img.image_url = url_for('static', filename='generated/' + img.filename)
    return render_template("nft_history.html", images=images)