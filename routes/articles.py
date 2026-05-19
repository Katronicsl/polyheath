from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from models import Favorite
from database import db

articles = Blueprint("articles", __name__)

ARTICLE_SLUG_MAP = {
    "Здоровый сон": "depression",
    "Стресс и здоровье": "stress",
    "Вред курения": "smoking",
}

REVERSE_ARTICLE_MAP = {slug: title for title, slug in ARTICLE_SLUG_MAP.items()}


def _normalize_article_input(article):
    if article in ARTICLE_SLUG_MAP:
        return ARTICLE_SLUG_MAP[article]
    if article in REVERSE_ARTICLE_MAP:
        return article
    return article


@articles.route("/article/<article>")
def article_page(article):
    is_favorited = False
    if current_user.is_authenticated:
        slug = _normalize_article_input(article)
        is_favorited = Favorite.query.filter_by(user_id=current_user.id, article=slug).first() is not None
    return render_template(f"article/{article}.html", is_favorited=is_favorited, article_name=article)


@articles.route("/favorite/<article>")
def favorite(article):
    if not current_user.is_authenticated:
        return render_template("login_prompt.html", next=url_for("articles.favorite", article=article))

    slag = _normalize_article_input(article)

    existing_fav = Favorite.query.filter_by(user_id=current_user.id, article=slag).first()
    if existing_fav:
        flash("Эта статья уже в вашем избранном!", "info")
        return redirect(url_for("profile"))

    fav = Favorite(
        user_id=current_user.id,
        article=slag
    )
    db.session.add(fav)
    db.session.commit()
    flash("Статья добавлена в избранное!", "success")

    return redirect(url_for("profile"))

#@articles.route('/article/stress')
#def stress_article():
 #   return render_template('article/stress.html')

#@articles.route('/article/smoking')
#def smoking_article():
 #   return render_template('article/smoking.html')