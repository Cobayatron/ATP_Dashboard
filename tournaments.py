import pandas as pd

anos_list=[]
for i in range(1998,2025):
        ano=pd.read_csv(f'Data/atp_matches_{i}.csv')
        anos_list.append(ano)
all=pd.concat(anos_list)
# Drop Davies Cup matches
all=all[all['tourney_level']!='D']
all=all[all['tourney_level']!='O']
allfinals=all[all['round']=='F']   
allfinals=allfinals.sort_values(by='tourney_name') 
allfinals.to_csv('Data/Alltournaments.csv',index=False)