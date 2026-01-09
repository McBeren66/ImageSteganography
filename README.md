# Image Steganography GUI  

This repository contains a Python program with a graphical user interface built with tkinter. The application allows you to hide a secret message inside an image using the least significant bit (LSB) steganography method and to extract a hidden message from an image.  

## Features  

* **Hide message**: Load an image, enter a secret message and save a new image where the message is encoded in the pixel data.  
* **Extract message**: Load an image that contains a hidden message and decode the secret text.  
* Uses the Pillow library for image processing and tkinter for the GUI.  
* Implements the LSB method to embed bits of the message into the least significant bits of the image's pixels.  
* Automatically handles message length and detects if the message is too long for the chosen image.  

## Prerequisites  

* Python 3.x  
* Pillow (`pip install pillow`)  

## Usage  

Run the script:  

```
python steganography_gui.py
```  

The application opens with two tabs:  

1. **Hide**: Click **Load Image** to choose a cover image, enter your secret message in the text field and click **Save** to generate a new image file with the hidden message.  

2. **Extract**: Click **Load Image** to select an image containing a hidden message and click **Decrypt** to display the extracted text.  

The output image is saved to a file you choose during the saving process. 
