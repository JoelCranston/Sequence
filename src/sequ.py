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
    """Reads the command line arguements and returns them if they were two integers."""
    #http://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Returns the inclusive sequence between two integers')
    parser.add_argument('--version', action='version', version='%(prog)s "Compliance Level 0"')
    parser.add_argument('startNum',type=int, nargs=1, help='a starting integer')
    parser.add_argument('endNum',type=int, nargs=1, help='an ending integer')  
    args=parser.parse_args(['1', '11'])
    return args

def createSeq(numlist):
    """Checks the values and returns a list containing the sequence"""
    numSeq = []
    if numlist.startNum <= args.endNum:
        print("valid Input")
        return numSeq
    else:
        print("invalid input")
        return numSeq

# does not print each element correctly yet
def printSeq(lst):
    """Accepts one argument [lst] and prints the sequence of values in lst with each element seporated by a newline"""
    print("here be the output: " )
    print (lst)

       
if __name__ == "__main__":
    print("Sequ in running")
    args = parseArgs()
    seq = createSeq(args)
    printSeq(seq)
    print("Sequ is done")
