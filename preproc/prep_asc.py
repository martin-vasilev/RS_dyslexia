# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:11:06 2021

@author: Martin Vasilev
"""

import pandas as pd
import re
from os import listdir
from os.path import isfile, join

file_dir= 'C:/Data/Dyslexia/'

asc = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]

for k in range(len(asc)):

    # open the .asc file
    with open(file_dir + asc[k]) as file:
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
            
            ## extract text coordinates from image:
           # df= text_coords(img_dir + img_file)
            
    
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
            
            ### Print text coordinates:
            if D==0:    # only if not a question
                # load up data frame with coords:
                df=  pd.read_csv('C://Users/Martin/Documents/R/RS_dyslexia/stimuli/boxes/'+ img_file.split('.')[0] +'_fixed.csv')    
    
                new_file.append(msg_flag + ' DISPLAY TEXT 1')
                
                for i in range(len(df)):
                    new_file.append(msg_flag + ' REGION CHAR %d 1 %s %d %d %d %d' % (i, df.Character[i], df.Left[i], df.Top[i], df.Right[i], df.Bottom[i]))
                    new_file.append(msg_flag + ' DELAY 1 MS')
    
            
            
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
    
    with open(file_dir + 'new/'+ asc[k].split('.')[0] + "_new.asc", 'w') as f:
        f.write('\n'.join(new_file))
    
