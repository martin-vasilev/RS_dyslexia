import os
import csv
from PIL import Image, ImageDraw, ImageFont

# Set the working directory
os.chdir('C:\\Users\\Martin\\Documents\\R\\RS_dyslexia\\stimuli\\img')

def ImageGenerator(sent, ScreenX=1920, ScreenY=1080, posX=200, posY=200, Font_size=26, filename='test.bmp', draw_boxes=False):
    # Load the font
    font = ImageFont.truetype('OpenDyslexic-Regular.otf', Font_size)
    
    # Create a white canvas
    img = Image.new("RGB", [ScreenX, ScreenY], (255, 255, 255))
    d = ImageDraw.Draw(img) # Draw canvas
    
    # Initialize current position
    current_x, current_y = posX, posY
    
    # Store bounding boxes
    bounding_boxes = []
    
    # Fixed line spacing
    line_spacing = Font_size * .8 #0.182  # Adjust this multiplier as needed
    
    # Draw each character separately and calculate its bounding box
    lines = sent.split('\n')
    for line_idx, line in enumerate(lines):
        line_height = 0  # Reset line height for each line
        
        for char_idx, char in enumerate(line):
            # Get bounding box of the character
            bbox = d.textbbox((current_x, current_y), char, font=font)
            bounding_boxes.append((char, bbox))
            
            # Calculate line height based on the tallest character in the line
            char_height = bbox[3] - bbox[1]
            if char_height > line_height:
                line_height = char_height
            
            # Draw the character
            d.text((current_x, current_y), char, font=font, fill=(0, 0, 0))
            
            # Optionally draw the bounding box
            if draw_boxes:
                d.rectangle(bbox, outline="red")
            
            # Update current position
            current_x += bbox[2] - bbox[0]
        
        # Calculate the next line's starting position
        if line_idx < len(lines) - 1:
            next_line_height = max(line_height, Font_size)  # Ensure next line starts below the tallest character
            current_y += int(next_line_height + line_spacing)
        
        current_x = posX  # Reset x to initial posX at the end of each line
    
    # Save the image
    img.save(filename, "BMP")
    
    # Save bounding boxes to CSV file
    csv_filename = os.path.splitext(filename)[0] + '_bounding_boxes.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Character', 'Left', 'Top', 'Right', 'Bottom'])
        for char, bbox in bounding_boxes:
            csv_writer.writerow([char, bbox[0], bbox[1], bbox[2], bbox[3]])


    
    # Return the bounding boxes
    return bounding_boxes

# Example usage
img_name = "P1"

with open(img_name + ".txt", "rt") as f:
    text = f.read().replace('\\n', '\n')

bounding_boxes = ImageGenerator(text, ScreenX=1024, ScreenY=768, posX=112, posY=63,
                                Font_size=17.5, filename='comp/' + img_name + ".bmp", draw_boxes=True)
                                      #19.48 TNR first 4
# Print the bounding boxes
for char, box in bounding_boxes:
    print(f"Character: '{char}', Bounding Box: {box}")
