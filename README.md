# svg-to-wav

Converts an svg file to a wav file, interpolating paths to draw closed shapes with sound. Every point on the path is represented with x-y coordinates, and the left-right audio channels are respectively the x and y signals.

## SVG requirements

The script has been tested with inkScape. The only element that the script read is 'path', meaning that any other element will be ignored. Moreover, the path needs to be made of lines only (no bezier or arcs). The path should be closed, but if it isn't the software will close it on its own.

## Usage

Run `python/main.py --help` to get information about usage. Sorry, today I'm lazy.