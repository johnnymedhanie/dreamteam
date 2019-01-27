from flask import Flask, render_template, url_for, redirect
from yelp.client import Client
import json
import requests
from collections import defaultdict
from pprint import pprint
from flask import request


app = Flask(__name__)
#
url = "https://api.yelp.com/v3/businesses/search"

# querystring = {"term":"asian,chinese","location":"vancouver","radius":7, "price":"1, 2, 3"}
headers = {
    'Authorization': "Bearer TcTzRvNstk-8bdJkDiY3mwUhcCraFKD1SERukD6IxsOIiyN_pbbdmzb1JQdcCig0YYqECwWYEMB5YAD-8Z_XXso0MHOz47jJGqrH3S_t0L1V_frSvWq0jzsP1_5MXHYx",
    'cache-control': "no-cache",
}

keyword_map = {
    "Q1":{"location":"vancouver"}, # where are you planning to go
    "Q2":{"interest" : ["hiking", "snowboarding", "chocolate"]},
    "time" : {"10:AM", "7:PM"} # what do you like to do
}


#
def foodParser(*foods):
    return {}



def filter_results(response):
    """ given a response object's json, filter out and select a few for itinerary
    @param response: Response object containing json data from get request to yelp api
    return: a list of dictionary where the list is a list of scheduled activities, and the dictionary contains information for each activity
    """

    # print(response.text)
    response_json = response.text
    response = json.loads(response_json)
    return response['businesses'][0]["id"]

def create_querystring(survey_answers):
    """

    :param survey_answers: a list of all survey answers as keywords to querystring
    :return:
    """
    querystring = {}
    for ans in survey_answers:
        querystring.update(ans)
    print(querystring)
    return querystring


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # replace this with an insert into whatever database you're using
        print("this is req data", request.data)
        choices = request.get_json()  # yelp keywords that we can use in query string
        choices = [{"term": "asian"}, {'limit':2},{"location": "vancouver", "price": "1, 2, 3"}]

        querystring = create_querystring(choices)


        # querystring = create_querystring(request.args) #query yelp api
        response = requests.request("GET", url, headers=headers, params=querystring)
        print("response")
        itinerary_objects = filter_results(response) #filter yelp api results
        # return render_template("index.html")
        print("IASDKAJSFLKASJFLKFJLASKFJ")
        print(itinerary_objects)
        return redirect(url_for('display_itinerary', itinerary_objects=itinerary_objects))
        # return redirect(url_for('display_itinerary', itinerary_objects="asdasf"))

    else:
        return render_template("index.html")

@app.route('/schedule/<string:itinerary_objects>', methods=['GET', 'POST'])
def display_itinerary(itinerary_objects):
    errors = []
    # if request.method == "POST":
    #     # get url that the person has entered
    #     try:
    #         url = request.form['url']
    #         r = requests.get(url)
    #     except:
    #         errors.append(
    #             "Unable to get URL. Please make sure it's valid and try again."
    #         )
    #         return render_template('schedule.html', errors=errors)
    #     if r:
    #         return render_template("schedule.html", itinerary_objects=itinerary_objects)
    return render_template("schedule.html", itinerary_objects=itinerary_objects)



#    return itinerary_objects
    # pprint(response.json())
    # print(type(response))

    # return str(["{}\n".format(line) for line in json.dumps(response.json()).split(",")])

