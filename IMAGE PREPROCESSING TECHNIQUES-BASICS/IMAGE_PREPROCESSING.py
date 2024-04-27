#!/usr/bin/env python
# coding: utf-8

# # IMAGE PREPROCESSING 

# import libraries 

# In[5]:


get_ipython().system('pip install pytesseract')


# In[6]:


import cv2
import pytesseract


# In[9]:


# Path to the image file
image_path = r"C:\Users\User\Downloads\test_2.png"

# Load the image
img = cv2.imread(image_path)

# Check if the image is loaded successfully
if img is None:
    print("Error: Failed to load image from path:", image_path)
    exit()


# In[10]:


# Convert the image to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Image preprocessing techniques
# 
#     - Noise Reduction: Use Gaussian Blur to reduce noise.
#     - Thresholding: Convert the image to binary (black and white) to make text regions stand out.
#     - Gaussian Blur helps to smooth out noise and imperfections in the image.
#     - Thresholding then converts the smoothed image into a binary format, making text regions stand out against the    background.

# In[12]:


# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)

# Apply adaptive thresholding to obtain a binary image
thresh_img = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)


# In[13]:


# Set the path to the Tesseract executable (change as per your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# In[14]:


# Perform text extraction using Tesseract
extracted_text = pytesseract.image_to_string(thresh_img)

# Display the extracted text
print("Extracted Text:")
print(extracted_text)


# In[ ]:




