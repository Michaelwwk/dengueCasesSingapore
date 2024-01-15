import pandas as pd
import numpy as np
import sys, os


def replaceRoundBracket(listLike):
    temp = list()
    
    for l in listLike:
        if "(" in l or ")" in l:
            l = l.replace('(', '')
            l = l.replace(')', '')
            
        temp.append(l)
        
    return(temp)
    
def cleanStrings(listLike):
    listLike = replaceRoundBracket(listLike)
    
    return(listLike)
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        pa = 'paListDoc.csv'
    
    elif len(sys.argv) == 2:
        pa = sys.argv[1]
        
    homePath = os.path.dirname(__file__)
    
    data = pd.read_csv(os.path.join(homePath, 'sgWeatherData.csv'))
    pa = pd.read_csv(os.path.join(homePath, pa))
    
    paPlanningArea = pa['Planning Area']
    paSubzone = pa['Subzone']
    
    stations = data['Station'].unique()
    
    tempStations = pd.Series(cleanStrings(stations))
    tempPa = paPlanningArea.unique()
    
    mList1 = ['Buangkok', 'Lower Peirce Reservoir', 'Macritchie Reservoir', 'Kampong Bahru', 'Jurong Pier', 
              'Chai Chee', 'Buona Vista', 'Pulau Ubin', 'Jurong (North)', 'Upper Peirce Reservoir', 
              'Botanic Garden', 'Marina Barrage', 'Nicoll Highway', 'Pasir Panjang', 'Whampoa', 'Jurong Island']
    mList2 = ['Sengkang', 'Central Water Catchment', 'Central Water Catchment', 'Bukit Merah', 'Boon Lay', 
              'Bedok', 'Queenstown', 'North-Eastern Islands', 'Jurong West', 'Central Water Catchment', 
              'Tanglin', 'Marina South', 'Downtown Core', 'Queenstown', 'Novena', 'Western Islands']
    
    data.insert(0, 'Planning Area', np.nan)
    
    print('Mapping subzones to planning areas...')
    for i in range(len(paSubzone)):
        try:
            fIndex = tempStations[tempStations.str.find(paSubzone[i]) != -1].index
            
        except ValueError:
            print('Subzone {} not found in dataframe!'.format(paSubzone[i]))
            
        else:
            print('Subzone {} found! Inserting value...'.format(paSubzone[i]))
            
            for idx in fIndex:
                data.loc[data['Station'] == stations[idx], 'Planning Area'] = paPlanningArea[i]
            
    print('Mapping planning areas directly to weather station...')
    for paName in tempPa:
        try:
            fIndex = tempStations[tempStations.str.find(paName) != -1].index
            
        except ValueError:
            print('Planning area {} not found as a weather station name!'.format(paName))
            
        else:
            print('Weather station {} found! Inserting value...'.format(paName))
            
            for idx in fIndex:
                data.loc[data['Planning Area'].isnull() & (data['Station'] == stations[idx]), 'Planning Area'] = paName
    
    for paName in tempPa:
        data.loc[data['Planning Area'].isnull() & (data['Station'].str.find(paName) != -1), 'Planning Area'] = paName
        
    for i in range(len(mList1)):
        data.loc[data['Planning Area'].isnull() & (data['Station'].str.find(mList1[i]) != -1), 'Planning Area'] = mList2[i]
    
    print('Cleaning complete!')
    
    data.to_csv(os.path.join(homePath, 'sgWeatherDataPa.csv'), index = False)
    print('Data saved as sgWeatherDataPa.csv')
    
    
    
    
    
    
    