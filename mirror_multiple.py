import os
import argparse

parser = argparse.ArgumentParser(description="Swap lines in txt file")
parser.add_argument("file", help="file to swap lines in")
parser.add_argument("num", help="number of files to create")

args = parser.parse_args()


for i in range(1, int(args.num) + 1):
    filename = args.file + str(i) + ".txt"
    if not os.path.isfile(filename):
        print("File does not exist")
    else:
        os.system("python3 mirror.py " + filename)

print("Done")