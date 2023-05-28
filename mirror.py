## Program to swap lines in txt file
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Swap lines in txt file")
parser.add_argument("file", help="file to swap lines in")

args = parser.parse_args()

if not os.path.isfile(args.file):
    print("File does not exist")
    sys.exit()

# Swap even lines with odd lines and save to new file but keep first word
with open(args.file, "r") as f:
    lines = f.readlines()

with open("m_" + args.file, "w") as f:
    # Split line into words
    for i in range(0, len(lines), 2):
        split_line = lines[i].split()
        split_line2 = lines[i + 1].split()
        f.write(split_line[0] + " " + split_line2[1] + "\n")
        f.write(split_line2[0] + " " + split_line[1] + "\n")