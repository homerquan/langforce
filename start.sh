#!/bin/bash

# Set the Webots home directory
export WEBOTS_HOME="/Applications/Webots.app/Contents/MacOS"

# Launch Webots with the specified world file in stream mode in the background.
"$WEBOTS_HOME/webots" --stream --minimize ./worlds/pick_and_place.wbt &

# Start the HTTP server serving files from the ./www directory.
http-server ./www