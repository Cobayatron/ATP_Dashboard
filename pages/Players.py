#import all necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
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
    if len(names)==2:
        id=players.loc[(players['name_first']==names[0]) & (players['name_last']==names[1]),'player_id'].values[0]
    elif len(names)==3:
        id=players.loc[(players['name_first']==names[0] + ' '+ names[1]) & (players['name_last']==names[2]) | (players['name_first']==names[0]) & (players['name_last']==names[1]+ ' '+ names[2]),'player_id'].values[0]        
    elif len(names)==4:
        id=players.loc[(players['name_first']==names[0] + ' '+ names[1]) & (players['name_last']==names[2]+ ' '+ names[3]) | (players['name_first']==names[0]) & (players['name_last']==names[1]+ ' '+ names[2]+ ' '+ names[3]) | (players['name_first']==names[0]+ ' '+ names[1]+ ' '+ names[2]) & (players['name_last']==names[3]),'player_id'].values[0]
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
h100=len(history[history['rank']<=100])
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
        col2.metric(label='Weeks Top 10',value=h10)
        col3.metric(label='Weeks Top 20',value=h20)
        col4.metric(label='Weeks Top 100', value=h100)
with g[1]:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3,gap='small')
        col1.metric(label='Total +/-',value=str(len(won)) + '-' + str(len(lost)),delta=str(str(round(len(won)/len(matches)*100,2)) + ' %'))
        col2.metric(label='Grand Slam +/-',value=str(len(wonGS)) + '-' + str(len(lostGS)),delta=str(ratioGS + ' %'))
        col3.metric(label='Master +/-',value=str(len(wonMaster)) + '-' + str(len(lostMaster)),delta=str(ratioM + ' %'))            

# Map of the player's performance using GOAT points (invented by me but fixed)
if matches['winner_id'].iloc[0]==id:
    year1=int(matches['winner_age'].iloc[0])
else:
    year1=int(matches['loser_age'].iloc[0])
if matches['winner_id'].iloc[-1]==id:
    year2=int(matches['winner_age'].iloc[-1])
else:
    year2=int(matches['loser_age'].iloc[-1])    
years=[]
for i in range(year1,year2+1):
    years.append(i)
points=np.zeros((4,len(years)))  # Matrix to complete with the corresponding points, columns will be the player's age
categories=['ATP','Masters', 'Tour Finals', 'Grand Slam'] #Rows of the matrix

# Total performance points calculation
atp=matches[(matches['tourney_level']=='A') & (matches['round']=='F')]
p_atp=len(atp[atp['winner_id']==id])*2+len(atp[atp['loser_id']==id])*1  
Tfinals=matches[(matches['tourney_level']=='F') & (matches['round']=='F')]
if any(Tfinals['tourney_name']=='NextGen Finals'):
    NG=Tfinals[Tfinals['tourney_name']=='NextGen Finals']
    p_atp=p_atp+len(NG[NG['winner_id']==id])*2+len(NG[NG['loser_id']==id])*1
    Tfinals=Tfinals[Tfinals['tourney_name']!='NextGen Finals']

TSFinals=matches[(matches['tourney_level']=='F') & (matches['round']=='SF')]
TSFinals=TSFinals[TSFinals['tourney_name']!='NextGen Finals']
p_Finals=len(Tfinals[Tfinals['winner_id']==id])*6+len(Tfinals[Tfinals['loser_id']==id])*3+len(TSFinals[TSFinals['loser_id']==id])*1
GSFinals=GSmatches[(GSmatches['round']=='F')]
GSSFinals=GSmatches[(GSmatches['round']=='SF')]
GSQFinals=GSmatches[(GSmatches['round']=='QF')]
MasterFinals=Mastermatches[(Mastermatches['round']=='F')]
MasterSFinals=Mastermatches[(Mastermatches['round']=='SF')]
p_GS=len(GSFinals[GSFinals['winner_id']==id])*8+len(GSFinals[GSFinals['loser_id']==id])*4+len(GSSFinals[GSSFinals['loser_id']==id])*2+len(GSQFinals[GSQFinals['loser_id']==id])*1
p_Master=len(MasterFinals[MasterFinals['winner_id']==id])*4+len(MasterFinals[MasterFinals['loser_id']==id])*2+len(MasterSFinals[MasterSFinals['loser_id']==id])*1
p_points=p_atp+p_Finals+p_GS+p_Master

p=st.columns([3,1],gap='small',vertical_alignment='center')
with p[1]:
    st.header(''':red[Performance]''')
    with st.container(border=True):
        st.metric(label=':blue-background[Performance points]',value=p_points)


for i in range(year1,year2+1):
    points[0,i-year1]=len(atp[(atp['winner_id']==id) & (atp['winner_age'].astype(int)==i)])*2+len(atp[(atp['loser_id']==id) & (atp['loser_age'].astype(int)==i)]*1)
    points[1,i-year1]=len(MasterFinals[(MasterFinals['winner_id']==id) & (MasterFinals['winner_age'].astype(int)==i)])*4+len(MasterFinals[(MasterFinals['loser_id']==id) & (MasterFinals['loser_age'].astype(int)==i)])*2+len(MasterSFinals[(MasterSFinals['loser_id']==id) & (MasterSFinals['loser_age'].astype(int)==i)])*1   
    points[2,i-year1]=len(Tfinals[(Tfinals['winner_id']==id) & (Tfinals['winner_age'].astype(int)==i)])*6+len(Tfinals[(Tfinals['loser_id']==id) & (Tfinals['loser_age'].astype(int)==i)])*3+len(TSFinals[(TSFinals['loser_id']==id) & (TSFinals['loser_age'].astype(int)==i)])*1
    points[3,i-year1]=len(GSFinals[(GSFinals['winner_id']==id) & (GSFinals['winner_age'].astype(int)==i)])*8+len(GSFinals[(GSFinals['loser_id']==id) & (GSFinals['loser_age'].astype(int)==i)])*4+len(GSSFinals[(GSSFinals['loser_id']==id) & (GSSFinals['loser_age'].astype(int)==i)])*2+len(GSQFinals[(GSQFinals['loser_id']==id) & (GSQFinals['loser_age'].astype(int)==i)])*1

with p[0]:
    
    fig1, axs = plt.subplots()
    fig1=px.imshow(points,labels=dict(x="Age", y="", color="Performance"),x=years, y=categories ,color_continuous_scale='sunset')
    st.plotly_chart(fig1)