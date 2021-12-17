# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 00:24:06 2021

@author: Martin
"""
import os
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.chdir(r'C:\Users\Martin\OneDrive - Bournemouth University\Research\Raw_data\Dyslexia- Leon\coords')


img = 'D:\TNR20text1Key.bmp'
imge = Image.open(img)
data=pytesseract.image_to_boxes(imge)

print(data)

text = pytesseract.image_to_string(imge, config='--psm 11')

with open('coords1.txt', 'w') as f:
    f.write(data)
    
with open('text1.txt', 'w') as f:
    f.write(text)

fig, ax = plt.subplots()

# Display the image
ax.imshow(imge)

# Create a Rectangle patch
rect = patches.Rectangle((113, 768-688), 5, 13, linewidth=1, edgecolor='r', facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()

#plt.imsave(fname='my_image.png', arr=imge, cmap='gray_r', format='png')