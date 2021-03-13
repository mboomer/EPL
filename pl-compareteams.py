import pandas as pd
import numpy as np
import os

# select a premier league season to examine 
print('# ---------------------------------------------------- #')
fname = input('Select a premier league season to examine : ')
if len(fname) == 0 : fname = 'pl-01-02.csv'

#open file
try:
    pl_season = open(fname, 'rt', encoding='UTF8')
except:
    print('Cannot find the file to open')
    quit()

print('# ---------------------------------------------------- #')
print('Using Data From Premier League Season : "%s" '%(fname))
print('# ---------------------------------------------------- #')

#initialise empty lists to use to create the dictionary
DatePlayed = list()
HomeTeam   = list()
AwayTeam   = list()
HomeGoals  = list()
AwayGoals  = list()
Result     = list()

# parse each match in the CSV file
for game in pl_season:
    
    #trim game 
    game = game.rstrip()
    
    # split the game into parts, comma as separator
    game_parts = game.split(',')
    
    # skip the header line, which has "Div" as first column
    if game_parts[0] == "Div" : continue

    # append the match_parts to the corresponding list
    DatePlayed.append(game_parts[1])
    HomeTeam.append(game_parts[2])
    AwayTeam.append(game_parts[3])
    HomeGoals.append(int(game_parts[4]))                # converting str to int
    AwayGoals.append(int(game_parts[5]))                # converting str to int
    Result.append(game_parts[6])

# create the python dictionary - each lists becomes a column in the dataframe
game_data = {  'DatePlayed': DatePlayed, 
                'HomeTeam': HomeTeam, 
                'AwayTeam': AwayTeam, 
                'HomeGoals': HomeGoals, 
                'AwayGoals': AwayGoals, 
                'Result': Result
            }

# create the dataframe from the match_data dictionary
historical_data = pd.DataFrame(game_data)

print('#----------------------------------------------------------------------#')
print('                           historical_data DATAFRAME                           ')
print('#----------------------------------------------------------------------#')
print(historical_data)

# ---------------------------------------------------------------------- #
# select two teams to compare                                            # 
# ---------------------------------------------------------------------- #
print('')
TeamA = input('Select Your First Team : ')
if len(TeamA) == 0 : 
    print('You must select a team name')
    quit()

# ---------------------------------------------------------------------- #
# Check team to make sure it exists in the dataframe                   #
# ---------------------------------------------------------------------- #
ht = historical_data['HomeTeam'].str.contains(TeamA).sum()
at = historical_data['AwayTeam'].str.contains(TeamA).sum()
if (ht > 0) & (at > 0):
    print('%s is a valid team'%(TeamA))
else:
    print('%s is NOT a valid team'%(TeamA))
    quit()

print('')

TeamB = input('Select Your Second Team : ')
if len(TeamB) == 0 : 
    print('You must select a team name')
    quit()

# ---------------------------------------------------------------------- #
# Check team to make sure it exists in the dataframe                     #
# ---------------------------------------------------------------------- #
ht = historical_data['HomeTeam'].str.contains(TeamB).sum()
at = historical_data['AwayTeam'].str.contains(TeamB).sum()
if (ht > 0) & (at > 0):
    print('%s is a valid team'%(TeamB))
else:
    print('%s is NOT a valid team'%(TeamB))
    quit()

# ---------------------------------------------------------------------- #
# Check that 2 different teams have been selected                        #
# ---------------------------------------------------------------------- #
if TeamA == TeamB:
    print('You have entered the same team twice, please select two different teams to compare')
    quit()

print()
print('# ---------------------------------------------------- #')
print('Comparing Stats for %s and %s'%(TeamA, TeamB))
print('# ---------------------------------------------------- #')

# ---------------------------------------------------------------------- #
# Build League Table and compare the current positions of each team      #
# ---------------------------------------------------------------------- #

# create an empty dictionary 
league_table = dict()

matches = open(fname, 'rt', encoding='UTF8')

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
    
print('#-------------------------------------------------#')
print('         REVERSE SORT THE LEAGUE TABLE             ')
print('#-------------------------------------------------#')

print('Team', '\t\t', 'Points')

# create an empty dict to hold the sorted values
sorted_league_table = {}

# return a list of keys (team), sorted in value (points) order - from highest to lowest
sorted_keys = sorted(league_table, key=league_table.get, reverse=True) 

# for each team in the list of sorted_keys 
# Add the key in the sorted dictionary and set to the corresponding value from league table  
for team in sorted_keys:
    sorted_league_table[team] = league_table[team]

# print the key value pairs from the sorted league table
for team,points in sorted_league_table.items():
    if len(team) > 6:
        print(team, '\t', points)
    else:
        print(team, '\t\t', points)

print('#-------------------------------------------------#')
print(TeamA, ' - Current Position : ', sorted_keys.index(TeamA), ' With Points : ', sorted_league_table[TeamA])
print(TeamB, ' - Current Position : ', sorted_keys.index(TeamB), ' With Points : ', sorted_league_table[TeamB])
print('#-------------------------------------------------#')

# ----------------------------------------------------------------- #
#       Read in each CSV file and append to epl_df dataframe        #
# ----------------------------------------------------------------- #

try:
    historical_data = pd.read_csv('data-csv\\all-seasons.csv')
    print(historical_data)
except:
    print('Cannot Open Historical Data File')
    quit()

# ----------------------------------------------------------------- #
#  Check the number of wins/losses/draws                            #
# ----------------------------------------------------------------- #


print('#-----------------------------------------------------------#')
print('    %s - %s : Played, Win, Loss, Draw, Goal Diff'%(TeamA, TeamB))
print('#-----------------------------------------------------------#')
print('Team', '\t\t Pl', ' \t W', '\t L', '\t D','\t   GD', '\tPts')
print('-------------------------------------------------------------')

# for each team query the historical_results for matching rows
# count the P/W/L/D/GD from the matching rows 

TeamA_Wins = (( (historical_data.loc[ ((historical_data.HomeTeam == TeamA) & (historical_data.FTR == 'H') ) | ((historical_data.AwayTeam == TeamA) & (historical_data.FTR == 'A') ), 'FTR' ]) )).count()
TeamB_Wins = (( (historical_data.loc[ ((historical_data.HomeTeam == TeamB) & (historical_data.FTR == 'H') ) | ((historical_data.AwayTeam == TeamB) & (historical_data.FTR == 'A') ), 'FTR' ]) )).count()

TeamA_Loss = (((historical_data.loc[ ((historical_data.HomeTeam == TeamA) & (historical_data.FTR == 'A') ) | ((historical_data.AwayTeam == TeamA) & (historical_data.FTR == 'H') ), 'FTR' ]) )).count()
TeamB_Loss = (( (historical_data.loc[ ((historical_data.HomeTeam == TeamB) & (historical_data.FTR == 'A') ) | ((historical_data.AwayTeam == TeamB) & (historical_data.FTR == 'H') ), 'FTR' ]) )).count()

AB_Draws   = (( (historical_data.loc[ ((historical_data.HomeTeam == TeamA) & (historical_data.FTR == 'D') ) | ((historical_data.AwayTeam == TeamA) & (historical_data.FTR == 'D') ), 'FTR' ]) )).count()

AB_Played  = (( (historical_data.loc[ ((historical_data.HomeTeam == TeamA) | (historical_data.AwayTeam == TeamA) ), 'FTR' ]) )).count()

TeamA_GFH  = (( ( historical_data.loc[ ( (historical_data.HomeTeam == TeamA) ), 'FTHG' ]))).sum()
TeamA_GFA  = (( ( historical_data.loc[ ( (historical_data.AwayTeam == TeamA) ), 'FTAG' ]))).sum()
TeamA_GAH  = (( ( historical_data.loc[ ( (historical_data.HomeTeam == TeamA) ), 'FTAG']) )).sum()
TeamA_GAA  = (( ( historical_data.loc[ ( (historical_data.AwayTeam == TeamA) ), 'FTHG']) )).sum()

TeamB_GFH  = (( ( historical_data.loc[ ( (historical_data.HomeTeam == TeamB) ), 'FTHG' ]))).sum()
TeamB_GFA  = (( ( historical_data.loc[ ( (historical_data.AwayTeam == TeamB) ), 'FTAG' ]))).sum()
TeamB_GAH  = (( ( historical_data.loc[ ( (historical_data.HomeTeam == TeamB) ), 'FTAG']) )).sum()
TeamB_GAA  = (( ( historical_data.loc[ ( (historical_data.AwayTeam == TeamB) ), 'FTHG']) )).sum()

TeamA_GD   = ( (TeamA_GFH + TeamA_GFA ) - ((TeamA_GAH + TeamA_GAA )) )
TeamB_GD   = ( (TeamB_GFH + TeamB_GFA ) - ((TeamB_GAH + TeamB_GAA )) )

if len(TeamA) > 6:
    print(TeamA, '\t', AB_Played, '\t', TeamA_Wins, '\t', TeamA_Loss, '\t', AB_Draws, '\t', '%d:%d'%((TeamA_GFH + TeamA_GFA), (TeamA_GAH + TeamA_GAA)), '\t', sorted_league_table[TeamA])
else:
    print(TeamA, '\t\t', AB_Played, '\t', TeamA_Wins, '\t', TeamA_Loss, '\t', AB_Draws, '\t', '%d:%d'%((TeamA_GFH + TeamA_GFA), (TeamA_GAH + TeamA_GAA)), '\t', sorted_league_table[TeamA])
    
if len(TeamB) > 6:
    print(TeamB, '\t', AB_Played, '\t', TeamB_Wins, '\t', TeamB_Loss, '\t', AB_Draws, '\t', '%d:%d'%((TeamB_GFH + TeamB_GFA), (TeamB_GAH + TeamB_GAA)), '\t', sorted_league_table[TeamB])
else:
    print(TeamB, '\t\t', AB_Played, '\t', TeamB_Wins, '\t', TeamB_Loss, '\t', AB_Draws, '\t', '%d:%d'%((TeamB_GFH + TeamB_GFA), (TeamB_GAH + TeamB_GAA)), '\t', sorted_league_table[TeamB])
    