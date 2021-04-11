from vereinswebseite import app, db
from vereinswebseite.models import Article, ArticleSchema
from flask import request, jsonify

OneArticle = ArticleSchema()
ManyArticles = ArticleSchema(many=True)


# Create Article
@app.route('/article', methods=['POST'])
def add_article():
    title = request.json['title']
    content = request.json['content']
    author = request.json['author']

    new_article = Article(title, content, author)

    db.session.add(new_article)
    db.session.commit()
    return "Article " + title + " Added"


# Get all Articles
@app.route('/article', methods=['GET'])
def get_all_articles():
    all_articles = Article.query.all()
    result = jsonify(ManyArticles.dump(all_articles))
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


# Get one Article
@app.route('/article/<article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get(article_id)
    result = OneArticle.jsonify(article)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result
