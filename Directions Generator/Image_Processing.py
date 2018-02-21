'''
Name: Mitchell Marino
Date: 2018-02-20
Program: Image_Processing.py
Description: Used to fetch my linkedin image from the web for the help screen.
'''

#Imports
from PIL import Image, ImageTk
import urllib.request
import io

def generate_profile_image():
    '''
    Pull my Linkedin photo from the web for use by the application's help page.
    My linkedin as of writing this can be found at: https://www.linkedin.com/in/mitchelltmarino/
    '''
    #Address of my Linkedin photo.
    url = ("https://media.licdn.com/mpr/mpr/shrinknp_400_400/AAEAAQAAAAAAAAaPAAAAJDQ5NmQwZGI3LWEyYjUtNDBjZi05NzVhLTdhZWYwOTU4MzkzZA.jpg")
    #Open the image for use locally.
    with urllib.request.urlopen(url) as URL:
        img = io.BytesIO(URL.read())
        img = Image.open(img)
        #Save as TKinter image for use by the canvas.
        photo = ImageTk.PhotoImage(img)
    return photo