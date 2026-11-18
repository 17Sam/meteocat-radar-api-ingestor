import requests
from PIL import Image
from io import BytesIO
import os

def DownloadImages(iterations, startminute, starthour, startday, startmonth = 10, startyear = 2026):
    success = True # Whether the images are successfully downloaded. If it fails
                   # (usually due to no connection), returns False

    projectPath = os.path.dirname(os.path.abspath(__file__))

    xcoords = [128, 129, 130]
    ycoords = [159, 160, 161]

    # The total number of iterations the code is going to run
    # Each iteration is an image request
    totaliterations = len(xcoords) * len(ycoords) * iterations

    imgsdownloaded = 0

    override = False # set this to True if you want existing saved images to be overwritten

    for xcoord in xcoords: # iterate through all the x coordinates within xcoords
        if (not success): break
        for ycoord in ycoords: # iterate through all the y coordinates within ycoords
            print(f"\n*** DOWNLOADING IMAGES FROM COORDINATES [{xcoord}, {ycoord}] ***]")

            # Iterate through the image links
            minute = startminute
            hour = starthour
            day = startday
            month = startmonth
            year = startyear


            for n in range(iterations):
                strhour = "0" * (2 - len(str(hour))) + str(hour)
                strminute = "0" * (2 - len(str(minute))) + str(minute)

                strmonth = "0" * (2 - len(str(month))) + str(month)
                strday = "0" * (2 - len(str(day))) + str(day)

                strdate = f"{year}-{strmonth}-{strday}"

                # Check if target folder exists. If not, create it
                if (not os.path.isdir(f"{projectPath}/radarImages/{strdate}")): # If date file does not exist, create it
                    print("Creating folder at " + os.path.abspath(f"{projectPath}/radarImages/{strdate}") + ", as it did not exist")
                    os.mkdir(f"{projectPath}/radarImages/{strdate}") # Make the dir
                if (not os.path.isdir(f"{projectPath}/radarImages/{strdate}/[{xcoord}-{ycoord}]")): # If date file does not exist, create it
                    print("Creating folder at " + os.path.abspath(f"{projectPath}/radarImages/{strdate}/[{xcoord}-{ycoord}]") + ", as it did not exist")
                    os.mkdir(f"{projectPath}/radarImages/{strdate}/[{xcoord}-{ycoord}]") # Make the dir

                # Check if image already exists
                if (not override):
                    try: # If the image already exists
                        Image.open(f"{projectPath}/radarImages/{strdate}/[{xcoord}-{ycoord}]/{strhour}:{strminute}.png")

                        imgsdownloaded += 1
                        print("[ \033[33mSKIP \033[0m" + str(int((imgsdownloaded)/totaliterations * 100)) + "% ] " + f"({strdate} {strhour}:{strminute}) " + str(imgsdownloaded) + "/" + str(totaliterations) + " image already exists")

                        # Change time
                        minute -= 6
                        if (minute < 0):
                            minute = 54
                            hour -= 1

                            if (hour == -1):
                                hour = 23
                                day -= 1

                                # Day would have to change here

                        continue
                    except:
                        None # Image does not exist

                imgurl = f"https://static-m.meteo.cat/tiles/combinada/{year}/{strmonth}/{strday}/{strhour}/{strminute}/6/08/000/000/{xcoord}/000/000/{ycoord}.png"

                try:
                    imgdata = requests.get(imgurl).content
                except:
                    success = False # Request failed. Abort and return False
                    break

                imgsdownloaded += 1

                # Check if the downloaded image is a valid image
                try:
                    img = Image.open(BytesIO(imgdata))
                except:
                    # Image is NOT a valid image
                    print("[ \033[31mERROR \033[0m" + str(int((imgsdownloaded)/totaliterations * 100)) + "% ] " + f"({strdate} {strhour}:{strminute}) " + str(imgsdownloaded) + "/" + str(totaliterations) + " downloaded image is not a valid image. Image from: " + imgurl)

                    # Change time
                    minute -= 6
                    if (minute < 0):
                        minute = 54
                        hour -= 1

                        if (hour == -1):
                            hour = 23
                            day -= 1

                            # Day would have to change here

                    continue

                with open(f"{projectPath}/radarImages/{strdate}/[{xcoord}-{ycoord}]/{strhour}:{strminute}.png", "wb") as image:
                    image.write(imgdata)
                
                print("[ \033[32mOK \033[0m" + str(int((imgsdownloaded)/totaliterations * 100)) + "% ] " + f"({strdate} {strhour}:{strminute}) " + str(imgsdownloaded) + "/" + str(totaliterations) + " downloaded from " + imgurl)
                
                minute -= 6
                if (minute < 0):
                    minute = 54
                    hour -= 1

                    if (hour == -1):
                        hour = 23
                        day -= 1

                        # Day would have to change here
    
    return success