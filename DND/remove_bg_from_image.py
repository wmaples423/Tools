import os
from rembg import remove
from PIL import Image
import easygui

# display a file selection dialog to choose the directory containing the JPEG files
directory = easygui.diropenbox(title="Select directory containing JPEG files")

# loop through all files in the directory
for filename in os.listdir(directory):
    # check if the file is a JPEG file
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # create input and output paths
        input_path = os.path.join(directory, filename)
        output_path = os.path.join(directory, os.path.splitext(filename)[0] + ".png")
        
        # open the input image
        input_image = Image.open(input_path)
        
        # remove the background from the input image
        output_image = remove(input_image)
        
        # save the output image as a PNG file with the original name
        output_image.save(output_path)