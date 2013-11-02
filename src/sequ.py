#!usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright ©2013 Joel Cranston
#
# sequ accepts 2 integers and inclusivly prints the integers between them.

__author__="Joel Cranston"
__date__ ="$Oct 18, 2013 11:46:17 AM$"

import argparse

def main():
    args = parseArgs()
    seq = createSeq(args)
    printSeq(seq)  
    #print(args.first)
    #print(args.increment)
    #print(args.last)
    
    
def parseArgs():
    """
    Reads the command line arguements and returns a Namespace object
    containing integers first and last.
    """
    #http://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Prints a sequence of numbres to standard output')
    parser.add_argument('-v','--version', action='version', version='%(prog)s "Compliance Level 1"')
    #parser.add_argument('-f', nargs=1, help='printf type format string')
    #parser.add_argument('--format=',nargs=1, help='printf type format string')
    #parser.add_argument('-s', nargs=1, help='charactor to separate numbers')
    #parser.add_argument('--separator=')
    parser.add_argument('-w','--equal-width', dest='w', action='append_const', const='w', help='Pad number with zeros')
    parser.add_argument('first', nargs='?', default='1', help='starting value')
    parser.add_argument('increment', nargs='?',  default='1', help='increment')
    parser.add_argument('last', help='ending value')  
    args=parser.parse_args('1 2 3'.split())
    return args

def createSeq(numList):
    """
    Checks the values and returns a list containing the sequence.
    Returns an empty set if start number is greater then end number.
    """
    numSeq = []
    if numList.first <= numList.last:
        numSeq = [x for x in range(numList.first, numList.last + 1)]
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
     main()
     
