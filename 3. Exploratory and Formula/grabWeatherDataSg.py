import pandas as pd
import requests as rq
import sys, os, re, time

from datetime import datetime


def chkDateFormatOk(string):
    return(re.match('^\d{4}-\d{2}$', string) is not None)

def parseDate(string):
    return(string.split('-'))

def grabData(year, month, paList, homePath, url):
    paList = pd.read_csv(os.path.join(homePath, paList))
    year = str(year)
    month = str(month)
    data = pd.DataFrame()
    
    if len(month) < 2:
        month = "0" + month
    
    for i in range(len(paList)):
        print(paList.iloc[i, 1])
        
        areaNum = str(paList.iloc[i, 0])
        
        if len(areaNum) < 2:
            areaNum = "0" + areaNum
            
        csvFile = url + "/DAILYDATA_S" + areaNum + "_" + year + str(month) + ".csv"
        
        time.sleep(1)   # suspect MSS ftp server download unable to respond in time
        
        temp = rq.get(csvFile).content.decode('unicode_escape')
        temp = temp.replace('\xc2', '')
        temp = temp.replace('\xef\xbb\xbf', '')
        temp = temp.replace('\x97', '')
        temp = temp.replace('-', '')
        
        # No data, skip
        if re.search('<!DOCTYPE html>', temp) is not None:
            print(paList.iloc[i, 1] + '...No data, skip')
            continue
        
        temp = temp.splitlines()
        
        tempList = []
        
        for j in range(1, len(temp)):
            line = temp[j].split(',')
            tempList.append(line)
            
        tempTable = pd.DataFrame(tempList, columns = temp[0].split(','))
        data = pd.concat([data, tempTable])
        
        # Strip leading and trailing whitespaces from cell values
        for c in data.columns:
            data[c] = data[c].str.strip()
        
        print(paList.iloc[i, 1] + '...Done')
    
    return(data)

    

if __name__ == "__main__":
    if len(sys.argv) < 3:
        startYear, startMonth = 2010, 1
        endYear, endMonth = datetime.now().year, datetime.now().month
    
    else:
        if len(sys.argv) == 3:
            if not chkDateFormatOk(sys.argv[2]):
                sys.exit('Wrong date format provided!')
                
            endYear, endMonth = datetime.now().year, datetime.now().month
                
        if len(sys.argv) == 4:
            if not chkDateFormatOk(sys.argv[2]) or not chkDateFormatOk(sys.argv[3]):
                sys.exit('Wrong date format provided!')
                
            endYear, endMonth = parseDate(sys.argv[3])
            
        startYear, startMonth = parseDate(sys.argv[2])
        
        startYear = int(startYear)
        startMonth = int(startMonth)
        endYear = int(endYear)
        endMonth = int(endMonth)
        
        if startYear < 1980:
            sys.exit('Start year is less than 1980!')
            
        else:
            if startYear > endYear:
                sys.exit('Start year is greater than end year!')
            
            else:
                if startMonth > endMonth:
                    sys.exit('Start month is greater than end month!')
                    
    if len(sys.argv) >= 2:
        paList = sys.argv[1]
        
    else:
        paList = "paList.csv"   # list of weather stations
        
    homePath = os.path.dirname(__file__)
    
    allData = pd.DataFrame()
    
    if startYear == endYear:
        for j in range(startMonth, endMonth + 1):
            print('Grabbing data for ' + str(startYear) + '-' + str(j))
            dt = grabData(year = startYear, 
                          month = j, 
                          paList = paList, 
                          homePath = homePath, 
                          url = 'http://www.weather.gov.sg/files/dailydata/')
            
            allData = pd.concat([allData, dt])
            
            print('Grabbing data for ' + str(startYear) + '-' + str(j) + '...Done')
            
    else:
        for j in range(startMonth, 13):
            print('Grabbing data for ' + str(startYear) + '-' + str(j))
            dt = grabData(year = startYear, 
                          month = j, 
                          paList = paList, 
                          homePath = homePath, 
                          url = 'http://www.weather.gov.sg/files/dailydata/')
            
            allData = pd.concat([allData, dt])
            
            print('Grabbing data for ' + str(startYear) + '-' + str(j) + '...Done')
            
        for i in range(startYear + 1, endYear):
            for j in range(1, 13):
                print('Grabbing data for ' + str(i) + '-' + str(j))
                dt = grabData(year = i, 
                              month = j, 
                              paList = paList, 
                              homePath = homePath, 
                              url = 'http://www.weather.gov.sg/files/dailydata/')
                
                allData = pd.concat([allData, dt])
                
                print('Grabbing data for ' + str(i) + '-' + str(j) + '...Done')
                
        for j in range(1, endMonth + 1):
            print('Grabbing data for ' + str(endYear) + '-' + str(j))
            dt = grabData(year = endYear, 
                          month = j, 
                          paList = paList, 
                          homePath = homePath, 
                          url = 'http://www.weather.gov.sg/files/dailydata/')
            
            allData = pd.concat([allData, dt])
            
            print('Grabbing data for ' + str(endYear) + '-' + str(j) + '...Done')
            
    allData.to_csv(os.path.join(homePath, 'sgWeatherData.csv'), index = False)
    
    print('Download done, see file: ' + 'sgWeatherData.csv' + ' in ' + homePath)
    
    
    
    
    