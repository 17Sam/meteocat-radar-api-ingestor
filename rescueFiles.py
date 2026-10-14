import os
from PIL import Image

path = "/Users/cody/Documents/Didac/Python/visualitzacio-dades-meteocat/MeteoCat-XRAD+XDDE-Ingestor/.git/lost-found/other"

nonimages = []

for filename in os.listdir(path):
    try:
        Image.open(f"{path}/{filename}")
    except:
        nonimages.append(filename)

print("Files which aren't a valid image:", nonimages)