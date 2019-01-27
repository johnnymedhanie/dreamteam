from flask import Flask
from yelp.client import Client
import json
import requests
from collections import defaultdict
from pprint import pprint
from flask import request


app = Flask(__name__)
#
# keyword_map = {
#     {"location":"vancouver"}, # where are you planning to go
#     {"interest" : ["hiking", "snowboarding", "chocolate"]},
#     {"time" : {"10:AM", "7:PM"}} # what do you like to do
# }

#
def foodParser(*foods):
    return {}



def create_querystring(*survey_answers):
    querystring = defaultdict(str)
    for ans in survey_answers:
        keyword_map[ans]


@app.route('/')
def main():
    print("this is req data", request.data)
    choices = request.get_json()

    cuisine = choices['cuisine']
    price = choices['price']


    print(request.get_json())
    print("cuisine is: ", cuisine)


    url = "https://api.yelp.com/v3/businesses/search"
    location = ""

    querystring = {"term":cuisine, "location":"vancouver"}
    payload = ""
    headers = {
    'Authorization': "Bearer TcTzRvNstk-8bdJkDiY3mwUhcCraFKD1SERukD6IxsOIiyN_pbbdmzb1JQdcCig0YYqECwWYEMB5YAD-8Z_XXso0MHOz47jJGqrH3S_t0L1V_frSvWq0jzsP1_5MXHYx",
    'cache-control': "no-cache",
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    #
    # print(pprint(response.json()))
    # print(type(response))

    return str(["{}\n".format(line) for line in json.dumps(response.json()).split(",")])

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
