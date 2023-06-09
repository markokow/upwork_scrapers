#import block
import requests   
##import request library - this is http for humans
from bs4 import BeautifulSoup
#import BeautifulSoup library
import pandas as pd
#import pandas for file read dataframe...
import time

#specify the file name and location
# file_path="paa-csvsearcha.csv"

#open the file to be read
# df=pd.read_csv(file_path, usecols =["query"],squeeze = True)

#block to create a dataframe
# key_search=list(df)
key_search=['best coffee here']
#create an empty output dictionary
output_csv={}
#creating dictionary output_csv...
key=1
##counter variable key for the dictionary...
max_ques_val=0
#block for a loop that goes through each keyword one by one and stores the output
for searchKey in key_search:
    page = 'https://www.google.com/search?q='+searchKey
    #url to be searched
    req = requests.get(page, headers={'User-Agent': 'Mozilla/5.0'})
    #avoid acting as a bot
    soup = BeautifulSoup(req.content,'html5lib')
    #soup object to parse the file
    print(soup)
    
#block to create an empty list called paa_list and look for content to be added that is within a certain div class
    paa_list=[]
    #create empty list
    div_tag=soup.find_all("div", {"class": "Lt3Tzc"})
    #find all data with div tag with class Lt3Tzc and store it in div_tag variable...
    for tags in div_tag:
        paa_list.append(tags.text)
        #add each element to the list.. 
    count=len(paa_list)
    #print(count)
    #count total elements...
    print("searched word:",searchKey)
    #print searched word on console...
    print("Questions fetched:\n",paa_list)
    #print questions fetched on console...
    print("\n")
    #next line
    if count == 1: 
            output_csv[key]=[searchKey, paa_list[0]]; 
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 2: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1]]; 
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 3: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2]]; 
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 4: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3]];
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 5: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3], paa_list[4]];
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 6: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3], paa_list[4], paa_list[5]];
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 7: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3], paa_list[4], paa_list[5], paa_list[6]];
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 8: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3], paa_list[4], paa_list[5], paa_list[4], paa_list[6], paa_list[7]];
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 9: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3], paa_list[4], paa_list[5], paa_list[6], paa_list[7], paa_list[8]];
            #check the count in the list and accordingly assign it to the dictionary
    elif  count == 10: 
            output_csv[key]=[searchKey, paa_list[0], paa_list[1], paa_list[2], paa_list[3], paa_list[4], paa_list[5], paa_list[6], paa_list[7], paa_list[8], paa_list[9]];
            #check the count in the list and accordingly assign it to the dictionary            
    else:
            print("more than 10 questions for a particular searched word...");
    key+=1
    #increment key...
    if count > max_ques_val:
        max_ques_val=count
        #update the max. value for the heading value...
    time.sleep(5)
    #sleep counter for 5 seconds...


#block that creates an output file
if  max_ques_val == 1: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1']); 
elif  max_ques_val == 2: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2']); 
elif  max_ques_val == 3: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3']); 
elif  max_ques_val == 4: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4']);
elif  max_ques_val == 5: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4', 'Question 5']);			
elif  max_ques_val == 6: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6']);
elif  max_ques_val == 7: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6', 'Question 7']);
elif  max_ques_val == 8: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6', 'Question 7', 'Question 8']);
elif  max_ques_val == 9: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6', 'Question 7', 'Question 8', 'Question 9']);
elif  max_ques_val == 10: 
        output_file_create = pd.DataFrame.from_dict(output_csv, orient = 'index', columns = ['Searched words','Question 1','Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6', 'Question 7', 'Question 8', 'Question 9', 'Question 10']);		
else: 
        print("... more than 10 questions for a particular searched word ...");

output_file_create.head()
#printing the head of output_file_create file...
output_file_create.to_csv('output_file.csv', encoding='utf-8-sig')
#exporting the output to the dataframe in output_file_create file...
print("Output file created successfully")
print("...script ended...")