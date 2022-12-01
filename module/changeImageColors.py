from PIL import Image
import os

def change_image_pixel_values(imaged_path,by_value):
    # Import an image from directory:
    input_image = Image.open(imaged_path)
    
    # Extracting pixel map:
    pixel_map = input_image.load()
    
    # Extracting the width and height 
    # of the image:
    width, height = input_image.size
    
    # taking half of the width:
    for i in range(width):
        for j in range(height):

            # getting the RGB pixel value.
            red, green, blue, alpha_level = input_image.getpixel((i, j))
            
            red -= by_value
            green -= by_value
            blue -= by_value
            # setting the pixel value.
            pixel_map[i, j] = (red,green,blue,alpha_level)
    
    # Saving the final output
    # as "grayscale.png":
    input_image.save(imaged_path.split(".")[0]+"2"+".png", format="png")
# open the image - input_image = Image.open("gfg.png")
change_image_pixel_values("base game/base game images/game buttons/more games button.png",50)