# dictionary uses {} 
# Lists uses []
# Creating a dictionary for converting to panda dataframe
# data = {
#   "HomeTeam" : ['Arsenal', 'Man Utd', 'Chelsea'],
#   "AwayTeam" : ['Charlton','Everton', 'Burnley'],
#   "HomeGoals": [1, 2, 2],
#   "AwayGoals": [0, 4, 2],
#   "Result"   : ['H','A','D']
# }
# df = pd.DataFrame(data)

import pandas as pd
import numpy as np
import os

fname = input('Enter File Name : ')
if len(fname) == 0 : fname = 'pl-01-02.csv'

#open file
try:
    matches = open(fname, 'rt', encoding='UTF8')
except:
    print('Cannot find the file to open')
    quit()

#initialise empty lists to use to create the dictionary
DatePlayed = list()
HomeTeam   = list()
AwayTeam   = list()
HomeGoals  = list()
AwayGoals  = list()
Result     = list()

# parse each match in the CSV file
for match in matches:
    
    #trim match
    match = match.rstrip()
    
    # split the match into parts, comma as separator
    match_parts = match.split(',')
    
    # skip the header line, which has "Div" as first column
    if match_parts[0] == "Div" : continue

    # append the match_parts to the corresponding list
    DatePlayed.append(match_parts[1])
    HomeTeam.append(match_parts[2])
    AwayTeam.append(match_parts[3])
    HomeGoals.append(match_parts[4])
    AwayGoals.append(match_parts[5])
    Result.append(match_parts[6])

# create the python dictionary - each lists becomes a column in the dataframe
match_data = {  'DatePlayed': DatePlayed, 
                'HomeTeam': HomeTeam, 
                'AwayTeam': AwayTeam, 
                'HomeGoals': HomeGoals, 
                'AwayGoals': AwayGoals, 
                'Result': Result
            }

# create the dataframe from the match_data dictionary
results = pd.DataFrame(match_data)

# the HomeGoals and AwayGoals columns were str not int
# convert the str values to ints
results['HomeGoals'] = results['HomeGoals'].astype(int)
results['AwayGoals'] = results['AwayGoals'].astype(int)

# print(results.info())
# print('SIZE  ', results.size)
# print('SHAPE ', results.shape)
# print(results.duplicated().to_string())
# print(results.to_string())

print('#----------------------------------------------------------------------#')
print('                           RESULTS DATAFRAME                           ')
print('#----------------------------------------------------------------------#')
print(results)

# create the league table from the CSV file
# create a dictionary with an entry for each team
# need to check if the team exists and if it does calcuclate the points and add it to the value for the team

matches = open(fname, 'rt', encoding='UTF8')

# create the empty dictionary 
league_table = dict()

# parse each match in the CSV file matches
for match in matches:
    
    #trim match
    match = match.rstrip()
    
    # split the match into parts, comma as separator
    match_parts = match.split(',')
    
    # skip the header line, which has "Div" as first column
    if match_parts[0] == "Div" : continue

    ht  = match_parts[2]
    at  = match_parts[3]
    res = match_parts[6]

    # this creates a new Key or retrieves an existing Key
    # if a new Key then the Value is 0
    # if an existing Key, the Value is incremented by the points for W/L/D
    if res == 'H':
        league_table[ht] = league_table.get(ht, 0) + 3
    elif res == 'A':
        league_table[at] = league_table.get(at, 0) + 3
    elif res == 'D':
        league_table[ht] = league_table.get(ht, 0) + 1
        league_table[at] = league_table.get(at, 0) + 1
    
print('#----------------------------------------#')
print('       PYTHON DICTIONARY League Table     ')
print('#----------------------------------------#')
print('Team', '\t\t', 'Points')

# print the key value pairs from the league table
for team,points in league_table.items():
    if len(team) > 6:
        print(team, '\t', points)
    else:
        print(team, '\t\t', points)


print('#-------------------------------------------------#')
print('         REVERSE SORT THE LEAGUE TABLE             ')
print('#-------------------------------------------------#')

sorted_league_table = {}
# return a list of keys, sorted in value order - from highest to lowest
sorted_keys = sorted(league_table, key=league_table.get, reverse=True) 

for team in sorted_keys:
    # for each team in the list of sorted keys 
    # Add the key in the sorted dictionary and set to the corresponding value from league table  
    sorted_league_table[team] = league_table[team]

print('#-------------------------------------------------#')
print('  EXTRACT ROWS FOR EACH TEAM FROM THE DATAFRAME    ')
print('#-------------------------------------------------#')

# Wins = (( ( results.loc[ ((results.HomeTeam == team) | (results.AwayTeam == team)), 'Result' ]) ) == 'H').sum()
# HomeWins = (( ( results.loc[ ( (results.HomeTeam == team) ) & ( (results.FTHG > results.FTAG)), 'FTR' ]) )).count()
# (( ( df.loc[ ((df.HomeTeam == 'Arsenal') & (df.FTR == 'H') ) | (  (df.AwayTeam == 'Arsenal') & (df.FTR == 'A') ), 'FTR' ]) )).count()

# initialise the counter variables
Played   = 0
HomeWins = 0
AwayWins = 0
Losses   = 0
Draws    = 0
GFH      = 0    # Goals For Home
GFA      = 0    # Goals For Away
GAH      = 0    # Goals Against Home
GAA      = 0    # Goals Against away
GoalDiff = 0

print('#-----------------------------------------------------------#')
print('                         LEAGUE TABLE                        ')
print('#-----------------------------------------------------------#')
print('Team', '\t\t Pl', ' \t W', '\t L', '\t D','\t   GD', '\tPts')
print('-------------------------------------------------------------')

# for each team query the league table for matching rows
# count the W/L/D from the matching rows 

for team, points in sorted_league_table.items():
    
    Wins   = (((results.loc[ ((results.HomeTeam == team) & (results.Result == 'H') ) | ((results.AwayTeam == team) & (results.Result == 'A') ), 'Result' ]) )).count()
    Losses = (((results.loc[ ((results.HomeTeam == team) & (results.Result == 'A') ) | ((results.AwayTeam == team) & (results.Result == 'H') ), 'Result' ]) )).count()
    Draws  = (((results.loc[ ((results.HomeTeam == team) & (results.Result == 'D') ) | ((results.AwayTeam == team) & (results.Result == 'D') ), 'Result' ]) )).count()
    Played = (((results.loc[ ((results.HomeTeam == team) | (results.AwayTeam == team) ), 'Result' ]) )).count()

    GFH    = (((results.loc[ ((results.HomeTeam == team) ), 'HomeGoals' ]))).sum()
    GFA    = (((results.loc[ ((results.AwayTeam == team) ), 'AwayGoals' ]))).sum()

    GAH = (( ( results.loc[ ( (results.HomeTeam == team)), 'AwayGoals']) )).sum()
    GAA = (( ( results.loc[ ( (results.AwayTeam == team)), 'HomeGoals']) )).sum()

    GoalDiff = ((GFH + GFA) - (GAH + GAA))

    if len(team) > 6:
        # print(team, '\t', Played, '\t', Wins, '\t', Losses, '\t', Draws, '\t', GoalDiff, '\t', points)
        print(team, '\t', Played, '\t', Wins, '\t', Losses, '\t', Draws, '\t', '%d:%d'%((GFH + GFA), (GAH + GAA)), '\t', points)
    else:
        print(team, '\t\t', Played, '\t', Wins, '\t', Losses, '\t', Draws, '\t', '%d:%d'%((GFH + GFA), (GAH + GAA)), '\t', points)
    
