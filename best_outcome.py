import pandas as pd
import numpy as np
def best_results(df):
    df['Rating']=df['Rating'].replace('No_Rating','0.0')
    df['Rating']=df['Rating'].astype(float)
    df['Rated_By']=df['Rated_By'].astype(int)
    df['Currency']=df['Bus_Fare'].str[:].str[:4]
    df['Bus_Fare']=df['Bus_Fare'].str.split('\s+').str[-1]
    df['Final_Price']=df['Final_Price'].str.split('\s+').str[-1]
    df['Bus_Fare']=df['Bus_Fare'].astype(int)
    df['Final_Price']=df['Final_Price'].astype(int)
    df['Cost_decreses']=df['Bus_Fare']-df['Final_Price']
    df['Seats_Available']=df['Seats_Available'].str.split('\s+').str[0]
    df['Seats_Available']=df['Seats_Available'].astype(int)
    df['Total_Duration1'] = df['Total_Duration'].str.split('h').str[0] + ':' + df['Total_Duration'].str.split('m').str[
                                                                                   0].str[4:]
    df['hour'] = df['Total_Duration1'].str[:].str[:2]
    df['min'] = df['Total_Duration'].str[:].str[3:6]
    df['hour'] = df['hour'].astype(int)
    df['min'] = df['min'].astype(int)
    df['Total_Duration1'] = df['hour'] * 60 + df['min']
    df['Time in Day'] = df['Starting_Time'].str[:].str[:2]
    df['Time in Day'] = df['Time in Day'].replace('00', 'Late Night')
    df['Time in Day'] = df['Time in Day'].replace('01', 'Late Night')
    df['Time in Day'] = df['Time in Day'].replace('02', 'Late Night')
    df['Time in Day'] = df['Time in Day'].replace('04', 'Late Night')
    df['Time in Day'] = df['Time in Day'].replace('05', 'Early Morning')
    df['Time in Day'] = df['Time in Day'].replace('06', 'Early Morning')
    df['Time in Day'] = df['Time in Day'].replace('07', 'Early Morning')
    df['Time in Day'] = df['Time in Day'].replace('08', 'Morning')
    df['Time in Day'] = df['Time in Day'].replace('09', 'Morning')
    df['Time in Day'] = df['Time in Day'].replace('10', 'Morning')
    df['Time in Day'] = df['Time in Day'].replace('11', 'Morning')
    df['Time in Day'] = df['Time in Day'].replace('12', 'Afternoon')
    df['Time in Day'] = df['Time in Day'].replace('13', 'Afternoon')
    df['Time in Day'] = df['Time in Day'].replace('14', 'Afternoon')
    df['Time in Day'] = df['Time in Day'].replace('15', 'Afternoon')
    df['Time in Day'] = df['Time in Day'].replace('16', 'Evening')
    df['Time in Day'] = df['Time in Day'].replace('17', 'Evening')
    df['Time in Day'] = df['Time in Day'].replace('18', 'Evening')
    df['Time in Day'] = df['Time in Day'].replace('19', 'Night')
    df['Time in Day'] = df['Time in Day'].replace('20', 'Night')
    df['Time in Day'] = df['Time in Day'].replace('21', 'Night')
    df['Time in Day'] = df['Time in Day'].replace('22', 'Night')
    df['Time in Day'] = df['Time in Day'].replace('23', 'Night')
    '''
    df['Time in Day'] =df['Time in Day'].astype(int)
    for i in range(0, len(df['Time in Day'])):
        if df['Time in Day'][i] <= int('04'):
            df['Time in Day'] = df['Time in Day'].replace(df['Time in Day'][i], 'Late Night')
        elif df['Time in Day'][i] <= int('07'):
            df['Time in Day'] = df['Time in Day'].replace(df['Time in Day'][i], 'Early Morning')
        elif df['Time in Day'][i] <= int('12'):
            df['Time in Day'] = df['Time in Day'].replace(df['Time in Day'][i], 'Morning')
        elif df['Time in Day'][i] <= int('15'):
            df['Time in Day'] = df['Time in Day'].replace(df['Time in Day'][i], 'Afternoon')
        elif df['Time in Day'][i] <= int('17'):
            df['Time in Day'] = df['Time in Day'].replace(df['Time in Day'][i], 'Evening')
        elif df['Time in Day'][i] <= int('23'):
            df['Time in Day'] = df['Time in Day'].replace(df['Time in Day'][i], 'Night')'''
    bins=np.linspace(min(df['Final_Price']),max(df['Final_Price']),4)
    group_name=['Low','Medium','High']
    df['Final_Binned']=pd.cut(df['Final_Price'],bins,labels=group_name,include_lowest=True)
    df['Rating_Value']=df['Rating']*df['Rated_By']
    bins=np.linspace(min(df['Rating_Value']),max(df['Rating_Value']),4)
    group_name=['Bad','Average','Good']
    df['Rating_Binned']=pd.cut(df['Rating_Value'],bins,labels=group_name,include_lowest=True)
    df['Rating_Binned']=df['Rating_Binned'].replace('Good',2)
    df['Rating_Binned']=df['Rating_Binned'].replace('Average',1)
    df['Rating_Binned']=df['Rating_Binned'].replace('Bad',0)
    df['Final_Binned']=df['Final_Binned'].replace('High',2)
    df['Final_Binned']=df['Final_Binned'].replace('Medium',1)
    df['Final_Binned']=df['Final_Binned'].replace('Low',0)
    df['Time in Day']=df['Time in Day'].replace('Night',4)
    df['Time in Day']=df['Time in Day'].replace('Late Night',5)
    df['Time in Day']=df['Time in Day'].replace('Morning',1)
    df['Time in Day']=df['Time in Day'].replace('Early Morning',0)
    df['Time in Day']=df['Time in Day'].replace('Afternoon',2)
    df['Time in Day']=df['Time in Day'].replace('Evening',3)
    bins=np.linspace(min(df['Total_Duration1']),max(df['Total_Duration1']),6)
    group_name=['Very Slow','Slow','Average','Fast','Super Fast']
    df['Duration_Binned']=pd.cut(df['Total_Duration1'],bins,labels=group_name[::-1],include_lowest=True)
    df['Duration_Binned']=df['Duration_Binned'].replace('Super Fast',4)
    df['Duration_Binned']=df['Duration_Binned'].replace('Fast',3)
    df['Duration_Binned']=df['Duration_Binned'].replace('Average',2)
    df['Duration_Binned']=df['Duration_Binned'].replace('Slow',1)
    df['Duration_Binned']=df['Duration_Binned'].replace('Very Slow',0)
    df['Final_Binned'] = df['Final_Binned'].astype(int)
    df['Rating_Binned'] = df['Rating_Binned'].astype(int)
    df['Duration_Binned'] = df['Duration_Binned'].astype(int)
    return(df)

