# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:11:06 2021

@author: Martin Vasilev
"""

# Function that extracts letter coordinates from stimulus image:

def text_coords(filename= 'D:\R\RS_dyslexia\stimuli\img\TNR20text1Key.bmp', yRes= 768):
    
    import pytesseract
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    import pandas as pd
    import numpy as np
    
    imge = Image.open(filename)
    data=pytesseract.image_to_boxes(imge)
    #text = pytesseract.image_to_string(imge, config='--psm 11')
    
    lines= data.split('\n')
    lines= list(filter(None, lines))
    
    # here y coords are recorded relative to bottom of image, so we need to reverse them

    # recode values from tesseract string into num coords:
    letter= []
    x1= []
    y1= []
    x2= []
    y2= []
    
    for i in lines:
        break_line= i.split(' ')
        letter.append(break_line[0]) # add letters
        x1.append(int(break_line[1])) # x1 left end of box
        x2.append(int(break_line[3])) # x2 right end of box
        
        y1.append(yRes- int(break_line[4]))
        y2.append(yRes- int(break_line[2]))
        
    # now we need to go over the coords and add the empty spaces:
    letter_n= []
    x1_n= []
    x2_n= []
    y1_n= []
    y2_n= []
    
    for i in range(len(letter)):
    
        if i>0:
            if x1[i]- x2[i-1] >= 3:
                # add the empty space before character:
                letter_n.append(' ')
                x1_n.append(x2[i-1]+1) # start of empty space
                x2_n.append(x1[i]-1) # end of empty space
                y1_n.append(y1[i])
                y2_n.append(y2[i])
                
                ## now we need to append actual character at current iteration:
                letter_n.append(letter[i])
                x1_n.append(x1[i])
                x2_n.append(x2[i])
                y1_n.append(y1[i])
                y2_n.append(y2[i])
            else:
                ## not word boundary, append letters as per usual:
                letter_n.append(letter[i])
                x1_n.append(x1[i])
                x2_n.append(x2[i])
                y1_n.append(y1[i])
                y2_n.append(y2[i])
                            
        else:
            letter_n.append(letter[i])
            x1_n.append(x1[i])
            x2_n.append(x2[i])
            y1_n.append(y1[i])
            y2_n.append(y2[i])
        

    
    xdiff = np.diff(x1_n) # differences between successive x1 numbers
    # Return-sweeps are going to show (large) negative differences
    neg_index= np.where(xdiff < 0)# find position of line breaks
    
    rs= [0]*len(x1_n)
    
    for i in range(len(neg_index[0])):
        rs[neg_index[0][i]+1]= 1
        
    df = pd.DataFrame(list(zip(letter_n, x1_n, x2_n, y1_n, y2_n, rs)),
                   columns =['letter', 'x1', 'x2', 'y1', 'y2', 'RS'] )
    
    
    
    ### start at beginning and use a fixed offset and between line-height
    #how to fix extreme values affecting min/ max:
    #1) keep track of prev lines- make sure the current line is bigger than the end of the previous one. 
    #2) If not, take the average of line spacing in the previous
    # last_y1= 0
    # last_y2= 0
    
    # for i in range(len(neg_index[0])):
    #     if i==0:
    #         start= 0
    #         end= neg_index[0][i]+1 # +1 bc we count from 0
    #     else:
    #         start= neg_index[0][i-1]+1
    #         end= neg_index[0][i]+1
        
    #     if i==0:
    #         y1_bound= min(df.y1[start:end])
    #         y2_bound= max(df.y2[start:end])
    #         last_y1= y1_bound
    #         last_y2= y2_bound
            
    #     else:
    #         y1_nums= pd.Series.to_numpy(df.y1[start:end])
    #         y2_nums= pd.Series.to_numpy(df.y2[start:end])
            
    #         ## check for outliers crossing boundaries:
    #         out1= np.where(y1_nums< last_y2)
    #         if len(out1[0])>0:
    #             y1_nums = np.delete(y1_nums, out1)
    #         #out2= np.where(y1_nums< last_y2)
            
    #         y1_bound= min(y1_nums)
    #         y2_bound= max(y2_nums)
    #         last_y1= y1_bound
    #         last_y2= y2_bound
            
    #     # replace existing y positions with the box bounds:
    #     y1_n[start:end]= [y1_bound]* len(df.y1[start:end])
    #     y2_n[start:end]= [y2_bound]* len(df.y2[start:end])
            
    
    # df2 = pd.DataFrame(list(zip(letter_n, x1_n, x2_n, y1_n, y2_n, rs)),
    #                columns =['letter', 'x1', 'x2', 'y1', 'y2', 'RS'] )
    
    return df




import re

file_dir= 'D:/Data/Dyslexia/'
img_dir= 'D:/R/RS_dyslexia/stimuli/img/'
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
        
        ## extract text coordinates from image:
        df= text_coords(img_dir + img_file)
        

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
        new_file.append(msg_flag + ' DISPLAY TEXT 1')
    
        for i in range(len(df)):
            new_file.append(msg_flag + 'REGION CHAR %d 1 %s %d %d %d %d' % (i, df.letter[i], df.x1[i], df.y1[i], df.x2[i], df.y2[i]))
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

with open(file_dir + 'new/'+ file_name + "_new.asc", 'w') as f:
    f.write('\n'.join(new_file))

