#import all necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium


st.set_page_config(layout="wide")
initial_sidebar_state="hidden" #this seems not to work
st.logo ('Data/ATP.png',size='large')


with st.sidebar:
    
        
    selector=st.selectbox("Which year are you interested in?", list(range(1998,2025)),disabled=False)
st.title(f'Summary of the ATP :blue[{selector}]  winners')
data=pd.read_csv(f'Data/atp_matches_{selector}.csv')

with st.container(border=True):
    row=st.columns([1, 1, 1, 1],gap='small', vertical_alignment='top')
    with row[0]:
        st.header('Australian Open',divider='rainbow')
        auswinner_name = data.loc[(data['tourney_id'].str[-3:] == '580') & (data['round'] == 'F'), 'winner_name'].values[0]
        st.subheader(auswinner_name)
    with row[1]:
        st.header('Roland Garros',divider='rainbow')
        rrwinner_name = data.loc[(data['tourney_id'].str[-3:] == '520') & (data['round'] == 'F'), 'winner_name'].values[0]
        st.subheader(rrwinner_name)
    with row[2]:
        st.header('Wimbledon',divider='rainbow')
        if any(data['tourney_name']=='Wimbledon'):
            wwinner_name = data.loc[(data['tourney_id'].str[-3:] == '540') & (data['round'] == 'F'), 'winner_name'].values[0]
        else:
            wwinner_name='Not played'
        st.subheader(wwinner_name)
    with row[3]:
        st.header('US Open',divider='rainbow')
        uswinner_name = data.loc[(data['tourney_id'].str[-3:] == '560') & (data['round'] == 'F'), 'winner_name'].values[0]
        st.subheader(uswinner_name)
row2=st.columns([1,1],gap='small',vertical_alignment='center')

#Some calculations to generate interesting data
winners=pd.DataFrame(data[(data['tourney_level']!='D')]['winner_name'].value_counts()).reset_index()
winners.columns = ['player_name', 'wins']
losers=pd.DataFrame(data[(data['tourney_level']!='D')]['loser_name'].value_counts()).reset_index()
losers.columns=['player_name', 'loses']
performance = winners.merge(losers, on='player_name', how='left')
ratio=[]
for i in range(len(performance)):
    ratio.append(performance.wins[i] / (performance.wins[i] + performance.loses[i]))
performance['ratio']=ratio
b=performance.sort_values(by=['wins','ratio'],ascending=False,ignore_index=True)
b1=performance.sort_values(by=['ratio'],ascending=False,ignore_index=True)

winners_all=pd.DataFrame(data[(data['tourney_level']!='D') & (data['round']=='F')]['winner_name'].value_counts()).reset_index()
winners_m=data[((data['tourney_level']=='M') | (data['tourney_level']=='F')) & (data['round']=='F')]
winners_t=data[(data['tourney_level']=='A') & (data['round']=='F')]
if any(winners_m['tourney_name']=='NextGen Finals'):
    winners_t=pd.concat([winners_t, winners_m[winners_m['tourney_name']=='NextGen Finals']])
    winners_m = winners_m[winners_m['tourney_name'] != 'NextGen Finals']


masterData=data[((data['tourney_level']=='M') | (data['tourney_level']=='F')) & ((data['round']=='F') | (data['round']=='SF'))]
masterData = masterData.drop(masterData[masterData.tourney_name== 'NextGen Finals'].index)
Unames=pd.unique(winners_m['winner_name'])
winners=pd.DataFrame(np.identity(len(winners_m),dtype=int)*100)

if len(Unames)<10:
    occ=[0]*len(Unames)
    for i in range(len(Unames)):
        occ[i]=pd.array((Unames[i]==winners_m['winner_name'])*100)
    winners=occ

for i in range(len(Unames)):
        A=np.array(Unames[i]==masterData[(masterData['round']=='F')]['loser_name'])*50
        B1=np.array(Unames[i]==masterData[(masterData['round']=='SF')]['loser_name'][::2])*25    
        B2=np.array(Unames[i]==masterData[(masterData['round']=='SF')]['loser_name'][1::2])*25    
   
        winners[i]=winners[i]+A+B1+B2

with row2[1]:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3,gap='small')
        col1.metric(label='Most wins',value=b.player_name[0],delta=int(b['wins'][0]))
        col2.metric(label='Best +/-',value=b1.player_name[0],delta=str(str(round(b1.ratio[0]*100,2)) + '%'))
        col3.metric(label='Most Tournaments',value=winners_all.winner_name[0],delta=int(winners_all['count'][0]))
with row2[0]:
    
    fig1, axs = plt.subplots()
    fig1=px.imshow(winners,labels=dict(x="", y="", color="Performance"),x=winners_m['tourney_name'], y=Unames ,color_continuous_scale='sunset')
    st.plotly_chart(fig1)
with st.columns([1,1,1])[1]:
    st.header(':red[Other ATP winners]')

    


fig2 = px.bar(winners_t, x='winner_name', color='surface', hover_data={'tourney_name':True,'winner_name':False, 'surface':False},color_discrete_sequence=['#8dd3c7', '#ffffb3', '#bebada', '#fb8072'])
fig2.update_layout(xaxis_title='', yaxis_title='', xaxis_tickangle=80, xaxis_tickfont=dict(size=14), yaxis_tickfont=dict(size=12), bargap=0.05)
fig2.update_traces(hovertemplate='<b>Tournament</b>: %{customdata[0]}<extra></extra>')
fig2.update_yaxes(tickmode='linear', tick0=0, dtick=1)

st.plotly_chart(fig2)