"""
Created on Tue Feb 23 20:04:19 2021

@author: cm

Skript for visualising results. 

"""

from Squad_List import *
import pandas as pd
import numpy as np

#%% Functions

def unique_name(list1):
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    for nr, element in enumerate(unique_list):
        element = str(element).strip('\n\\n')
        unique_list[nr] = element
    return unique_list
        

#%% Import data from Google Drive


# Load the data
df_all = pd.read_csv('C:/Users/cm/Google Drive/ComunioBot/Database_ComunioBot.csv')

raw_data = df_all.to_numpy()
attributeNames = np.asarray(df_all.columns)


#%% devide into matchdays

# look at mean of days points, if mean did not change, then there was no matchday

# find all data of one import day
matchday = 4    # start matchday
matchday_vector = np.zeros(len(raw_data))



daily_variation = 200

daypointer = 0

first_date = raw_data[daypointer,0]

indices = raw_data[:,0]==first_date  # get all the instances where the player occured
one_day = raw_data[indices,:]

pts_mean_first = np.mean(one_day[:,3])
pts_sum_first = np.sum(one_day[:,3])
daypointer = daypointer + len(one_day)

while (daypointer < len(raw_data)):
    date = raw_data[daypointer,0]
    indices = raw_data[:,0]==date  # get all the instances where the player occured
    one_day = raw_data[indices,:]
    pts_mean_next = np.mean(one_day[:,3])
    pts_sum_next = np.sum(one_day[:,3])
    
    
    
    if (pts_sum_next> pts_sum_first  + daily_variation ):
        matchday = matchday+1
        delta = pts_sum_first-pts_sum_next
        # print(delta)    # for defining daily variation
    
    matchday_vector[indices] = matchday
    
    pts_sum_first = pts_sum_next
    pts_mean_first != pts_mean_next
    daypointer = daypointer + len(one_day)

# Add matchday vector to data

# As pandas dataframe
matchdays_df = pd.DataFrame(matchday_vector, columns = ['Matchday'])
df_all = pd.concat([df_all, matchdays_df], axis=1)

# As numpy array
raw_data = df_all.to_numpy()
attributeNames = np.asarray(df_all.columns)



#%% Define Players 

PlayerNames = ['sigh']


#%% Market Value

marketplot = plt.figure(figsize=[10,7.5])

for PlayerName in PlayerNames:

    indices = [index for index, name in enumerate(raw_data[:,1]) if PlayerName in name] # get all the instances where the player occured
    Player = raw_data[indices,:] # whole data
    Name = unique_name((Player[:,1])) 
    if len(Name)==1:
    # tranform date from string to datetime
        xvalue = [datetime.strptime(date, '%Y-%m-%d').date() for date in Player[:,0]]
        yvalue = Player[:,4]*(1e-6) # mio
        plt.plot(xvalue,yvalue, '-x', label = Name[0])
    elif len(Name) > 1 :
        # devide the Names again
        for oneName in Name:
            indices = [index for index, name in enumerate(raw_data[:,1]) if oneName in name] # get all the instances where the player occured
            Player = raw_data[indices,:] #whole data
            xvalue = [datetime.strptime(date, '%Y-%m-%d').date() for date in Player[:,0]]
            yvalue = Player[:,4]*(1e-6) # mio
            plt.plot(xvalue,yvalue, '-x', label = oneName)
            
    else:
        print('Did not make plot for Name: ', PlayerName)    

plt.xlabel('Date')
plt.ylabel('Price in mio')
plt.title('Market Value')
plt.legend()
plt.grid()
plt.show()


#%% Points

pointsplot = plt.figure(figsize=[10,7.5])

for PlayerName in PlayerNames:

    indices = [index for index, name in enumerate(raw_data[:,1]) if PlayerName in name] # get all the instances where the player occured
    Player = raw_data[indices,:] # whole data
    Name = unique_name((Player[:,1])) 
    # if there is only one player with that name
    if len(Name)==1:
    # tranform date from string to datetime
        xvalue = matchday_vector[indices]
        yvalue = Player[:,3] # points
        plt.plot(xvalue, yvalue, '-x', label = Name[0])
    # if there is more players with the same name
    elif len(Name) > 1 :
        # devide the Names again
        for oneName in Name:
            indices = [index for index, name in enumerate(raw_data[:,1]) if oneName in name] # get all the instances where the player occured
            Player = raw_data[indices,:] #whole data
            xvalue = matchday_vector[indices]
            yvalue = Player[:,3]  # Points
            plt.plot(xvalue,yvalue, '-x', label = oneName)
            
    else:
        print('Did not make plot for Name: ', PlayerName)    

plt.xlabel('Matchday')
plt.ylabel('Points')
plt.title('Points')
plt.legend()
plt.grid()
plt.show()