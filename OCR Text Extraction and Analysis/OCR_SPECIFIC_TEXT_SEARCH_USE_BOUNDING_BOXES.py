#!/usr/bin/env python
# coding: utf-8

# # Accurate Text Recognition in Images with Bounding Boxes: A Technique for Precise Text Extraction

# In[112]:


#Import libraries 


# In[113]:


get_ipython().system('pip install pytesseract')


# In[157]:


import pandas as pd
import pytesseract
import cv2
import numpy as np


# In[158]:


# Path to the image file
image_path = r"C:\Users\User\Downloads\payslip.jpg"

# Load the image
img = cv2.imread(image_path)


# In[159]:


# Check if the image is successfully loaded
if img is None:
    print("Error: Image not loaded.")
    exit()


# In[160]:


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# In[161]:


# Thresholding
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# Ensure thresh is a NumPy array
if not isinstance(thresh, np.ndarray):
    print("Error: Thresholded image is invalid.")
    exit()


# In[162]:


# Use Tesseract for text extraction (assuming Tesseract is installed and configured)
data = pytesseract.image_to_data(thresh, config='--psm 6')
print(data)


# In[120]:


get_ipython().system('pip install opencv-python pytesseract')


# In[163]:


# Text detection with Tesseract (ensure Tesseract OCR is installed)
data = pytesseract.image_to_data(thresh, config='--psm 6', output_type=pytesseract.Output.DICT)


# Specify the text you are looking for in the picture 

# In[164]:


# Extract text and bounding boxes for specific text
text_boxes = []
for i in range(len(data['text'])):
    text = data['text'][i].strip()
    if "NAME" in text:  # Check if the text contains "Customer" or any other text you are looking for
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        box = (text, (x, y, x + w, y + h))  # Create a tuple (text, bounding box)
        text_boxes.append(box)

        # Draw bounding box on the image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


# In[165]:


# Save the output image with bounding boxes
output_image_path = r"C:\Users\User\Downloads\scan_2_with_boxes.png"
cv2.imwrite(output_image_path, img)


# In[166]:


# Optionally, display the image with bounding boxes
cv2.imshow("Image with Bounding Boxes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[167]:


# Resize the image to fit the screen while maintaining the aspect ratio
screen_width = 1000  # Set this to your desired width
aspect_ratio = img.shape[1] / img.shape[0]
new_width = screen_width
new_height = int(new_width / aspect_ratio)

resized_img = cv2.resize(img, (new_width, new_height))

# Save the output image with bounding boxes
output_image_path = r"C:\Users\User\Downloads\scan_2_with_boxes.png"
cv2.imwrite(output_image_path, img)

# Display the resized image with bounding boxes
cv2.imshow("Image with Bounding Boxes", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Get the coordiantes of the bounding box of the text you were searching for 

# In[126]:


# Display extracted text and bounding boxes
for text, box in text_boxes:
    print(f"Text: {text}, Bounding Box: {box}")
    x, y, x2, y2 = box
    cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)  # Draw rectangle on the original image


# Show me the bouding box and the text (just that!)

# In[127]:


if 0 <= y < img.shape[0] and 0 <= x < img.shape[1] and 0 <= y2 < img.shape[0] and 0 <= x2 < img.shape[1]:
  # Bounding box is within image boundaries
  cropped_img = img[y:y2, x:x2]
  # Display the cropped image with bounding box
  cv2.imshow('Cropped Image with Bounding Box', cropped_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
else:
  print("Error: Bounding box coordinates are outside the image.")


# # Another way to have look for a text in image. 

# EXTRACT TEXT USING OCR

# In[168]:


boxes = pytesseract.image_to_data(thresh, config='--psm 6')


# CREATE BOUNDING BOX AROUND ALL THE TEXT IN THE PICTURE 

# In[171]:


for i, box in enumerate(boxes.splitlines()[1:]):
    values = box.split('\t')
    if len(values) == 5:
        x, y, w, h, text = map(int, values)
        if text.lower() == "NORMAL":
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print(f"coordinates of your text (x,y) = ({x}, {y})")
    else:
        print(f"Skipping line: {box}")


# SEARCH FOR SPECIFIC TEXT AND COORDINATES AND DRAW A BOUNDING BOX AROUND IT 

# In[172]:


# Extract text and bounding boxes for specific text
text_boxes = []
for i in range(len(data['text'])):
    text = data['text'][i].strip()
    if "OUT" in text:  # Check if the text contains "Customer" or any other text you are looking for
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        box = (text, (x, y, x + w, y + h))  # Create a tuple (text, bounding box)
        text_boxes.append(box)

        # Draw bounding box on the image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


# In[173]:


# Resize the image to fit the screen while maintaining the aspect ratio
screen_width = 1000  # Set this to your desired width
aspect_ratio = img.shape[1] / img.shape[0]
new_width = screen_width
new_height = int(new_width / aspect_ratio)

resized_img = cv2.resize(img, (new_width, new_height))

# Save the output image with bounding boxes
output_image_path = r"C:\Users\User\Downloads\scan_2_with_boxes.png"
cv2.imwrite(output_image_path, img)

# Display the resized image with bounding boxes
cv2.imshow("Image with Bounding Boxes", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




