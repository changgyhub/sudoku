import os
import sys


def main():
    ll = []
    file = open("log/ph-test.txt","r")
    for line in file:
        llist = line.split()
        ll.append(int(llist[0]))
    print(ll)


main()