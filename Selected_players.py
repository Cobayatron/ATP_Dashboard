import pandas as pd

anos_list=[]
for i in range(1998,2025):
    ano=pd.read_csv(f'Data/atp_matches_{i}.csv')
    anos_list.append(ano)
all=pd.concat(anos_list)    
# Drop Davies Cup matches
all=all[all['tourney_level']!='D']
winners=all[['winner_id']].drop_duplicates()
losers=all[['loser_id']].drop_duplicates()

allplayers=pd.read_csv('Data/atp_players.csv')
selectedplayers = allplayers[allplayers['player_id'].isin(winners['winner_id'])]
selectedplayers.to_csv('Data/selectedplayers.csv',index=False)


   