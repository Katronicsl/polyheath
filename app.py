from flask import Flask, render_template, request
from flask_login import login_required, current_user
from database import db, login_manager
from routes.auth import auth
from routes.tests import tests
from routes.articles import articles, REVERSE_ARTICLE_MAP, ARTICLE_SLUG_MAP
from models import User, Favorite, TestResult


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/site"

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(tests)
app.register_blueprint(articles)


@app.route('/')
def home():
    home_articles = [
        {
            "title": "Гигиена сна",
            "desc": "7 правил здорового сна собраны для вас в одной статье.",
            "image": "catsleep.jpg",
            "url": "/article/depression"
        },
        {
            "title": "Стресс и здоровье",
            "desc": "Стресс может стать причиной серьезных проблем со здоровьем. В статье — 10 простых советов, которые помогут справиться с напряжением и сохранить душевное равновесие.",
            "image": "stress.png",
            "url": "/article/stress",
        },
        {
            "title": "Отказ от курения",
            "desc": "Простые советы, которые помогут избавиться от никотиновой зависимости и улучшить качество жизни.",
            "image": "smoking.png",
            "url": "/article/smoking"
        }
    ]

    return render_template('glavnaya.html', home_articles=home_articles)


@app.route('/profile')
@login_required
def profile():
    favorites_raw = Favorite.query.filter_by(user_id=current_user.id).all()
    test_results = TestResult.query.filter_by(user_id=current_user.id).all()

    favorites = []
    for fav in favorites_raw:
        if fav.article in REVERSE_ARTICLE_MAP:
            title = REVERSE_ARTICLE_MAP[fav.article]
            slug = fav.article
        elif fav.article in ARTICLE_SLUG_MAP:
            title = fav.article
            slug = ARTICLE_SLUG_MAP[fav.article]
        else:
            title = fav.article
            slug = fav.article

        favorites.append({"title": title, "slug": slug})

    return render_template('profile.html', favorites=favorites, tests=test_results)


@app.route('/navigatortests')
def navigatortests():
    q = request.args.get('q', '').strip()

    tests_list = [
        {
            "title": "Тест на качество сна",
            "desc": "Оцените своё эмоциональное состояние, уровень апатии, усталости и психологической нагрузки.",
            "image": "catsleep.jpg",
            "url": "/test/sleep/0",
            "tags": ["Здоровый сон", "Распорядок дня"]
        },
        {
            "title": "Тест на уровень стресса",
            "desc": "Пройдите тест и узнайте, насколько стресс влияет на ваше самочувствие и здоровье.",
            "image": "stress.png",
            "url": "/test/stress/0",
            "tags": ["Управление стрессом", "Самочувствие"]
        },
        {
            "title": "Тест Фагерстрема (оценка степени никотиновой зависимости)",
            "desc": "Оцените свою зависимость от никотина с помощью теста Фагерстрема.",
            "image": "smoking.png",
            "url": "/test/smoking/0",
            "tags": ["ЗОЖ", "Привычки"]
        }
    ]

    if q:
        filtered_tests = [
            test for test in tests_list
            if q.lower() in test["title"].lower()
        ]
    else:
        filtered_tests = tests_list

    return render_template(
        'navigatortests.html',
        tests_list=filtered_tests,
        q=q
    )


@app.route('/navigatorarticle')
def navigatorarticle():
    q = request.args.get('q', '').strip()

    articles_list = [
        {
            "title": "Гигиена сна",
            "desc": "7 правил здорового сна собраны для вас в одной статье. Узнайте, как улучшить качество ночного отдыха и спите с удовольствием!",
            "image": "catsleep.jpg",
            "url": "/article/depression",
            "tags": ["Здоровый сон", "Распорядок дня"]
        },
        {
            "title": "Стресс и здоровье",
            "desc": "Стресс может негативно влиять на здоровье — узнайте простые способы справиться с ним и сохранить внутреннее равновесие.",
            "image": "stress.png",
            "url": "/article/stress",
            "tags": ["Управление стрессом", "Здоровый образ жизни"]
        },
        {
            "title": "Отказ от курения",
            "desc": "Простые советы, которые помогут избавиться от никотиновой зависимости и улучшить качество жизни.",
            "image": "smoking.png",
            "url": "/article/smoking",
            "tags": ["ЗОЖ", "Отказ от курения"]
        },
    ]

    if q:
        filtered_articles = [
            article for article in articles_list
            if q.lower() in article["title"].lower()
        ]
    else:
        filtered_articles = articles_list

    return render_template(
        'navigatorarticle.html',
        articles=filtered_articles,
        q=q
    )

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)