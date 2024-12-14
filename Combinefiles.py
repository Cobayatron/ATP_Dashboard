import pandas as pd
def Combinefiles (year1,year2):
    anos_list=[]
    for i in range(year1,year2):
        ano=pd.read_csv(f'../Data/atp_matches_{i}.csv')
        anos_list.append(ano)
    all=pd.concat(anos_list)    
    return(all)