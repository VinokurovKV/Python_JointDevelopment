import argparse
import cowsay

parser = argparse.ArgumentParser()

parser.add_argument("message1")
parser.add_argument("message2")

parser.add_argument("-e", dest="eyes1", default="oo")
parser.add_argument("-t", dest="tongue1", default="  ")
parser.add_argument("-f", dest="cow1", default="default")

parser.add_argument("-E", dest="eyes2", default="oo")
parser.add_argument("-N", dest="tongue2", default="  ")
parser.add_argument("-F", dest="cow2", default="default")

args = parser.parse_args()

cow1 = cowsay.cowsay(args.message1, eyes=args.eyes1, tongue=args.tongue1, cow=args.cow1)
cow2 = cowsay.cowsay(args.message2, eyes=args.eyes2, tongue=args.tongue2, cow=args.cow2)

cow1_lines = cow1.splitlines()
cow2_lines = cow2.splitlines()

w1 = max((len(s) for s in cow1_lines), default=0)
w2 = max((len(s) for s in cow2_lines), default=0)
h = max(len(cow1_lines), len(cow2_lines))

cow1_pad = [" " * w1] * (h - len(cow1_lines)) + cow1_lines
cow2_pad = [" " * w2] * (h - len(cow2_lines)) + cow2_lines

for l1, l2 in zip(cow1_pad, cow2_pad):
    print(l1.ljust(w1) + " " + l2)

