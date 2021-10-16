import flask
import csv

from final_demographic import output
from final_content_based import getRecomm

with open('proccessed.csv', newline = '', encoding='utf8') as f:
    reader = list(csv.reader(f))
    all_articles = reader[1:]

for i in range(len(all_articles)):
    del all_articles[i][0]

app = flask.Flask(__name__)

liked = []
dis_liked = []

@app.route('/all-articles')
def getAllArticles():
    movie_data = {
        "url": all_articles[0][9],
        "title": all_articles[0][10],
        "text": all_articles[0][11],
        "lang": all_articles[0][12],
        "total_events": all_articles[0][13]
    }
    return flask.jsonify({
        'data': movie_data,
        'message': 'success'
    }), 200

@app.route('/liked-articles', methods = ["POST"])
def likedArticles():
    article = all_articles[0]
    liked.append(article)
    all_articles.pop(0)
    print(liked)
    return flask.jsonify({
        'status': 'success'
    }), 200

@app.route('/disliked-articles', methods = ["POST"])
def dislikedArticles():
    article = all_articles[0]
    dis_liked.append(article)
    all_articles.pop(0)
    return flask.jsonify({
        'status': 'success'
    }), 200


@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        data = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        article_data.append(data)
    return flask.jsonify({
        "data": article_data,
        "status": "success"
    }), 200


@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked:
        output = getRecomm(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = [all_recommended for all_recommended, _ in itertools.groupby(all_recommended)]
    article_data = []
    for recommended in all_recommended:
        data = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(data)
    return flask.jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)