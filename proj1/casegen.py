import random
import sys

count = 50000

if len(sys.argv)==2 and sys.argv[1].isdigit():
    count = int(sys.argv[1])

case = [random.choice("01") for _ in range(count)]

with open("case.txt", "w", encoding="utf-8") as f:
    print("".join(case), end="", file=f)
