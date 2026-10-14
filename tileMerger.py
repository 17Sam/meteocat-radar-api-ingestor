from PIL import Image
from datetime import datetime, timezone
import os

xcoords = [128, 129, 130]
ycoords = [159, 160, 161]

def GenerateFullRadarImages(iterations):
    projectPath = os.path.dirname(os.path.abspath(__file__))

    timestampnow = datetime.now(tz=timezone.utc).timestamp()

    targetdate = datetime.fromtimestamp(timestampnow - 900, timezone.utc)

    hour = targetdate.hour
    minute = (targetdate.minute // 6) * 6

    year = targetdate.year
    month = targetdate.month
    day = targetdate.day

    # Check if necessary folders exist. If not, create them.
    if (not os.path.isdir(f"{projectPath}/radarImages/full-radar-images")): # If date file does not exist, create it
        print("Creating folder at " + os.path.abspath(f"{projectPath}/radarImages/full-radar-images") + ", as it did not exist")
        os.mkdir(f"{projectPath}/radarImages/full-radar-images") # Make the dir
    if (not os.path.isdir(f"{projectPath}/radarImages/complete-radar-images")): # If date file does not exist, create it
        print("Creating folder at " + os.path.abspath(f"{projectPath}/radarImages/complete-radar-images") + ", as it did not exist")
        os.mkdir(f"{projectPath}/radarImages/complete-radar-images") # Make the dir

    for n in range(iterations):
        imagesexist = True

        strhour = "0" * (2 - len(str(hour))) + str(hour)
        strminute = "0" * (2 - len(str(minute))) + str(minute)

        strmonth = "0" * (2 - len(str(month))) + str(month)
        strday = "0" * (2 - len(str(day))) + str(day)

        date = f"{year}-{strmonth}-{strday}"

        # Check if folder exists. If not, create it
        if (not os.path.isdir(f"{projectPath}/radarImages/full-radar-images/{date}")): # If date file does not exist, create it
            print("Creating folder at " + os.path.abspath(f"{projectPath}/radarImages/full-radar-images/{date}") + ", as it did not exist")
            os.mkdir(f"{projectPath}/radarImages/full-radar-images/{date}") # Make the dir
        if (not os.path.isdir(f"{projectPath}/radarImages/complete-radar-images/{date}")): # If date file does not exist, create it
            print("Creating folder at " + os.path.abspath(f"{projectPath}/radarImages/complete-radar-images/{date}") + ", as it did not exist")
            os.mkdir(f"{projectPath}/radarImages/complete-radar-images/{date}") # Make the dir

        # Check if image already exists
        try:
            Image.open(f"{projectPath}/radarImages/full-radar-images/{date}/{strhour}:{strminute}.png")
            # Image exists
            print("[ \033[33mSKIP \033[0m" + str(int((n+1)/iterations * 100)) + "% ] " + f"({date} {strhour}:{strminute}) " + str(n+1) + "/" + str(iterations) + " image already exists")

            minute -= 6
            if (minute < 0):
                minute = 54
                hour -= 1

                if (hour == -1):
                    hour = 23
                    day -= 1
            
            continue
        except:
            # Image does NOT exist
            None

        # Generate the image
        radarimg = Image.new("RGBA", (768, 768), color="#00000000")

        for column in range(len(xcoords)):
            if (not imagesexist): continue # If the radar subimages do not exist, continue
            for row in range(len(ycoords)):
                if (not imagesexist): continue # If the radar subimages do not exist, continue

                # Check if folder exists. If not, create it

                # see if image exists
                try:
                    img = Image.open(f"{projectPath}/radarImages/{date}/[{xcoords[column]}-{ycoords[row]}]/{strhour}:{strminute}.png")
                    # image exists
                except:
                    # image does NOT exist
                    imagesexist = False
                    continue

                radarimg.paste(img, (256*column, 512 - (256*row)))
        
        if (not imagesexist):
            print("[ \033[31mERROR \033[0m" + str(int((n+1)/iterations * 100)) + "% ] " + f"({date} {strhour}:{strminute}) " + str(n+1) + "/" + str(iterations) + " radar subimages do not exist")

            minute -= 6
            if (minute < 0):
                minute = 54
                hour -= 1

                if (hour == -1):
                    hour = 23
                    day -= 1
            continue

        # Save the generated image
        radarimg.save(f"{projectPath}/radarImages/full-radar-images/{date}/{strhour}:{strminute}.png")

        # Paste the radar image on top of the map of Catalunya to create the completed image
        completeradarimg = Image.open(f"{projectPath}/radarImages/background.png")
        completeradarimg.paste(radarimg, (0, 0), radarimg)
        completeradarimg.save(f"{projectPath}/radarImages/complete-radar-images/{date}/{strhour}:{strminute}.png")

        print("[ \033[32mOK \033[0m" + str(int((n+1)/iterations * 100)) + "% ] " + f"({date} {strhour}:{strminute}) " + str(n+1) + "/" + str(iterations) + " images generated")
        
        minute -= 6
        if (minute < 0):
            minute = 54
            hour -= 1

            if (hour == -1):
                hour = 23
                day -= 1

GenerateFullRadarImages(200)