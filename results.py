
# import urllib.request
# make sure you have these modules: json, requests, peewee, pytz, pandas
import json
import requests
import datetime
from peewee import *
from pytz import timezone
import pytz
from datetime import datetime
import csv
import os

import pandas as pd
from collections import defaultdict

# used for live database connections
from config import Config
from models import *

# these are the hosts user name in splatoon!
hosts = ["Lizmo","albertk","Teeze#8222","◇.◆'"]

# host's name on stat_net!
statnet_hosts = ["Lizmo","albertk","bella","Teeze"]


results_data = []
unique_players = []

def convert_pst(Y,M,D,H,Mi,S):
    pacificTZ = timezone("US/Pacific")
    datePacific = pacificTZ.localize(datetime(Y,M,D,H,Mi,S), is_dst=None)
    dateEpoch = (datePacific - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return dateEpoch

def convert_pstst(Y,M,D,H,Mi,S):
    pacificTZ = timezone("US/Pacific")
    datePacific = pacificTZ.localize(datetime(Y,M,D,H,Mi,S), is_dst=None)
    dateEpoch = (datePacific - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    result = str(dateEpoch).split(".")
    result2 = result[0][:-2]
    return result2

def database_check(result):
    if result == "y" or result == "Y":
        return True
    else:
        print('ok, no database connection!')
        return False

db_connection = database_check(input("do you have a database connection? y/n \n"))

# start_date= "9/21/2019" 
# end_date = "9/22/2019"


# start day and time for splatfest
fest_start = convert_pst(2019,9,21,12,0,0)
print(fest_start)


# end day and time for splatfest
fest_end = convert_pst(2019,9,22,12,0,0)
print(fest_end)

# 100x modifier for splatfest
onehundred_x =[]
if db_connection:
    onehundred_x_q = Match.select().where(Match.modifier == 100)
    for result in onehundred_x_q:
        short_time = str(result.start_time_fixed)
        onehundred_x.append({'time_id':short_time[:-2]})
    print('number of 100x matches')
    print(onehundred_x)


# 10x modifier for splatfest
ten_x =[]
if db_connection:
    ten_x_query = Match.select().where(Match.modifier == 10)


    for result in ten_x_query:
        # ten_x.append({'time_id':(convert_pstst(result.datetime.year,result.datetime.month,result.datetime.day,result.datetime.hour,result.datetime.minute,result.datetime.second))})
        short_time = str(result.start_time_fixed)
        ten_x.append({'time_id':short_time[:-2]})
        # print(result)

print('number of 10x matches')
print(ten_x)

team_numbers = [1,2]


players_result =[]

# hard coded so code will still work without database connection
if not db_connection:
    team_a = ["Chieftess8","Geryi","Rubixcuban","Zuzu8901","Alex","Gadzooks","ashieIto","せいうん☆∴∵*","ケンヂ83","JacobHofer","Justin_135","Zentangle","Hazerblade","ranjeeta<3","Paisan0","Dende","Dhfjgn","Nathan","SneakyT","JoJo","Sharpie","Puff","Bright","GJB","★JOKΞR★","チビコチャー★Ω★","〒εεηεπβεαη","Callie","Anxiety","Rat","りーりー","Soapy","Enza ☆ミ","Shiek","Alan","Wolvercon","Hanako","Nopoe","TooSweet","Sushimi","albertk"]
    
    team_b = ["Solace","Weez","MmmMMMmmmM","Hazelwize","Lewdcina","micrò","ss","ushuarioh","Cosmic☆Duo ","AltBen","Qwerty","ψ☆Nadia","Lizmo","¥ŘŅ⇒ハビエルww","†§Mean","キPrimal","TaoPanda"]
else:
    team_a = []
    team_b = []
### this code will only work when connected to live data base, db credentials will not be shared so it's disabled ###


    for team_number in team_numbers:
        team_players = Newuser.select().where((Newuser.cur_team == team_number)&(Newuser.cur_fest == True))
        for player in team_players:
            if team_number == 1:
                team_a.append(player.ign)
            if team_number == 2:
                team_b.append(player.ign)

            
# print(team_a)
# print(team_b)

# used to get local data instead of pinging the api during development
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
    if older != None:
        parameters.update({'older_than':older})

    # print(parameters)
    response = requests.get(url, params=parameters)
    data = json.loads(response.text)
    return data

def save_matches(the_match,multi):
    # print(the_match['id'])
    return the_match

def multi_count_assigner(multi):
    if multi == 100:
        return 1
    if multi == 10:
        return 1



def save_players(match,multi):
    result = match['result']
    players = match['players']
    # print(players)
    multi_100x_check = 0
    multi_10x_check = 0
    matchtime = match['start_at']['time']
    for player in players:
        team = player['team']
        name = player['name']
        count_match = 1
        
        total_kills = player['kill_or_assist']
        solo_kills = player['kill']
        deaths = player['death']
        specials = player['special']
        rank_in_team = player['rank_in_team']
        player_assist = total_kills - solo_kills            
        points = player['point']
        win = 0
        if result == "win":
            if team == "my":
                win = 1
                # print("data recorded for host:")
                # print("their team got:")
                # print(points)
                player_clout_original = player['point']
                player_clout = player['point'] * multi
                # print(player_clout)
                team_clout = player['point'] * multi
                # multi_100x_check = multi_count_assigner(multi)
                # multi_10x_check = multi_count_assigner(multi)
                if multi == 100:
                    multi_100x_check = 1
                if multi == 10:
                    multi_10x_check = 1       
                      
            else:
                player_clout
                player_clout_original = player['point']
                team_clout = 0


        if result == "lose":
            if team != "my":
                # print('other splatfest side got:')
                player_clout_original = player['point']
                player_clout = player['point'] * multi
                team_clout = player['point'] * multi
                win = 1
                if multi == 100:
                    multi_100x_check = 1
                if multi == 10:
                    multi_10x_check = 1                
            else:
                player_clout = player['point']
                player_clout_original = player['point']
                team_clout = 0
        team = '0'
        if name in team_a:
            team = '1'
        if name in team_b:
            team = '2'

        player_data = {'name':name,'clout':player_clout,'original_clout':player_clout_original,'assists':player_assist,'team':team,'team_clout':team_clout,'fourx_won':multi_100x_check,'twox_won':multi_10x_check,'number_matches':count_match,'matchstart':matchtime,'win':win,'death':deaths,'specials':specials,'rank_in_team':rank_in_team}
        
        players_result.append(player_data)

already_counted = []
def record_data(data,username,fest_start,fest_end):
    # print(data)
    for match in data:
        # print('this many players')
        players = match['players']
        # print(len(players))
        # print(match)
        matchtime = match['start_at']['time']
        # check for the fest_end time and start time
        player_list = []
        for player in players:
            player_name = player['name']
            player_list.append(player_name)
            if player_name not in unique_players:
                unique_players.append(player_name)
        count_hosts = sum(el in hosts for el in player_list)
        matchtime_string = str(matchtime)
        time_id = matchtime_string[:-2]

        id_check = any(d['time_id'] == time_id for d in results_data)
        multi = 1
        
        # print(onehundred_x)
        # print(time_id)
        four_check = any(d['time_id'] == time_id for d in onehundred_x)
        if four_check == True:
            if time_id not in already_counted:
                multi = 100
                already_counted.append(time_id)
                print(time_id)
                print('Found a 100x!!!!')
            
            # delattr(object, name)
            print(multi)

        two_check = any(d['time_id'] == time_id for d in ten_x)
        if two_check == True:
            if time_id not in already_counted:
                already_counted.append(time_id)
                multi = 10
                print(time_id)
                print('Found a 10x!!!!')
                print(multi)        
        if match['lobby']['key'] == 'private' and match['rule']['key'] == 'nawabari':
            if matchtime < fest_end and matchtime > fest_start:
                if count_hosts > 1 :
                    if id_check == False:
                        results_data.append({'time_id':time_id})
                        # print(match)
                        save_matches(match,multi)
                        save_players(match,multi)
                    if id_check == True:
                        print("this match had 2 hosts in it")
                        # print(match['id'])
                if count_hosts == 1:
                    results_data.append({'time_id':time_id})
                    save_matches(match,multi)
                    
                    save_players(match,multi)                 

    end_of_match_batch = data[-1]
    last_start = end_of_match_batch['start_at']['time']
    oldest_id = end_of_match_batch['id']
    # print(oldest_id)

    if last_start < fest_end and last_start > fest_start:
        try:
            print('need to get more matches')

        ### uncomment this out after development to get all the records
            data = get_splatnet(username,oldest_id) 
            record_data(data,username,fest_start,fest_end)
        except:
            print("no matches exist before the splatfest or some other error")
    


def get_matches(username,fest_start,fest_end):    
    #### this chunk is for getting the data on the web, disabled to be nice during development
    data = get_splatnet(username)


    # used for local parsing... development only ####
    # data = open_data()

    record_data(data,username,fest_start,fest_end)

final_result_player = []
final_result_match = []

for host in statnet_hosts:
    print(host)
    matches = get_matches(host,fest_start,fest_end)

with open('player_result.json', 'w') as fp:
    json.dump(players_result, fp)
currentPath = os.getcwd()

def create_dict(data,groupby,method,outfile):
    df = pd.DataFrame(data)
    if method == 'sum':
        newframe = df.groupby(groupby,as_index=False).sum()
        print('sum detected')
    if method == 'mean':
        newframe = df.groupby(groupby,as_index=False).mean()
    if method == 'team_time':
        newframe = df.groupby(groupby,as_index=False).sum()
        

    output = newframe.to_dict('r')
    the_keys = output[0].keys()
    WriteDictToCSV(outfile,the_keys,output)
    print('created csv file '+str(outfile))

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, lineterminator='\n',delimiter=',')
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as errno:
        print("I/O error({0})".format(errno))    
    return            

# print(players_result)

create_dict(players_result,['name','team'],'sum','result_for_players_sum_0921.csv')
create_dict(players_result,['name','team'],'mean','result_for_players_mean_0921.csv')
create_dict(players_result,['team'],'sum','result_for_teams_0921.csv')
create_dict(players_result,['matchstart','team'],'sum','result_for_times_0921.csv')
create_dict(players_result,['team'],'mean','result_for_average_teams_0921.csv')


print("splatfest results calculated!!")
