from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from flask import Response
from flask import jsonify
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from py_pkg.MakeWordCloud import Word_Cloud

import json
import os

from py_pkg.tfidf import TF_IDF
from py_pkg.crawling import Crawling
from py_pkg.cosinesimilarity import CosineSimilarity
from py_pkg.dbtocsv import ToCsv
from py_pkg.es import ES
from elasticsearch import Elasticsearch


es_host=os.environ['ELASTICSEARCH_URL']; es_port='9200'
es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
es.indices.delete(index='urls', ignore=[400,404])

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload/File', methods=['GET', 'POST'])
def uploadFile():
    error = None
    if request.method == 'GET':
        url = request.args.get('url')
        id = request.args.get('id')
        crawling_url = Crawling(url,id, es_host, es_port)
        result = crawling_url.word_processing()
        print(result)

        return json.dumps(result)
		
	

@app.route('/analysis/tfidf', methods=['GET'])
def tfidfAnalysis() :
    error = None
    if request.method == 'GET' :
        url = request.args.get('url')
        Elastic=ES(es_host, es_port)
        entire_wordfreq=Elastic.get_wordfrequency_by_url()
        tf=TF_IDF(url, entire_wordfreq)

        lstWord=[]; lstPercent = []
        top10=tf.get_Top10_TFIDF_words()
        for word in top10:
            lstWord.append(word[0])
            lstPercent.append(word[1])
        returnResult = {
            "word":lstWord,
            "percent":lstPercent
        }
        return json.dumps(returnResult)


@app.route('/analysis/cosineSimilarity', methods=['GET'])
def cosineSimilariyAnaylsis() :
    error = None
    if request.method == 'GET':
        url = request.args.get('url')
        Elastic=ES(es_host, es_port)
        entire_wordfreq=Elastic.get_wordfrequency_by_url()
        url_lst=[]; sm_lst=[]
        top3=CosineSimilarity().get_Top3_ConsineSimilarity(url, entire_wordfreq)
        for url in top3:
            url_lst.append(url[0])
            sm_lst.append(url[1])
        returnResult = {
            "url":url_lst,
            "percent":sm_lst
        }
        return json.dumps(returnResult)



@app.route('/make/wordcloud', methods=['GET'])
def make_cloud_image():
    error = None
    if request.method == 'GET' :
        url = request.args.get('url')
        wd=Word_Cloud(url,es_host, es_port).make_cloud_image()
        fig=plt.figure(figsize=(10,10))
        plt.imshow(wd)
        plt.axis("off")
        fname= url.split("//")[1].split(".")[0] + ".png"
        fig.savefig("static/image/"+fname)
        plt.close()
        returnResult = {
            "fname":fname
        }
        return json.dumps(returnResult)


@app.route('/down/csv')
def down_csv():
    inst=ToCsv(es_host, es_port, "./static/csv/db.csv")
    df=inst.toCsv()
    returnResult = {
        "fname":"../static/csv/db.csv"
    }
    return json.dumps(returnResult)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')