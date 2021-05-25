# importing the module
import pandas as pd
import csv
import datetime
import matplotlib.pyplot as plt
#matplotlib%inline

df = pd.read_csv("uber.csv")
print(df.head())
  
# counting the duplicates
dups = df.pivot_table(index = ['timestamp'], aggfunc ='size')
  
# displaying the duplicate Series
print(dups)

dfnew = pd.DataFrame({'timestamp':dups.index, 'frequency':dups.values})
#dfnew.to_csv('uberfreq.csv')

print(dfnew.head())
lines = dfnew.plot.line()

dfnew2 = dfnew.copy().set_index('timestamp')
print(dfnew2.head())
dfnew.to_csv('uberfreq2.csv')

#df.set_index('timestamp', inplace=True)
'''
def CountFrequency(my_list):
  
    # Creating an empty dictionary 
    freq = {}
    dfnew = pd.DataFrame({'timestamp' : [], 'frequency' : []})
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
  
    for date, value in freq.items():
        print ("% s : % d"%(date, value))
        dfwalk = {'timestamp' : date, 'frequency' : value}
        dfnew = df.append(dfwalk, ignore_index=True)
        dfwalk = {}
    
    dfnew.to_csv('uberfreq.csv')    
    return dfnew
  
# Driver function
if __name__ == "__main__": 
    dfcol = df['timestamp']
  
    CountFrequency(dfcol)
'''