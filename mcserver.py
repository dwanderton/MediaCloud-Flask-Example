import json, ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud

api_key = os.environ.get('MCAPIKEY')
# set up logging
logging.basicConfig(level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud(api_key)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("search-form.html")


@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    if not startdate:
        startdate = datetime.date( 2017, 1, 1)
    else:
        startdate = datetime.datetime.strptime(startdate, "%Y-%m-%d")
    if not enddate:
        enddate = datetime.datetime.now()
    else:
        enddate = datetime.datetime.strptime(enddate, "%Y-%m-%d")
    results = mc.sentenceCount(keywords,
                               solr_filter=[mc.publish_date_query( startdate, enddate ),
                                            'tags_id_media:9139487'],
                                            split=True,
                                            split_start_date=startdate.strftime("%Y-%m-%d"),
                                            split_end_date=enddate.strftime("%Y-%m-%d"))

    data = []
    # print(results['split'])
    for i in results['split']:
        temp_dict = {}
        temp_dict['name'] = keywords
        temp_dict['x'] = i
        temp_dict['y'] = results['split'][i]
        data.append(temp_dict)

    return render_template("search-results.html",
                           keywords=keywords,
                           sentenceCount=results['count'],
                           results=json.dumps(data, sort_keys=True),
                           startdate=startdate.strftime("%Y-%m-%d"),
                           enddate=enddate.strftime("%Y-%m-%d"))

if __name__ == "__main__":
    app.debug = True
    app.run()
