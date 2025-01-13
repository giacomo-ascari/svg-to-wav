# python main.py examples/disegno.svg examples/disegno.wav -v -p
# https://svg-path-visualizer.netlify.app/

if __name__ != '__main__':
    exit(1)

# All the imports
import os
from argparse import ArgumentParser
from PIL import Image
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import audiofile

from utils import *

# Parse command line arguments

parser = ArgumentParser(prog='SvgToWav', description='What the program does', epilog='Text at the bottom of help')
parser.add_argument("inputFile", help="Input .svg file")
parser.add_argument("outputFile", help="Output .wav file")
parser.add_argument("-v", "--verbose", action='store_true', help="Print status messages to stdout")
parser.add_argument("-p", "--plot", action='store_true', help="Plot results with Matplotlib")
parser.add_argument("-f", "--frequency", default=300, nargs='?', type=int, help="Quantity of drawings per second (def. 300)")
parser.add_argument("-s", "--sampling", default=48000, nargs='?', type=int, help="Sampling frequency (def. 48000)")
parser.add_argument("-d", "--duration", default=5, nargs='?', type=int, help="Duration of audio file in seconds (def. 5)")
args = parser.parse_args()

input_path = os.path.normpath(args.inputFile)
output_path = os.path.normpath(args.outputFile)

if args.verbose:
    print("Input file: ", input_path)
    print("Output file: ", output_path)

if not os.path.isfile(input_path):
    print("Input file does not exist")
    exit(1)

if os.path.isfile(output_path):
    print("Output file already exists. It will be overwritten")

# Read the .svg file

tree = ET.parse(args.inputFile)
root = tree.getroot()

# Explore the XML tree with breadth-first search

points_list = []
bfs(root, readnode, {"points": points_list})

if args.verbose:
    print(f"{len(points_list)} points added")

# Convert the points to cartesian

points_list.append(points_list[0])
points_cart = np.ndarray((len(points_list), 2), dtype=np.float32)
for i in range(0, len(points_list)):
    points_cart[i] = points_list[i]

x_raw = points_cart[:,0]
y_raw = points_cart[:,1]

# interpolate the points

points_inter_list = []
total_length = 0

for i in range(0, len(points_cart)-1):
    total_length += np.linalg.norm(points_cart[i+1] - points_cart[i])
period_samples = int(args.sampling / args.frequency)

for i in range(0, len(points_cart)-1):
    # calc the length of the segment
    length = np.linalg.norm(points_cart[i+1] - points_cart[i])
    div = int(period_samples / total_length * length)
    x_space = np.linspace(i, i+1, div, endpoint=False)
    x_interpolated = np.interp(x_space, range(0, len(points_cart)), points_cart[:,0])
    y_space = np.linspace(i, i+1, div, endpoint=False)
    y_interpolated = np.interp(y_space, range(0, len(points_cart)), points_cart[:,1])

    for j in range(0, div):
        points_inter_list.append((x_interpolated[j], y_interpolated[j]))

points_inter = np.ndarray((len(points_inter_list), 2), dtype=np.float32)
for i in range(0, len(points_inter_list)):
    points_inter[i] = points_inter_list[i]

if args.verbose:
    print(f"{points_inter.shape[0]} points from interpolation")

# Normalize the audio

points_inter[:,0] = points_inter[:,0] - np.average(points_inter[:,0]) # center x
points_inter[:,1] = points_inter[:,1] - np.average(points_inter[:,1]) # center y

max = np.max(np.abs(points_inter))
points_inter = points_inter / max

if args.verbose:
    print("Audio normalized")

# Convert the points to audio and write file

length = int(args.sampling * args.duration / points_inter.shape[0]) * points_inter.shape[0]

signal = np.zeros((2, length), dtype=np.float32)
for i in range(0, length):
    signal[0,i] = points_inter[i % points_inter.shape[0],0]
    signal[1,i] = points_inter[i % points_inter.shape[0],1]

audiofile.write(output_path, signal, 48000, bit_depth=32)

if args.verbose:
    print(f"Saved to {output_path}. {args.sampling}, {length / args.sampling}s ")

# Plot the results of the interpolation

if args.plot:
    fig, axs = plt.subplots(2,3)
    axs[0,0].invert_yaxis()
    axs[0,0].plot(points_cart[:,0], points_cart[:,1], '.-')
    axs[1,0].invert_yaxis()
    axs[1,0].plot(points_inter[:,0], points_inter[:,1], '.-')
    axs[0,1].plot(x_raw, '.-')
    axs[1,1].plot(points_inter[:,0], '.-')
    axs[0,2].plot(y_raw, '.-')
    axs[1,2].plot(points_inter[:,1], '.-')
    plt.show()
    fig, axs = plt.subplots(2,1)
    axs[0].plot(points_inter[:,0], '.-')
    axs[1].plot(points_inter[:,1], '.-')
    plt.show()
