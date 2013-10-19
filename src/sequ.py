#!usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright ©2013 Joel Cranston
#
# sequ accepts 2 integers and inclusivly prints the integers between them.

__author__="Joel Cranston"
__date__ ="$Oct 18, 2013 11:46:17 AM$"

import argparse
    
def parseArgs():
    """
    Reads the command line arguements and returns a Namespace object
    containing integers startNum and endNum.
    """
    #http://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Returns the inclusive sequence between two integers')
    parser.add_argument('--version', action='version', version='%(prog)s "Compliance Level 0"')
    parser.add_argument('startNum',type=int, nargs=1, help='a starting integer')
    parser.add_argument('endNum',type=int, nargs=1, help='an ending integer')  
    args=parser.parse_args()
    #convert lists to int
    args.startNum = args.startNum[0]
    args.endNum = args.endNum[0]
    return args

def createSeq(numList):
    """
    Checks the values and returns a list containing the sequence.
    Returns an empty set if start number is greater then end number.
    """
    numSeq = []
    if numList.startNum <= numList.endNum:
        numSeq = [x for x in range(numList.startNum, numList.endNum + 1)]
    #else:
    #   print("DEBUG - invalid input")
    return numSeq


def printSeq(lst):
    """
    Accepts one argument [lst] and prints the sequence of values in lst 
    with each element seporated by a newline
    """
    for i in lst:
        print(i)
      
if __name__ == "__main__":
    args = parseArgs()
    seq = createSeq(args)
    printSeq(seq)   
