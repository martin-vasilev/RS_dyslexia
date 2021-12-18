# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:11:06 2021

@author: Martin Vasilev
"""

import re

file_dir= 'D:/Data/Dyslexia/'
file_name= '3'

# open the .asc file
with open(file_dir + file_name + '.asc') as file:
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
trial_seq= 0


for i in range(len(lines)):
    
    curr_line= lines[i]
    
    if '!V TARGET_POS TARG1' in curr_line:
        continue # get rid of annoying EB flags
    
    # fix display coords issue:
    if 'DISPLAY_COORDS' in curr_line:
        curr_line= curr_line.replace('DISPLAY_COORDS', 'DISPLAY COORDS')
    
    if 'IMGLOAD CENTER' in curr_line: # image loaded for current trial
        img_file= curr_line.split(' ')[4]
        wait_flag= 1
        trial_seq= trial_seq+1
        
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
            

    if 'TRIALID' in curr_line and wait_flag==0:
        
        if trial_seq>0:
            msg_flag= curr_line.split(' ')[0]
            
            ## add trial end flags
            new_file.append(msg_flag + ' ENDBUTTON 5')
            new_file.append(msg_flag + ' DISPLAY OFF')
            new_file.append(msg_flag + ' TRIAL_RESULT 5')
            new_file.append(msg_flag + ' TRIAL OK')
        
        continue # don't add the current flag so that we have one flag per trial
    
    
    if wait_flag==1 and 'TRIALID' in curr_line:
        
        # replace flag with umass convention, so we can open it in EyeDoctor
        msg_flag= curr_line.split(' ')[0]
        curr_line= msg_flag+ ' ' + ET_flag
        wait_flag= 0 # reset so that it doesn't get triggered in repetition
        
        # print current line:
        new_file.append(curr_line)
        
        # print start flags:
        msg_flag= curr_line.split(' ')[0]
        new_file.append(msg_flag + ' GAZE TARGET ON')
        new_file.append(msg_flag + ' GAZE TARGET OFF')
        new_file.append(msg_flag + ' DISPLAY ON')
        new_file.append(msg_flag + ' SYNCTIME')
        
        continue
    
    if 'SYNCTIME' in curr_line:
        continue
    #    msg_flag= curr_line.split(' ')[0]
    #    new_file.append(msg_flag + ' GAZE TARGET ON')
    #    new_file.append(msg_flag + ' GAZE TARGET OFF')
    #    new_file.append(msg_flag + ' DISPLAY ON')
    
    # append current line to new file once all changes have been done:
    new_file.append(curr_line)

with open(file_dir + 'new/'+ file_name + "_new.asc", 'w') as f:
    f.write('\n'.join(new_file))

