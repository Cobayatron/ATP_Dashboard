#import all necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium
# from Combinefiles import Combinefiles

st.set_page_config(layout="wide")
initial_sidebar_state="collapsed" #this seems not to work

anos_list=[]
for i in range(1998,2025):
    ano=pd.read_csv(f'Data/atp_matches_{i}.csv')
    anos_list.append(ano)
all=pd.concat(anos_list)    
# Drop Davies Cup matches
all=all[all['tourney_level']!='D']


# Load Data for rankings and create a single variable
rank90=pd.read_csv('Data/atp_rankings_90s.csv')
rank00=pd.read_csv('Data/atp_rankings_00s.csv')
rank10=pd.read_csv('Data/atp_rankings_10s.csv')
rank20=pd.read_csv('Data/atp_rankings_20s.csv')
rankcurrent=pd.read_csv('Data/atp_rankings_current.csv')    
ranking=pd.concat([rank90,rank00,rank10,rank20,rankcurrent])
ranking=ranking[ranking['ranking_date']>19980000]

# Data for all players
players=pd.read_csv('Data/selectedplayers.csv')
players=players.sort_values(by=['name_last','name_first'])
st.logo ('Data/ATP.png',size='large')

with st.sidebar:
    selector=st.selectbox("Who is your favourite Tennis Player?", players['name_first'] + ' ' + players['name_last'],disabled=False)
    names=selector.split()
    id=players.loc[(players['name_first']==names[0]) & (players['name_last']==names[1]),'player_id'].values[0]
st.title(selector)
c=st.columns([1.5, 1],gap='small', vertical_alignment='top')
g=st.columns([1.5, 1],gap='small', vertical_alignment='top')

# General information of the player
nationality=players['ioc'][(players['player_id']==id)].values[0]
hand=players['hand'][(players['player_id']==id)].values[0]
h=players['height'][(players['player_id']==id)].values[0]
if np.isnan(h):
    h='Unknown'
if hand=='R':
    hand='Right'
elif hand=='L':        
    hand='Left'
else:
    hand='Unknown'
dob=players['dob'][(players['player_id']==id)].values[0]
birth=str(int(dob))
birth=birth[6:] + '-' + birth[4:6] + '-' + birth[:4]

# Performance of the player
matches=all[(all['winner_id']==id) | (all['loser_id']==id)] # Matches of the player in the database 
GSmatches=matches[matches['tourney_level']=='G'] # Grand Slam matches
Mastermatches=matches[(matches['tourney_level']=='M')] # Master matches
won=matches[matches['winner_id']==id] # Matches won by the player
lost=matches[matches['loser_id']==id] # Matches lost by the player
wonGS=GSmatches[GSmatches['winner_id']==id] # Grand Slam matches won by the player
lostGS=GSmatches[GSmatches['loser_id']==id]# Grand Slam matches lost by the player
if len(GSmatches)==0:
    ratioGS='--'
else:
    ratioGS=str(round(len(wonGS)/len(GSmatches)*100,2)) 
wonMaster=Mastermatches[Mastermatches['winner_id']==id] # Master matches won by the player
lostMaster=Mastermatches[Mastermatches['loser_id']==id] # Master matches lost by the player

if len(Mastermatches)==0:
    ratioM='--'
else:
    ratioM=str(round(len(wonMaster)/len(Mastermatches)*100,2)) 


# Ranking of the player
history=ranking[ranking['player']==id]
h20=len(history[history['rank']<=20])
h10=len(history[history['rank']<=10])
h5=len(history[history['rank']<=5])
h1=len(history[history['rank']==1])


with c[0]:
    with st.container(border=True):
        col1, col2, col3 ,col4= st.columns(4,gap='small')
        col1.metric(label='Nationality',value=nationality)
        col2.metric(label='Height',value=h)
        col3.metric(label='Birth',value=birth)
        col4.metric(label='Hand', value=hand)
with c[1]:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3,gap='small')
        col1.metric(label='Total Matches',value=len(matches))
        col2.metric(label='Grand Slam Matches',value=len(GSmatches))
        col3.metric(label='Master Matches',value=len(Mastermatches))
        
with g[0]:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4,gap='small')
        col1.metric(label='Weeks #1',value=h1)
        col2.metric(label='Weeks Top 5',value=h5)
        col3.metric(label='Weeks Top 10',value=h10)
        col4.metric(label='Weeks Top 20', value=h20)
with g[1]:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3,gap='small')
        col1.metric(label='Total +/-',value=str(len(won)) + '-' + str(len(lost)),delta=str(str(round(len(won)/len(matches)*100,2)) + ' %'))
        col2.metric(label='Grand Slam +/-',value=str(len(wonGS)) + '-' + str(len(lostGS)),delta=str(ratioGS + ' %'))
        col3.metric(label='Master +/-',value=str(len(wonMaster)) + '-' + str(len(lostMaster)),delta=str(ratioM + ' %'))            

# Map of the player's performance using GOAT points