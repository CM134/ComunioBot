# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 18:33:46 2020

@author: cm
"""

from Squad_List import *


# Load the data
df_imported = pd.read_csv('ClubScrape.csv')
    
# Compare time and from last update to now. 
# Load the last time

last_time_str = df_imported['Date'].iloc[-1]
last_time = datetime.strptime(last_time_str, '%Y-%m-%d').date()

# last_time = pickle.load(open('timestamp','rb'))
# get the time now and safe it in timestamp to be last_time when script executed next time
now = datetime.now().date()
# pickle.dump(now, open('timestamp','wb'))

# Comunio updates market value once per day
OneDay = timedelta(days=1)
# TimePassed =  OneDay # to import data of this day again if first run didnt work
TimePassed = now - last_time

#%% Test
df_all = df_imported
df = df_all
 
# # test list 
# data = [['tom', 'abw', '10',10000], ['nick', 'tor', '10',1000000015], ['juli', 'abw', '10',10000]] 
  
# # Create the pandas DataFrame 
# testframe = pd.DataFrame(data,columns=list(df.columns.values)) 

# newdf = df.append(testframe, ignore_index=True)

# insert a new column for daytime e.g.
# date = 'today'
# dateframe = newdf.insert(0,'Date',date)

# # Search for items in list template
# Tor_idx = df['Spieler'].str.contains('Lewandowski')
# Tor = df[Tor_idx]

# # file= open('variable_dump','wb')
# # pickle.dump(['Tor'],  open('variable_dump','wb') )

# file= open('variable_dump','rb')
# d= pickle.load(open('variable_dump','rb'))
# print(d)
# d.append('abw')
# a='test'

# pickle.dump(d,  open('variable_dump','wb') )
# d= pickle.load(open('variable_dump','rb'))
# print(d)


#%% Test plotting 


# # find player
# names = ['Tah','Lewandowski']
# Players = pd.DataFrame(columns = list(df_all.columns.values))
# # Search for items in list template
# # Player_idx = df['Spieler'].str.contains('Tah')
# for name in names:
#     Player_idx = df['Spieler'].str.contains(name)
#     Players = Players.append(df_all[Player_idx])
#%%  
# Players.plot()
# plt.show

# # plot marekt value to time 
# Players.plot(x='Date',y = 'Marktwert', kind='line', title = ('Market value of ' + 'Lewandowski'),
#             grid=True, xlabel = 'Date', ylabel = 'Market Value', style = 'x-', legend = True)
# plt.show()

#%% Start working with array instead of dataframes

# raw_data = df_all.to_numpy()


# # Extract the attribute names

# attributeNames = np.asarray(df_all.columns)

# # find players
# names = ['Tah','Lewandowski']

# indices = [index for index, name in enumerate(raw_data[:,1]) if 'Tah' in name]

# Player = raw_data[indices,:]

# # tranform date from string to datetime
# xvalue = [datetime.strptime(date, '%Y-%m-%d').date() for date in Player[:,0]]
# yvalue = Player[:,4]*(1e-6) # mio 
# marketplot = plt.figure()
# plt.plot(Player[:,0],yvalue, label = 'Tah')

# indices = [index for index, name in enumerate(raw_data[:,1]) if 'Lewandowski' in name]

# Player = raw_data[indices,:]

# # tranform date from string to datetime
# xvalue = [datetime.strptime(date, '%Y-%m-%d').date() for date in Player[:,0]]
# yvalue = Player[:,4]*(1e-6) # mio 
# plt.plot(Player[:,0], yvalue, label='Lewandowski')

# plt.xlabel('Date')
# plt.ylabel('Price in mio')
# plt.title('Market Value')
# plt.legend()
# plt.grid()
# plt.show()

#%%

def unique_name(list1):
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    for nr, element in enumerate(unique_list):
        element = str(element).strip('\n\\n')
        unique_list[nr] = element
    return unique_list
        

raw_data = df_all.to_numpy()
attributeNames = np.asarray(df_all.columns)
# find players
PlayerNames = ['Thuram','Kramer','Stindl','Musiala']
marketplot = plt.figure(figsize=[10,7.5])
for PlayerName in PlayerNames:

    indices = [index for index, name in enumerate(raw_data[:,1]) if PlayerName in name] # get all the instances where the player occured
    Player = raw_data[indices,:] #whole data
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


#%% Delete doublicates

# df_all = pd.read_csv('ClubScrape.csv')

# duplicate_idx = df_all.duplicated()
# duplicate = df_all[duplicate_idx]

# df_cleaned = df_all.drop_duplicates()
# df_cleaned.to_csv('ClubScrape.csv', index = None)
