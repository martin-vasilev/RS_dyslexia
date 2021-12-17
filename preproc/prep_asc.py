# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:11:06 2021

@author: Martin Vasilev
"""

import re

file_dir= 'D:/Data/Dyslexia/'
file_name= '3.asc'

# open the .asc file
with open(file_dir + file_name) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    
    
# now we go line by line to modify/ add stuff as needed:
new_file= []
img_file= ''
D= 0
cond= 0
item= 0
ET_flag= ''
wait_flag=0 


for i in range(len(lines)):
    
    curr_line= lines[i]
    
    # fix display coords issue:
    if 'DISPLAY_COORDS' in curr_line:
        curr_line= curr_line.replace('DISPLAY_COORDS', 'DISPLAY COORDS')
    
    if 'IMGLOAD CENTER' in curr_line: # image loaded for current trial
        img_file= curr_line.split(' ')[4]
        wait_flag= 1
        
        if 'text' in img_file: # check if it is item
            D= 0
            
        if 'question' in img_file: # check if it is item
            D= 1       
            
        if 'TNR' in img_file: # times new roman font
            cond= 1
            
        if 'OD' in img_file: # open dyslexia font
            cond= 2
            
        if D== 0: # if not question...
            
            # get numbers, second number is always item number:
            item= int(re.findall(r'\d+', img_file)[1])
        
        # if item is a question, take last item number (since item is not updated above)

    
    ET_flag= 'TRIALID ' + 'E' + str(cond)+'I' +str(item)+ 'D' +str(D)
    
    if wait_flag==1 and 'TRIALID' in curr_line:
        
        # replace flag with umass convention, so we can open it in EyeDoctor
        msg_flag= curr_line.split(' ')[0]
        curr_line= msg_flag+ ' ' + ET_flag
        wait_flag= 0 # reset so that it doesn't get triggered in repetition
    
    
    ## we want to filter out questions somehow?
    
    ## add trial end flags
    ## add display on/off flags?
    
    # append current line to new file once all changes have been done:
    new_file.append(curr_line)