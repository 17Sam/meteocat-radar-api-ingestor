from PIL import Image
import requests
import io
import os

projectPath = os.path.dirname(os.path.abspath(__file__))

xcoords = [128, 129, 130]
ycoords = [159, 160, 161]

iterations = 30 # aka 3 hours

# Generate the image
backgroundimg = Image.new("RGBA", (768, 768), color="#00000000")

for column in range(len(xcoords)):
    for row in range(len(ycoords)):
        img = requests.get(f"https://static-m.meteo.cat/tiles/fons/GoogleMapsCompatible/08/000/000/{xcoords[column]}/000/000/{ycoords[row]}.png").content

        backgroundimg.paste(Image.open(io.BytesIO(img)), (256*column, 512 - (256*row)))

# Save the generated image
backgroundimg.save(f"{projectPath}/radarImages/background.png")