# MeteoCat Radar API Ingestor
Ingests XRAD+XDDE (radar + lightning) tile images from the [static meteocat API](https://static-m.meteo.cat) and stores the files locally on a folder per day.

Each complete image is constituted by 9 tiles and a background map of Catalunya which can be merged using **tileMerger.py**.

All the files are stored under the radarImages folder.

## Vars JSON
Change this JSON to specify the behavior of automated-downloads.py.

**interval**: The waiting time between each fetch in seconds.

**iterations**: How many instants to fetch. A value of 2 will fetch 18 tile images totalling 2 complete radar images.

## File functions
**automated-downloads.py** — Calls ingestor.py every certain interval.

**ingestor.py** — Contains a function which calls the API and stores the files locally. Stores them to radarImages/{YYYY}-{MM}-{DD}/

**tileMerger.py** — Merges the 9 tiles into one whole image and slaps a background of Catalunya on the back. Images are stored under radarImages/complete-radar-images.

**generate-background.py** — Generates the map of Catalunya which is used as the background under radarImages.