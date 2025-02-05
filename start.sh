#!/bin/bash
# Launch Webots with the specified world file in stream mode in the background.
"/Applications/Webots.app/Contents/MacOS/webots" --stream  --minimize ./worlds/pick_and_place.wbt &

# Start the HTTP server serving files from the ./www directory.
http-server ./www