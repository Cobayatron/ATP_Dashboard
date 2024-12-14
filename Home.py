
#import all necessary libraries
import pandas as pd
import seaborn as sns
import plotly as pt
import plotly.express as px
import numpy as np
import streamlit as st
import folium
import matplotlib.pyplot as plt
from matplotlib import rcParams
from streamlit_folium import st_folium
from streamlit_navigation_bar import st_navbar
from Combinefiles import Combinefiles

##Matplot settings
plt.rcParams.update({'font.size':4})



###############
#Open all files in the folder
all=Combinefiles(1998,2024)
allfinals = pd.read_csv('..\Data\Alltournaments.csv')
tourn_names=allfinals.drop_duplicates('tourney_name')
tourneys_loc=pd.read_csv('..\Data\Tournament_location.csv')
st.set_page_config(layout="wide")
initial_sidebar_state="collapsed" #this seems not to work
st.logo ('..\Data\ATP.png',size='large')




with st.sidebar:
		selector=st.selectbox("Which Tennis Tournament would you choose?", (tourn_names['tourney_name']),disabled=False)
if selector=='Dusseldorf':
		selected=allfinals[allfinals['tourney_name']==selector][-2:] #There is a problem with this tournament, it was another type before 2013
else:
		selected=allfinals[allfinals['tourney_name']==selector]
mposition=list(selected['winner_age']).index(min(selected['winner_age']))
lat=list(tourneys_loc.Latitude[(tourneys_loc['Name']==selector)])
long=list(tourneys_loc['Longitude'][(tourneys_loc['Name']==selector)])
cat_flag=list(tourneys_loc[(tourneys_loc['Name']==selector)]['Level'])
if not cat_flag:
		category='ATP250' #This is to bypass COVID tournaments with numbers
elif cat_flag[0]=="F":
		category='Finals'
elif cat_flag[0]=='GS':
		category='Grand Slam'	
elif cat_flag[0]=='T':
		category='Teams'		
else:
		category='ATP' + cat_flag[0]
if not lat:
		lat=list(tourneys_loc.Latitude[(tourneys_loc['Name']==selector[:-2])])
		long=list(tourneys_loc['Longitude'][(tourneys_loc['Name']==selector[:-2])])
row1 = st.columns([1, 1],gap='small', vertical_alignment='center')

with row1[0]:
		m=folium.Map(location=[lat[0],long[0]],tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', zoom_start=16,max_bounds=False,min_zoom=2,min_lat=-60,max_lat=60, min_lon=-200,	attr= 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community') 
		st_folium (m,width=800,height=400)
with row1[1]:
		with st.container(border=True):
			cl1, cl2 = st.columns(2)
			cl1.header(f':red[{selector}]', divider='rainbow')
			cl2.header(category, divider='rainbow')
			col1, col2, col3 = st.columns(3)
			col1.metric(label='Years Played', value=str(len(selected)))
			col2.metric(label='Surface', value=' & '.join(list(set(selected['surface']))))           
			col3.metric(label='Youngest winner', value=selected['winner_name'].iloc[mposition], delta=min(selected['winner_age']))
row2 = st.container(border=False)
with row2:

	a=st.columns(3)
	with a[0]:	
		selected['Years']=selected['tourney_id'].str[:4]
		fig1 = px.bar(selected, y='winner_name', color='surface', hover_data={'Years':True,'loser_name':True},color_discrete_sequence=['#8dd3c7', '#ffffb3', '#bebada', '#fb8072'])
		fig1.update_layout(xaxis_title='', yaxis_title='', xaxis_tickfont=dict(size=11), yaxis_tickfont=dict(size=12), bargap=0.05)
		fig1.update_traces(hovertemplate='<b>Year</b>: %{customdata[0]}<br><b>Finalist</b>: %{customdata[1]}<extra></extra>')
		st.plotly_chart(fig1)
	with a[1]:
		fig2 = px.bar(selected, x='winner_ioc', color='surface', hover_data={'winner_name':True,'Years':True},color_discrete_sequence=['#8dd3c7', '#ffffb3', '#bebada', '#fb8072'])
		fig2.update_layout(xaxis_title='', yaxis_title='',  xaxis_tickfont=dict(size=11), yaxis_tickfont=dict(size=11), bargap=0.05)
		fig2.update_traces(hovertemplate='<b>Winner</b>: %{customdata[0]}<br><b>Year</b>: %{customdata[1]}<extra></extra>')
		st.plotly_chart(fig2)
	with a[2]:
		selected=selected.sort_values(['Years'])
		fig3 = px.bar(selected, y='Years', x='minutes',color='surface',hover_data={'score':True,'minutes':True}, color_discrete_sequence=['#8dd3c7', '#ffffb3', '#bebada', '#fb8072'])
		fig3.update_layout(xaxis_title='', yaxis_title='',  xaxis_tickfont=dict(size=11), yaxis_tickfont=dict(size=11), bargap=0.05,yaxis={'type': 'category'})
		fig3.update_traces(hovertemplate='<b>Final score</b>: %{customdata[0]}<br><b>Final duration</b>: %{x}<extra></extra>')
		st.plotly_chart(fig3)

