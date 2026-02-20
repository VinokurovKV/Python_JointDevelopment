import argparse

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

print(args)

