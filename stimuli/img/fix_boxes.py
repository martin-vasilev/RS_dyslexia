# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 18:13:48 2024

@author: Martin
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

os.chdir('C:\\Users\Martin\Documents\R\RS_dyslexia\stimuli\img')

### Font settings:
# TNR:
#y_offset= 68
#line_span= 18 +4
#dist_lines= 1

# TNR item 5:
y_offset= 70
line_span= 18 +6
dist_lines= 1

# OD: 
#y_offset= 76
#line_span= 18 +4 +8
#dist_lines= 1

filename= 'boxes\TNR20text5Key'
img = 'TNR20text5Key'
imge = Image.open(img +'.bmp')

df=  pd.read_csv(filename +'.csv')

xdiff = np.diff(df.Left) # differences between successive x1 numbers
# Return-sweeps are going to show (large) negative differences
neg_index= np.where(xdiff < 0)# find position of line breaks
breaks= np.append(neg_index[0], len(df))

y1_n= df.Top
y2_n= df.Bottom

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
    df.Top[start:end]= [y_start]* len(df.Top[start:end])
    df.Bottom[start:end]= [y_end]* len(df.Bottom[start:end])


# make the x1 and x2 coords non-overlapping:    
for i in range(len(df)):
    
    if i< len(df):
        df.Right[i]= df.Right[i]-1
    
    
    
    

df.to_csv(filename + '_fixed.csv', sep=',')

my_dpi= 120



fig= plt.figure(figsize=(1024/my_dpi, 768/my_dpi), dpi=my_dpi)
fig.figimage(imge)

for i in range(len(df)):
    fig.patches.extend([plt.Rectangle((df.Left[i], 768-17-df.Top[i]),
                              df.Right[i]-df.Left[i], df.Bottom[i]-df.Top[i],
                              fill= False, color='r', linewidth=0.15)])
                     
fig.savefig('my_fig2.png', dpi=my_dpi)    

