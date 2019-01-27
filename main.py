from flask import Flask
from yelp.client import Client
import json
import requests
from collections import defaultdict
from pprint import pprint
from flask import request


app = Flask(__name__)
#
keyword_map = {
    "Q1":{"location":"vancouver"}, # where are you planning to go
    "Q2":{"interest" : ["hiking", "snowboarding", "chocolate"]},
    {"time" : {"10:AM", "7:PM"}} # what do you like to do
}


def foodParser(*foods):
    return {}



def filter_results(response):
    """ given a response object's json, filter out and select a few for itinerary
    @param response: Response object containing json data from get request to yelp api
    return: a list of dictionary where the list is a list of scheduled activities, and the dictionary contains information for each activity
    """


    return []

def create_querystring(survey_answers):
    """

    :param survey_answers: a list of all survey answers as keywords to querystring
    :return:
    """
    querystring = {}
    for ans in survey_answers:
        querystring.update(ans)

    return querystring


@app.route('/')
def main():
    print("this is req data", request.data)
    choices = request.get_json() # yelp keywords that we can use in query string

    querystring = create_querystring(choices)
    url = "https://api.yelp.com/v3/businesses/search"

    # querystring = {"term":"asian,chinese","location":"vancouver","radius":7, "price":"1, 2, 3"}
    headers = {
    'Authorization': "Bearer TcTzRvNstk-8bdJkDiY3mwUhcCraFKD1SERukD6IxsOIiyN_pbbdmzb1JQdcCig0YYqECwWYEMB5YAD-8Z_XXso0MHOz47jJGqrH3S_t0L1V_frSvWq0jzsP1_5MXHYx",
    'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    itinerary_objects = filter_results(response)
    #
    return itinerary_objects
    # pprint(response.json())
    # print(type(response))

    # return str(["{}\n".format(line) for line in json.dumps(response.json()).split(",")])

#
#
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# r.status_code
# r.headers['content-type']
# 'application/json; charset=utf8'
#
# r.text
# r.json()
# {u'private_gists': 419, u'total_private_repos': 77, ...}
