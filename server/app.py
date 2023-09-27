#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, abort
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.before_request
def before_request():
    if 'page_views' not in session:
        session['page_views'] = 0

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):

    article = Article.query.filter_by(id=id).first()
    session['page_views'] += 1
    if session['page_views'] > 3:
        res_body = {'message': 'Maximum pageview limit reached'}
        response = make_response(jsonify(res_body), 401)
        return response
        #abort(401, description='You have exceeded the maximum number of viewed articles.')
    else:
        response_body = {
            "id": article.id,
            "author": article.author,
            "title": article.title,
            "content": article.content,
            "preview": article.preview,
            "minutes_to_read": article.minutes_to_read,
            "date": article.date
        }
        response = make_response(jsonify(response_body), 200)
        return response

#@app.errorhandler(401)
#def unauthorized(e):
    #return {'error': str(e)}, 401


if __name__ == '__main__':
    app.run(port=5555)
