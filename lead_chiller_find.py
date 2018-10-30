#!/usr/bin/env python3


##----------------------------------------------------------------------------
#--------------------------- FINDING LEAD CHILLER ----------------------------
#VERSION        : 1
##----------------------------------------------------------------------------


# Importing Libraries
import pandas as pd
from statistics import *
from datetime import datetime
import numpy as np
import json
import sys


output_passed= {}


try: #File_Input
    file_path= str(sys.argv[1])
    df= pd.read_csv(file_path)
    df.iloc[0:,0]= pd.to_datetime(df.iloc[0:,0], dayfirst=True)
    timestamp= df.iloc[0:,0].dt.strftime("%d-%m-%Y %H:%M").tolist()    
    
    try: #Off_Value Input
        input_data= sys.argv[2]
        input_json= json.loads(input_data)  
        off_val= np.float(input_json["input"][0])        
        
    except: #Off_Value Input: Error Handling by taking default values
        off_val = 0
        
        
    try: #Weightage_Percentage Input
        per_weight= list(map(float,input_json["input"][1]))
        if ((np.sum(np.array(per_weight))) == 1): #checking whether sum of all percentage is equals to 1 or not
            
            
            try: #Computation Block
                
                # finding no. of chiller's & separating their data
                chiller_count= len(df.columns) - 2  #as last col. is for total & first column for date
                #print (chiller_count)
                chiller_data= []
                for chiller in range(1,chiller_count+1):
                    data_list= df.iloc[0:,chiller].tolist()
                    chiller_data.append(data_list)
                #print(chiller_data)    
                
                
                # sum of all chiller
                total_reading= df.iloc[0:,chiller_count+1].tolist()
                total_reading= np.sum(np.array(total_reading))
                
                # calculating the interval in which entries are made
                x=datetime.strptime(timestamp[0],'%d-%m-%Y %H:%M')
                y=datetime.strptime(timestamp[1],'%d-%m-%Y %H:%M')
                day_entries= int((3600/(y-x).total_seconds())*24) #1 day selecting
        
            
                #---------------------------------------------------------------------------------------
                
                
                # function computing each chiller overall output
                def chiller_overview(benchmark, recorded_data):
                    # recorded_data's dictionary create
                    i=0
                    data_dict= {}
                    for data in recorded_data:
                       data_dict[i]= data
                       i+=1           
                           
                           
                    # sorting data's which are less than the off-value
                    off_list = [data for data in recorded_data if (data <= benchmark)]
                        
                    
                    # converting a dictionary into tuple | creating val_dict | creating r_index & f_index
                    # finding no. of cycles for a particular off-value
                    data_tuple= data_dict.items()
                    
                    r_index= []
                    f_index= []
                    val_dict={}
                    len_cycle= []
                    output_data= []
                    energy_use= []
                    peak_stats= []
                            
                           
                    # to combat repeating values which exists in a dataset. [Eg: 32.58 existing at indices- 5, 18, 55 etc]
                    # this is so that correct indices is fed despite of values being in repeatition.
                    for value in off_list:
                        rep_index= []
                        for tupl in data_tuple:
                            if (value==tupl[1] ):
                                rep_index.append(tupl[0])               
                            val_dict[value]=rep_index
                                
                                
                    # constructing f_index    
                    for value in off_list:
                        r_index.append(val_dict[value][0])
                        val_dict[value].remove(val_dict[value][0])      
                    
                    if(len(r_index) != 0):
                        for i in range(len(r_index)-1):
                            if((r_index[i+1]-r_index[i]) != 1):
                                f_index.append((r_index[i]+1, r_index[i+1]-1))            
                    else:
                        f_index= []
                            
                            
                    # constructing array of :: cycles duration & interval b/w cycles 
                    if ((len(f_index) > 1)):
                        for index in range(len(f_index)-1):
                            len_cycle.append(f_index[index][1]-f_index[index][0]+1)
                        len_cycle.append((f_index[-1][1]-f_index[-1][0])+1)  #+1 as both the points are included          
                    
                    elif (len(f_index) == 1):
                        len_cycle.append(f_index[0][1]-f_index[0][0]+1)
                    
                    else:
                        len_cycle.append(0)
                            
                            
                    # inserting- energy consumption , peak max, min & difference
                    for each in f_index:
                        sample= []
                        for point in recorded_data[each[0]: each[1]+1]:
                            sample.append(point)
                        sample= np.array(sample)
                        energy_use.append(np.sum(sample))
                        peak_stats.append((np.max(sample), np.min(sample), np.max(sample) - np.min(sample)))
                        
                            
                    # inserting the output in output dictionary
                    output_data= [benchmark, len(f_index), f_index, len_cycle, peak_stats, energy_use] 
                    output_data[3] = np.array(output_data[3])  #cycle_duration    
                    output_data[-1]= np.array(output_data[-1]) #energy_consumption
                    
                            
                    # overview output
                    overview_output= []
                    if (len(f_index) != 0) :
                        overview_output.append(np.sum(output_data[-1]))  #energy consumption
                        overview_output.append(np.sum(output_data[3]))   #total duration
                        overview_output.append(np.max(output_data[3]))   #max duration
                        overview_output.append(np.mean(output_data[3]))  #avg duration
                        overview_output.append(output_data[1])           #cycles count
                        
                    else:
                        bool_output= np.array(np.array(recorded_data) >= benchmark)
                        true_count= np.sum(bool_output)
                        if (true_count == 0):
                            overview_output.append(0)  #energy consumption
                            overview_output.append(0)  #total duration
                            overview_output.append(0)  #max duration
                            overview_output.append(0)  #avg duration
                            overview_output.append("Comment_3,refer_codebook")  #All data below Off- Value, representing cycles count
                            
                        elif (true_count == len(df)):
                            overview_output.append(np.sum(np.array(recorded_data)))  #energy consumption
                            overview_output.append(len(df))  #total duration 
                            overview_output.append(len(df))  #max duration
                            overview_output.append(len(df))  #avg duration
                            overview_output.append("Comment_4,refer_codebook")  #All data above Off- Value, representing cycles count
                
                        else:
                            overview_output.append("Contact Data Analyst by sending the Off- Value you entered.")
                            
                    return (overview_output)
                
                        
                #---------------------------------------------------------------------------------------
                
                        
                # segregating for each chiller:
                rank_dict= {}
                chiller_dict= {}
                total_running_hrs= []
                max_running_hrs= []
                percentage_contribution= []
                cycles_count= []
                avg_running_hrs= []
                
                #print(rank_dict)
                index= 1
                for each_chiller in chiller_data:
                    function_output= chiller_overview(off_val, each_chiller)
                    #print(function_output)
                    percentage_contribution.append(function_output[0] / total_reading)
                    total_running_hrs.append(function_output[1])
                    max_running_hrs.append(function_output[2])
                    cycles_count.append(function_output[4])
                    avg_running_hrs.append(function_output[3])
                    chiller_dict[index] = [total_running_hrs[index-1], max_running_hrs[index-1], percentage_contribution[index-1], avg_running_hrs[index-1], cycles_count[index-1]]
                    rank_dict[index]= []
                    index+= 1
                
                #print (rank_dict)
                #print (chiller_dict)
                
                
                
                # calculating the rank for each category:
                
                #set creation- finding unique values
                unique_running_hrs= set(total_running_hrs)
                unique_max_running= set(max_running_hrs)
                unique_percentange= set(percentage_contribution)
                #print (unique_running_hrs, unique_max_running, unique_percentange)
                
                
                #sorting the unique 
                total_running_hrs= [val for val in unique_running_hrs ]
                total_running_hrs.sort(reverse= True)
                max_running_hrs= [val for val in unique_max_running ]
                max_running_hrs.sort(reverse= True)
                percentage_contribution= [val for val in unique_percentange ]
                percentage_contribution.sort(reverse= True)
                
                
                #storing ranks of each chiller in the chiller dictionary
                th_rank= 1  #total running hrs ranking
                for each_value in total_running_hrs:
                    for each_key in chiller_dict:
                        if (each_value == chiller_dict[each_key][0]):
                            rank_dict[each_key].append(th_rank)
                    th_rank+= 1 
                    
                mh_rank= 1  #maximum running hrs ranking
                for each_value in max_running_hrs:
                    for each_key in chiller_dict:
                        if (each_value == chiller_dict[each_key][1]):
                            rank_dict[each_key].append(mh_rank)
                    mh_rank+= 1    
                
                p_rank= 1  #percentage contribution ranking
                for each_value in percentage_contribution:
                    for each_key in chiller_dict:
                        if (each_value == chiller_dict[each_key][2]):
                            rank_dict[each_key].append(p_rank)
                    p_rank+= 1    
                #print(rank_dict)
                
                
                #computing average score 
                for each_key in rank_dict:
                    #rank_dict[each_key] = (rank_dict[each_key][0] * 0.40) + (rank_dict[each_key][1] * 0.40) + (rank_dict[each_key][2] * 0.20)
                    rank_dict[each_key] = round(((rank_dict[each_key][0] * per_weight[0]) + (rank_dict[each_key][1] * per_weight[1]) + (rank_dict[each_key][-1] * per_weight[2])), 2)
                
                
                #finding the lead chiller
                chiller_avg_score= [each_score for each_score in rank_dict.values()]
                chiller_avg_score.sort()
                lead_chiller_list= []
                for key in rank_dict:
                    if (rank_dict[key] == chiller_avg_score[0]):
                        lead_chiller_list.append(key)   
                #print(lead_chiller_list)
                
                
                #printing the insights of each chiller
                all_chiller_dict= {}
                all_chiller_dict["Chiller_Data"]= []
                for key in chiller_dict:
                    key_dict= {}
                    key_dict["Chiller_No"]= key
                    for item in lead_chiller_list:
                        if (key==item):
                            key_dict["Status"]= "Lead"
                            break
                        else:
                            key_dict["Status"]= "No-Lead"
                    key_dict["Total_Cycles"]= chiller_dict[key][4]
                    key_dict["Total_Duration_in_mins"]= float(round(chiller_dict[key][0]*(1440/day_entries), 2))
                    key_dict["Maximum_Duration_in_mins"]= float(round(chiller_dict[key][1]*(1440/day_entries), 2))
                    key_dict["Average_Duration_in_mins"]= float(round(chiller_dict[key][3]*(1440/day_entries), 2))
                    key_dict["Percentage_contribution_in_Total_Energy_in_%"]= float(round(chiller_dict[key][2]*100, 2))
                    all_chiller_dict["Chiller_Data"].append(key_dict)
                    
                
                output_passed["status"]= "success"
                output_passed["message"]= ""
                output_passed["data"]= all_chiller_dict
                output_passed["code"]= 200    
            
                
            except: #Computation Block: Error Handling
                output_passed["status"]= "error"
                output_passed["message"]= "Computation Error. Change Off-Value & Retry"
                output_passed["data"]= ""
                output_passed["code"]= 401    
                
            
        else: #Sum_of_Percentages Input: Error Handling
            output_passed["status"]= "error"
            output_passed["message"]= "make sure that sum of all percentage weights is equal to 1"
            output_passed["data"]= ""
            output_passed["code"]= 401
            
        
    except: #Weightage_Percentage Input: Error Handling
        output_passed["status"]= "error"
        output_passed["message"]= "please enter the format mentioned- 0.45 for 45% or 0.10 for 10%...& so on"
        output_passed["data"]= ""
        output_passed["code"]= 401
        

except: #File Input: Error Handling
    output_passed["status"]= "error"
    output_passed["message"]= "please provide the csv file path or check the file name entered"
    output_passed["data"]= ""
    output_passed["code"]= 401


# Very Important Line
output_json = json.dumps(output_passed, ensure_ascii = 'False')
print(output_json)




 #-----------------------------
 #|| written by AAYUSH GADIA ||
 #-----------------------------
       
   

