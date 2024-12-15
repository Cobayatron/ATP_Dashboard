#import all necessary libraries
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from Combinefiles import Combinefiles

st.set_page_config(layout="wide")
initial_sidebar_state="collapsed" #this seems not to work
all=Combinefiles(1998,2024)

players=pd.read_csv('Data/atp_players.csv')
st.logo ('Data/ATP.png',size='large')

with st.sidebar:
    selector=st.selectbox("Who is your favourite Tennis Player?", players['name_first'] + ' ' + players['name_last'],disabled=False)
    names=selector.split()
    id=players.loc[(players['name_first']==names[0]) & (players['name_last']==names[1]),'player_id'].values[0]