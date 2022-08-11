# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 00:24:06 2021

@author: Martin R. Vasilev
"""
import os
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches



os.chdir(r'D:\R\RS_dyslexia\stimuli')

### Font settings:
# TNR:
y_offset= 66
line_span= 18
dist_lines= 5 



img = 'D:\R\RS_dyslexia\stimuli\img\TNR20text1Key.bmp'
imge = Image.open(img)
data=pytesseract.image_to_boxes(imge)

print(data)

text = pytesseract.image_to_string(imge, config='--psm 11')

# with open('coords1.txt', 'w') as f:
#     f.write(data)
    
# with open('text1.txt', 'w') as f:
#     f.write(text)

# fig, ax = plt.subplots()

# # Display the image
# ax.imshow(imge)

# # Create a Rectangle patch
# rect = patches.Rectangle((113, 768-688), 5, 13, linewidth=1, edgecolor='r', facecolor='none')

# # Add the patch to the Axes
# ax.add_patch(rect)

# plt.show()

#plt.imsave(fname='my_image.png', arr=imge, cmap='gray_r', format='png')


lines= data.split('\n')
lines= list(filter(None, lines))

yRes= 768 # y dimension of screen
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
        
df = pd.DataFrame(list(zip(letter_n, x1_n, x2_n, y1_n, y2_n)),
               columns =['letter', 'x1', 'x2', 'y1', 'y2'] )

xdiff = np.diff(x1_n) # differences between successive x1 numbers
# Return-sweeps are going to show (large) negative differences
neg_index= np.where(xdiff < 0)# find position of line breaks
breaks= np.append(neg_index[0], len(df))

### start at beginning and use a fixed offset and between line-height
#how to fix extreme values affecting min/ max:
#1) keep track of prev lines- make sure the current line is bigger than the end of the previous one. 
#2) If not, take the average of line spacing in the previous

for i in range(len(breaks)):
    if i==0:
        start= 0
        end= breaks[i]+1 # +1 bc we count from 0
        y_start= y_offset # y offset of 1st line
        y_end= y_start+ line_span 
    else:
        start= breaks[i-1]+1
        end= breaks[i]+1
        y_start= y_end +dist_lines # y offset of 1st line
        y_end= y_start+ line_span 
        
    # replace existing y positions with the box bounds:
    y1_n[start:end]= [y_start]* len(df.y1[start:end])
    y2_n[start:end]= [y_end]* len(df.y2[start:end])
        

#x_diff= [x2_n - x1_n]
df2 = pd.DataFrame(list(zip(letter_n, x1_n, x2_n, y1_n, y2_n)),
               columns =['letter', 'x1', 'x2', 'y1', 'y2'] )


df2.to_excel('TNR20text1Key.xlsx')
