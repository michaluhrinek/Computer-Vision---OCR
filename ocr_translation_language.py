#!/usr/bin/env python
# coding: utf-8

# # OCR - Text Extraction & Langueage Translation 

# import libraries 

# In[1]:


from PIL import Image
import pytesseract
import cv2


# In[2]:


from PIL import Image
import pytesseract


# In[3]:


get_ipython().system('pip install pytesseract googletrans==4.0.0-rc1 Pillow')


# In[4]:


get_ipython().system('pip install opencv-python')


# In[5]:


#Define filepath and load image and extract text from it


# In[6]:


image_path = r"C:\Users\User\Downloads\czk_2.jpg"


# In[7]:


img=cv2.imread(r"C:\Users\User\Downloads\czk_2.jpg")


# In[8]:


# Read the image and perform OCR
text = pytesseract.image_to_string(Image.open(image_path), lang='eng')


# In[9]:


#Using different PSM modes for the text extraction 
text = pytesseract.image_to_string(Image.open(image_path), lang='eng', config='--psm 6')
print(text)


# In[16]:


print(pytesseract.image_to_string(Image.open(image_path), lang='eng'))


# CLEANING TEXT / NORMALIZATION + TEXT TRANSLATION

# In[17]:


import re
from googletrans import Translator # library for translation 

def clean_text(text):   #function for cleaning text from weird characters
  # Remove punctuation and special characters
  cleaned_text = re.sub(r'[^\w\s]', '', text)
  # You can add more specific patterns here to remove additional unwanted characters
  return cleaned_text

#in this function we define from which language we will translate our text into what language
def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, src='cs', dest='en')
    return translated_text.text


# APPLY CLEANING TEXT AND TRANSLATION FUNCTIONS ON OUR TEXT FROM PICTURE

# In[18]:


# Perform OCR to extract Czech text
text = pytesseract.image_to_string(img, lang='ces')
# Clean the extracted text
cleaned_text = clean_text(text)
# Translate the cleaned text to English
english_text = translate_text(cleaned_text)

print(english_text)


# ANOTHER WAY OF CLEANING DATA AND TRANSLATION 

# unicodedata.normalize('NFD', text) to normalize characters using Unicode Normalization Form Decomposition (NFD).
# Unicode normalization ensures that different representations of the same character are converted to a single, standardized form. For example, accented characters may be represented as a combination of a base character and a diacritic mark. Normalization converts such representations to a standardized form.
# This method is effective for dealing with accented characters, diacritics, and other complex Unicode characters. It ensures that text is consistent and compatible across different systems.

# In[19]:


import unicodedata

def clean_text(text):
  # Normalize characters using NFD (Normalization Form Decomposition)
  normalized_text = unicodedata.normalize('NFD', text)
  return normalized_text

text = pytesseract.image_to_string(img, lang='ces')
cleaned_text = clean_text(text)
english_text = translate_text(cleaned_text)


# In[20]:


print(english_text)


# Show me the original image 

# In[21]:


import cv2

# Check if the image is loaded successfully
if img is not None:
    # Create a named window
    cv2.namedWindow('Input Image')

    # Display the image
    cv2.imshow("Input Image", img)

    # Wait for a key press and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Failed to load image")


# In[ ]:




