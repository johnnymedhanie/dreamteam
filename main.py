from flask import Flask, render_template, url_for, redirect
from yelp.client import Client
import json
import requests
from pprint import pprint
from flask import request
from datetime import datetime
from random import randint


app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
#
url = "https://api.yelp.com/v3/businesses/search"

# querystring = {"term":"asian,chinese","location":"vancouver","radius":7, "price":"1, 2, 3"}
headers = {
    'Authorization': "Bearer TcTzRvNstk-8bdJkDiY3mwUhcCraFKD1SERukD6IxsOIiyN_pbbdmzb1JQdcCig0YYqECwWYEMB5YAD-8Z_XXso0MHOz47jJGqrH3S_t0L1V_frSvWq0jzsP1_5MXHYx",
    'cache-control': "no-cache",
}


def filter_activity_results(response):
    """ given a response object's json, filter out and select a few for itinerary
    @param response: Response object containing json data from get request to yelp api
    return: a list of dictionary where the list is a list of scheduled activities, and the dictionary contains information for each activity
    """

    # print(response.text)
    response_json = response.text
    response = json.loads(response_json)
    rng_activity = randint(0, len(response)-1)
    selected_activity = response["businesses"][rng_activity]  # TODO: improve selection
    print('AHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHHAHHHHHHHH')

    activities = {
        selected_activity["name"]:{
                "image_url": selected_activity["image_url"],
                "address": ','.join([item for item in selected_activity["location"]["display_address"]]),
                "time_duration": "2:00pm-4:30pm",  # TODO: change this so it is not hardcoded when have more time
                "description": "{}".format(selected_activity["name"])
        }
    }

    return activities

    # return response
    # return response['businesses'][0]["alias"]


def filter_food_results(response):
    """ given a response object's json, filter out and select a few for food
    @param response: Response object containing json data from get request to yelp api
    return: a list of dictionary where the list is a list of scheduled activities, and the dictionary contains information for each activity
    """

    # print(response.text)
    response_json = response.text
    response = json.loads(response_json)
    #select randomly from top 10
    rng_lunch = randint(0,len(response))
    selected_lunch_restaurant = response["businesses"][rng_lunch] #TODO: improve selection
    rng_dinner = randint(0,len(response))
    # while rng_dinner==rng_lunch:
    #     rng_dinner = randint(0, len(response))
    selected_dinner_restaurant = response["businesses"][rng_dinner] #TODO: improve selection
    # keywords that we need from response
    meals = {
        "lunch":{
            "image_url": selected_lunch_restaurant["image_url"],
            "address": ','.join([item for item in selected_lunch_restaurant["location"]["display_address"]]),
            "time_duration": "12:00pm-1:30pm",  # TODO: change this so it is not hardcoded when have more time
            "description": "Lunch at {}".format(selected_lunch_restaurant["name"])
        },
        "dinner":{
            "image_url": selected_dinner_restaurant["image_url"],
            "address": ','.join([item for item in selected_dinner_restaurant["location"]["display_address"]]),
            "time_duration": "5:00pm-6:30pm",  # TODO: change this so it is not hardcoded when have more time
            "description": "Dinner at {}".format(selected_dinner_restaurant["name"])
        }
    }

    print("FOOD")
    print(meals)
    return meals
    # return response['businesses'][0]["alias"]


def parse_survey_form(survey_form):
    """

    :param survery_answers:
    :return:
    """
    print(survey_form)


def get_activity_open_interval(departure_time, return_time, time_spent_per):
    """
    given a departure time, return time, and a guess at how long the user would like to spend at each location,
    figure out a range of times to check what places are open at.

    Eg. departure at 10am, return at 2pm, user likes to pack as many things as possible - usually 1-2 hours at each place
    Therefore, when querying for activities, activities should be queried whether they are open at 10,11,12pm,1pm,2pm

    :param departure_time:
    :param return_time:
    :param time_spent_per:
    :return: a list of integers representing unix time in same timezone as query that should be queried
    """

    return []


def get_food_open_interval(departure_time, return_time, time_spent_per):
    """
    given a departure time, return time, and a guess at how long the user would like to spend at each location,
    figure out a range of times to check what places are open at.
    assumes:
    breakfast is 6-10am
    lunch is 12-2pm
    dinner is 5-8pm

    Eg. departure at 10am, return at 2pm, user likes to pack as many things as possible - usually 1-2 hours at each place
    Therefore, when querying for activities, activities should be queried whether they are open at 10,11,12pm,1pm,2pm

    :param departure_time:
    :param return_time:
    :param time_spent_per:
    :return: a list of integers representing unix time in same timezone as query that should be queried
    """
    time_format = "%H:%M"
    depart_time = datetime.strptime(departure_time, time_format)
    ret_time = datetime.strptime(return_time, time_format)


    return []


def create_activity_querystring(survey_form):
    print("we got to activity")
    querystring = {}
    querystring["location"] = survey_form["location"]
    querystring["price"]=survey_form["activityBudget"]

    querystring["categories"] = ""
    if survey_form["intoBeer"]=="True":
        print("CORRECT WE WENT IN")
        querystring["categories"] = "bars,breweries,wineries,adultentertainment,social_clubs,"
    if survey_form["intoRNR"]=="True":
        querystring["categories"]+= "skincare,medicalspa,"
    if survey_form["intoCooking"]=="True":
        querystring["categories"]+= "restaurants,tastingclasses,gourmet,"
    if survey_form["intoMusic"]=="True":
        querystring["categories"]+= "festivals,"
    if survey_form["intoFamFriendly"]=="True":
        querystring["categories"]+= "artclasses,movietheaters,farms,zoos,"
    if survey_form["intoCulture"]=="True":
        querystring["categories"]+= "museums,tours,artsandcrafts,"
    if survey_form["intoOutdoors"]=="True":
        querystring["categories"]+= "active,fitness,parks,"
    querystring["categories"] = querystring["categories"].strip(",")
    querystring["sort_by"]="best_match"
    return querystring


def create_food_querystring(survey_form):
    """

    :param survey_form: a form containing all survey answers and outputs dictionary  of
    keywords:values to use as querystring for yelp api
    :return:
    """

    querystring = {}
    querystring["location"] = survey_form["location"]
    querystring["term"] = survey_form["cuisine"]
    open_interval = get_food_open_interval(survey_form["departureTime"], survey_form["homeTime"], "howtotravel")
    # querystring["term"] = "korean"
    querystring["price"]=survey_form["food-budget"]
    print(survey_form.keys())

    # vancouver 1. Japadog
    # vancouver 2. Medina Cafe
    # vancouver 3. Miku
    # vancouver 4. bluewater cafe
    # for ans in survey_form:
    #     querystring.update(ans)
    # print(querystring)
    querystring["sort_by"]="rating"

    return querystring


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        print("this is req is form data", request.form['location'])
        # use for debugging form fields

        # from flask import jsonify
        # return jsonify(request.form)

        food_querystring = create_food_querystring(request.form)
        food_response = requests.request("GET", url, headers=headers, params=food_querystring)
        #
        # from flask import jsonify
        # return jsonify(food_response.json())

        activity_querystring = create_activity_querystring(request.form)
        print(activity_querystring)
        activity_response = requests.request("GET", url, headers=headers, params=activity_querystring)
        # print("response")
        # from flask import jsonify
        # return jsonify(activity_response.json())


        itinerary_activity_objects = filter_activity_results(activity_response) #filter yelp api results
        itinerary_food_objects = filter_food_results(food_response)

        # from flask import jsonify
        # return jsonify(itinerary_food_objects)
        # return jsonify(itinerary_activity_objects)
        # return render_template("index.html")

        # print(itinerary_objects)


        content = {"activity":itinerary_activity_objects,
                   "food":itinerary_food_objects}
        import urllib
        content = urllib.urlencode(content)
        print('pls', content)
        return redirect(url_for('display_itinerary', content=content))
        # return redirect(url_for('display_itinerary', itinerary_objects="asdasf"))
    else:
        return render_template("survey.html", content={})

@app.route('/schedule/<content>', methods=['GET', 'POST'])
def display_itinerary(content):
    # print('YEEEEEE')
    # print(content)
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
    # import ast
    # content=ast.literal_eval(content)
    # print('AHHHHHHH')
    # print(content)
    import urlparse
    import ast
    content = urlparse.parse_qs(content)
    # print('quick moves')
    content['food'][0] = ast.literal_eval(content['food'][0])
    content['activity'][0] = ast.literal_eval(content['activity'][0])
    return render_template("initerary.html", content=content)



#    return itinerary_objects
    # pprint(response.json())
    # print(type(response))

    # return str(["{}\n".format(line) for line in json.dumps(response.json()).split(",")])
