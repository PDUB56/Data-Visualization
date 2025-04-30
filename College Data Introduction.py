"""
An introduction to exploring and transforming college football data
by: Paul Zakowski
Following 
GJMcClintock/Getting Started with College Football Data in Python
"""
import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
from tqdm import tqdm as tqdm
import pprint as pp

API_KEY = "Bearer A23+vO27dNehOfgIxQslYuhHtiCB8mv+LN4G1VeG4TA5+oaTHNZ271hkI7DLR7Gy"
HEADERS = {"Authorization" : API_KEY}

#Set variables for the season and prepare the data frame for data
YEAR = 2024
WEEKS = list(range(0,16))
pbp_req = []
pbp = pd.DataFrame()

#A loop for sorts through every week to add pbp data
for week in tqdm(WEEKS, desc = "fetch plays"):
    #Assign which variables to pass
    parameters = {"year":YEAR, "week":week}
    #Request the data from the URL
    pbp_req = requests.get("https://api.collegefootballdata.com/plays", 
                            params = parameters,
                            headers = HEADERS)
    #Add the week's data we just requested and put it into the data frame while ignoring empty weeks
    try:
        x = pd.DataFrame(json.loads(pbp_req.text))
        pbp = pd.concat([pbp,x])
    except IndexError:
        pass

#List of offensive play types and setiing to data frames to offensive plays and others
off_play_types = ['Pass Reception',
 'Rush',
 'Sack',
 'Pass Incompletion',
 'Fumble Recovery (Opponent)',
 'Passing Touchdown',
 'Rushing Touchdown',
 'Pass Interception Return',
 'Fumble Recovery (Own)',
 'Interception Return Touchdown',
 'Fumble Return Touchdown']

off_plays = pbp[pbp['play_type'].isin(off_play_types)].copy()
excl_plays = pbp[~pbp['play_type'].isin(off_play_types)].copy()

#Add flags for run and pass plays
off_plays.loc[(off_plays['play_type'].str.contains('Pass')), 'pass'] = 1
off_plays.loc[(off_plays['play_type'].str.contains('Interception')), 'pass'] = 1
off_plays.loc[(off_plays['play_type'].str.contains('Sack')), 'pass'] = 1
off_plays.loc[(off_plays['play_text'].str.contains('pass')), 'pass'] = 1
off_plays.loc[(off_plays['play_type'].str.contains('Rush')), 'rush'] = 1
off_plays.loc[(off_plays['play_text'].str.contains('rush')), 'rush'] = 1

off_plays.loc[(off_plays['play_type'].str.contains('Interception')), 'yards_gained'] = 0

flags_na = {'rush':0, 'pass':0}

off_plays.fillna(value=flags_na, inplace=True)

#Caculate the statistics in a function for any data set
#Rework of Function to factor Predicted Points and Yards Per Play
def calcs(x):
      names = {'Plays': x['yards_gained'].count(),
               'YPA': x[(x['pass'] == 1) & (x['play_type']!= 'Sack')]['yards_gained'].mean(),
               'YPC' :x[x['rush'] == 1]['yards_gained'].mean(),
               'PPA_Pass': x[(x['pass'] == 1) & (x['play_type']!= 'Sack')]['ppa'].mean(),
               'PPA_Rush' :x[(x['rush'] == 1)]['ppa'].mean(),
               'YPP' : x['yards_gained'].mean()
                }
      return pd.Series(names)
off_plays['ppa'] = off_plays['ppa'].astype(float)
offense =  off_plays.groupby('offense').apply(calcs)

# Filter out FCS Games
offense = offense[offense['Plays'] > 300].copy()

#Team Logos
team_logos = {
    'Abeline Christian': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Abeline Christian ACU.png",
    'Air Force': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Air Force.png",
    'Akron': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Akron.png",
    'Alabama': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Alabama.png",
    'App State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/App State.png",
    'Arizona': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Arizona.png",
    'Arizona State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Arizona State.png",
    'Arkansas': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Arkansas.png",
    'Arkansas State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Arkansas State Red.png",
    'Army': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Army.png",
    'Auburn': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Auburn.png",
    'Ball State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Ball State.png",
    'Baylor': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Baylor.png",
    'Boise State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Boise State.png",
    'Boston College': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Boston College.png",
    'Bowling Green': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Bowling Green.png",
    'Buffalo': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Buffalo.png",
    'BYU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/BYU.png",
    'California': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Cal.png",
    'Central Michigan': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Central Michigan.png",
    'Charlotte': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Charlotte.png",
    'Cincinnati': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Cincinnatti Bearcats.png",
    'Clemson': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Clemson.png",
    'Coastal Carolina': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Coastal Carolina.png",
    'Colorado': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Colorado Buffaloes.png",
    'Colorado State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Colorado State.png",
    'Duke': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Duke.png",
    'East Carolina': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/ECU.png",
    'Eastern Michigan': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Eastern Michigan.png",
    'FAU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/FAU.png",
    'FIU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/FIU.png",
    'Florida': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Florida Gators.png",
    'Florida State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Florida State.png",
    'Fresno State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Fresno State.png",
    'Georgia': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Georgia.png",
    'Georgia Southern': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Georgia Southern.png",
    'Georgia State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Georgia State.png",
    'Georgia Tech': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Georgia Tech.png",
    'Hawaii': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Hawaii.png",
    'Houston': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Houston.png",
    'Illinois': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Illinois.png",
    'Indiana': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Indiana.png",
    'Iowa': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Iowa.png",
    'Iowa State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Iowas State.png",
    'James Madison': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/JMU.png",
    'Jacksonville State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/JSU.png",
    'Kansas': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Kansas.png",
    'Kansas State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Kansas State.png",
    'Kent State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Kent State.png",
    'Kentucky': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Kentucky UK.png",
    'LA Tech': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/LA Tech.png",
    'Liberty': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Liberty.png",
    'Louisiana': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Louisiana Ragin Cajuns.png",
    'Louisiana Monroe': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Louisiana Monroe.png",
    'Louisville': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Lousville.png",
    'LSU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/LSU.png",
    'Marshall': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Marshall.png",
    'Maryland': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Maryland.png",
    'Memphis': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Memphis.png",
    'Miami (FL)': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Miami Florida.png",
    'Miami (OH)': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Miami Ohio.png",
    'Michigan': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Michigan.png",
    'Michigan State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Michigan State.png",
    'Minnesota': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Minnesota.png",
    'Ole Miss': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Ole Miss.png",
    'Mississippi State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Mississippi.png",
    'Missouri': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Missouri.png",
    'Middle Tennessee': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Middle Tennessee.png",
    'Minnesota': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Minnesota.png",
    'Navy': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Navy.png",
    'NC State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/NC State.png",
    'Nebraska': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Nebraska.png",
    'Nevada': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Nevada.png",
    'New Mexico State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/New Mexico State.png",
    'NIU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/NIU.png",
    'North Carolina': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/North Carolina.png",
    'North Texas': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Northern Texas.png",
    'Northwestern': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/North Western.png",
    'Notre Dame': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Notre Dame.png",
    'Ohio': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Ohio Bobcats.png",
    'Ohio State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Ohio State Dark Background.png",
    'Oklahoma': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Oklahoma.png",
    'Oklahoma State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Oklahoma State.png",
    'Old Dominion': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Old Dominion.png",
    'Oregon': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Oregon.png",
    'Oregon State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Oregon State.png",
    'Penn State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Penn State.png",
    'Pitt': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Pitt.png",
    'Purdue': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Purdue.png",
    'Rice': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Rice.png",
    'Rutgers': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Rutgers.png",
    'San Diego State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/San Diego.png",
    'San Jose State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/San Jose State.png",
    'SMU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/SMU.png",
    'South Alabama': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/South Alabama.png",
    'South Carolina': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/South Carolina.png",
    'Sam Houston': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Sam Houston.png",
    'Southern Miss': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Southern Miss.png",
    'Stanford': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Stanford.png",
    'Syracuse': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Syracuse.png",
    'TCU': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/TCU.png",
    'Temple': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Temple.png",
    'Tennessee': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Tennessee.png",
    'Texas': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Texas.png",
    'Texas A&M': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Texas A&M.png",
    'Texas State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Texas State.png",
    'Texas Tech': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Texas Tech.png",
    'Toledo': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Toledo.png",
    'Troy': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Troy.png",
    'Tulane': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Tulane.png",
    'Tulsa': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Tulsa.png",
    'UAB': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UAB.png",
    'UCF': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UCF.png",
    'UCLA': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UCLA.png",
    'UMass': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UMass.png",
    'UNLV': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UNLV.png",
    'USC': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/USC.png",
    'Utah': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Utah.png",
    'Utah State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Utah State.png",
    'UCONN': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UCONN.png",
    'USF': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/USF.png",
    'UTEP': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UTEP.png",
    'UTSA': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/UTSA.png",
    'Vanderbilt': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Vanderbilt.png",
    'Virginia': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Virginia.png",
    'Virginia Tech': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Virginia Tech.png",
    'Wake Forest': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Wake Forest.png",
    'Washington': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Washington.png",
    'Washington State': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Washington State.png",
    'West Virginia': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/West Virginia.png",
    'Western Kentucky': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Western Kentucky Hilltopers.png",
    'Wisconsin': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Wisconsin.png",
    'Wyoming': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Wyoming.png",
    'Western Michigan': "C:/Users/pzako/OneDrive/Desktop/Football/CFB Logos/Western Michigan.png",

}
#Data VIsualization
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
# Filter the offense DataFrame to include only teams with logos
offense_with_logos = offense[offense.index.isin(team_logos.keys())]

# Scatter plot with team logos
plt.figure(figsize=(10, 10))
plt.scatter(offense_with_logos['YPC'], offense_with_logos['YPA'], alpha=0)  # Use alpha=0 to hide dots

# Add logos to the scatter plot
for team, row in offense_with_logos.iterrows():
    logo_path = team_logos[team]
    try:
        # Load the logo image
        logo = plt.imread(logo_path)
        imagebox = OffsetImage(logo, zoom=0.1)  # Adjust zoom level as needed
        ab = AnnotationBbox(imagebox, (row['YPC'], row['YPA']), frameon=False)
        plt.gca().add_artist(ab)
    except FileNotFoundError:
        print(f"Logo for {team} not found at {logo_path}")

# Set the title and labels
plt.title('Rush vs Pass Avg YPA', fontsize=16, fontweight='bold')
plt.xlabel('Avg Rush YPC', fontsize=14)
plt.ylabel('Avg Pass YPA', fontsize=14)

# Show the plot
plt.show()