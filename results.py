import urllib.request
import json
import requests
from config import Config
import datetime
from peewee import *
from models import *
from pytz import timezone
import pytz

hosts = ["albertk"]

def convert_pst(Y,M,D,H):
    pacificTZ = timezone("US/Pacific")
    datePacific = pacificTZ.localize(datetime(Y,M,D,H,0,0,0), is_dst=None)
    dateEpoch = (datePacific - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return dateEpoch

fest_start = convert_pst(2019,8,10,10)
fest_end = convert_pst(2019,8,11,10)


def record_data():
    print('hi')

def open_data():
    with open("battle.json") as json_file:
        data = json.load(json_file)
        return data

def get_splatnet(username,older=None):
    url = "https://stat.ink/api/v2/battle"
    parameters = {
        'screen_name':username,
        'count':50
        }
    if older:
        parameters.update({'older_than':older})
    print(parameters)
    response = requests.get(url, params=parameters)
    data = json.loads(response.text)
    data = json.loads(url)    
    return data


def get_matches(username,fest_start,fest_end):    
    #### this chunk is for getting the data on the web, disabled to be nice during development
    # data = get_splatnet(username)


    # used for local parsing... development only ####
    data = open_data()

    for match in data:
        print('this many players')
        players = match['players']
        print(len(players))
        matchtime = match['start_at']['time']
        if matchtime < fest_end and matchtime > fest_start:
            record_data()
    end_of_match_batch = data[-1]
    last_start = end_of_match_batch['start_at']['time']
    oldest_id = end_of_match_batch['id']

    if last_start > fest_start:
        print('need to get more matches')
        get_splatnet(username,oldest_id)
            # get_next_batch()
        # return(data)
matches = get_matches("albertk",fest_start,fest_end)
