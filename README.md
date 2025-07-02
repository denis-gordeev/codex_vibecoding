# codex_vibecoding

This project overlays the transport network from one city onto another directly in the browser. It mimics the idea behind *The True Size Of* but for road systems.

## Running

Open `index.html` in a modern browser. You may need to serve the files via a small HTTP server so that network requests are allowed:

```bash
python -m http.server
```

Then navigate to `http://localhost:8000` and enter two city names. The base city's roads are drawn in black, and the overlay city is translated in red.

The page uses the Overpass API and Nominatim to fetch data from OpenStreetMap, so an internet connection is required.

## Legacy Python script

The repository still includes `overlay_transport.py`, which performs a similar overlay using Python and OSMnx. Install the dependencies from `requirements.txt` and run the script with two city names:

```bash
python overlay_transport.py -a "Tokyo, Japan" -b "Moscow, Russia" -o overlay.png
```
