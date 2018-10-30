## README- Finding-Lead-Chiller


### **BRIEF DESCRIPTION:**

  - Basically we had meter data of Several Chillers recorded at different timestamps over a period of time. Our main motive was to find the Lead Chiller among all, during the period of which we had the data.

  - The script was written to find the Lead Chiller. **The script basically takes an Off- Value as an Input (only 1 value)**, where the Off- Value is basically the Meter Reading or the value plotted in Y Axis. 

  - **The script returns the Lead Chiller No. alongwith its** Total Cycles, Total Duration, Maximum Duration, Average Duration & Percentage Contribution in Total Energy Consumption for the given Off- Value alongwith the status which tells whether it is Leading or not.

  - ***It may also happen that more than 1 Chiller are Lead Chiller.***

-------------------------------------------------------------------------------------------------------------------


### **PREREQUISITES:**

  - written for LINUX Server.
  - written in  Python 3.6 .
  - supporting packages required- pandas, numpy, statistics, json, sys.


-------------------------------------------------------------------------------------------------------------------


### **CLIENT-END FULFILMENTS:**

The below format must be followed for the successful running of the script:  

1. **File Path ::**
   - it must be a CSV File Path.
   - it must be passed in the second argument of sys.argv.
   
   ----------------------------------------------------------------------------------------------------------------
   
2. **CSV File Data ::**

    - Example:  
      - We have 4 chiller's meter reading, then in our CSV File, from Column 2 to Column 5 in each column there must be meter reading of each individual chiller & in Column 6 there must be Total Reading in which each row, represents the sum of meter reading of all chiller viz in that particular row & in Column 1 there must be timestamps with Date portion starting with Day.

      - make sure that Timestamp's Column is inserted in the CSV File and that too in the 1st column & make sure that Total Reading is inserted in the CSV File in the last column. 
   
   ----------------------------------------------------------------------------------------------------------------   

3. **Input String ::**

   - it must be passed as JSON String.
   - it must be passed in the third argument of sys.argv. 
   - **the JSON String, alternatively the dictionary data structure should have the following Key Names::**  
     `a. input :: it must contain the Off- Value & all the Percentage Weightage`

   - **Off- Value viz basically the Y- Values or the Meter Reading is taken as Input.**
   - **there is no constraint on the input values.**

   - Percentage Weightage is given to following variables- Total Running Hours, Maximum Running Hours &   Percentage Contribution in Total Energy Consumption & all are actually taken as user input & **in the same order as written above.**  
     `- WITH FIRST ITEM IN LIST WILL BE CONSIDERED FOR TOTAL RUNNING HOURS.`  
     `- SECOND ITEM IN LIST WILL BE CONSIDERED FOR MAXIMUM RUNNING HOURS.`  
     `- THIRD ITEM IN LIST WILL BE CONSIDERED FOR PERCENTAGE CONTRIBUTION IN TOTAL ENERGY CONSUMPTION.`  

   - **for 40% put 0.40, or for 95% put 0.95 and so on.**  
   - **make sure that sum of all is equals to 1.**  	  

   - `Example :: {"input" : [5, [0.40, 0.40, 0.20]] }`		

      **CAUTION: The above Key Names are case-sensitive, so use exactly as written above.**


   ---------------------------------------------------------------------------------------------------------------


4. **Output String ::**
	  - it is passed as a JSON String.  
	  - all the Chiller & each of its insights are passed in the Output.  
	  - **Folowing Insights are given :**  
		- Lead Status  
		- Total No of Cycles  
		- Total Duration of Cycle  
		- Average Duration of Cycle  
		- Maximum Duration of Cycle  
		- Percentage Contribution of Each Chiller in the Total Energy Consumption  

	  - **Units of Inights :**  
		- Lead Status            : simple string with LEAD or NO-LEAD written.  
		- Total No of Cycles     : simply count is given & for some outputs comments are written in Total No. of Cycles asking to refer to Codebook.  
		- Total Duration         : given in mins.  
		- Average Duration       : given in mins.  
		- Maximum Duration       : given in mins.  
		- Percentage Contribution: given in %.  

   ----------------------------------------------------------------------------------------------------------------   

5. **Codebook ::**

    - Comment_3 :: All Data Below Off- Value
    - Comment_4 :: All Data Above Off- Value	  

-------------------------------------------------------------------------------------------------------------------	

### **OUTPUT SAMPLE:**
  -	Please refer the Output Screenshots Folder.
  

-------------------------------------------------------------------------------------------------------------------	

### **AUTHORS:**

  -	coded by AAYUSH GADIA.

   
					  
