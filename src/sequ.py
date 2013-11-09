#!usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright ©2013 Joel Cranston
#
# sequ Prints a sequence of numbers to standard output.

__author__="Joel Cranston"
__date__ ="$2013$"

import argparse
#import math

def main():
    args = parseArgs()
    seqIterator = frange(args.first,args.last + args.increment, args.increment )
    args.format = processFormatString(args.format)
    printSeq(seqIterator,args) 
     
def parseArgs():
    """
    Reads the command line arguements and returns a Namespace object
    containing the command line arguments:
    first 
    last
    increment
    """
    #http://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Prints a sequence of numbres to standard output')
    parser.add_argument('-v','--version', action='version', version='%(prog)s "Compliance Level 1"')
    parser.add_argument('-f','--format=',metavar='FORMAT',dest='format', help='use printf style floating-point FORMAT')
    parser.add_argument('-s', '--separator=',metavar='STRING',dest='separator', help='use STRING to separate numbers')
    parser.add_argument('-w','--equal-width', dest='equalWidth', action='store_true',help='equalize width by padding with leading zeros')
    parser.add_argument('first', nargs='?', type=numberType, default='1', help='starting value')
    parser.add_argument('increment', nargs='?', type=numberType, default='1', help='increment')
    parser.add_argument('last', type=numberType, help='ending value') 
    #args=parser.parse_args(' 1 0 -1'.split())
    #args=parser.parse_args('-s "  " 0 1 13'.split())
    args=parser.parse_args()
    print('DEBUG - first: ',type(args.first),args.first)
    print('DEBUG - increment: ',type(args.increment),args.increment)
    print('DEBUG - last: ',type(args.last),args.last)
    print('DEBUG - format: ',type(args.format),args.format)
    print('DEBUG - separator: ',type(args.separator),args.separator)
    print('DEBUG - equal width: ',type(args.equalWidth),args.equalWidth)
    return args

# this function is used by argparse 
def numberType(argString):
    '''
    Takes a string and returns a float if there is a decimal point, otherwise returns a integer. 
    '''
    #http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
    num = float(argString) if '.' in argString else int(argString)    
    return num

# This function checks the format string and edits it if nessasary
def processFormatString(formatStr):
    #insert code here.
    return formatStr
    
def printSeq(iter,args):
    """
    Accepts a iterator and Namespace object.
    Prints each element seporated by seporator char and 
    displayed with printf style format string.
    """
    
    #args.separater = '\n'
    # numlength defaults to 1 if equalwidth is true set to max of first,last    
    # There is a Bug in Corutils seq for {-w -10 .1 10}, it does not pad correctly
    numLength=1
    if args.equalWidth:
        numLength = getNumLength(args.first,args.increment,args.last)

    #zfill pads zeros to the front after the sign
    #if no format specified use the default handling        
    if args.format == None:
        for i in iter:
            print(str(i).zfill(numLength),end=args.separator)
    else:
        #equal length strings are not attempted if format string is provided.
        for i in iter:
            print((args.format % i),end=args.separator)
    
    # print a backspace and newline if specifing a custom seporator.
    if args.separator != None:
        print('\b')
        
    print('DEBUG - ',args)
# returns the max lengh of a number between first and last by increments.
def getNumLength(first,increment,last):
    # if the increment is a float then make sure first and last are tested as floats.
    if type(increment) == float:
        numLength = max(len(str(float(first+increment))),len(str(float(last))),len(str(increment)))
    else:
        numLength = max(len(str(first)),len(str(last)))
    print('DEBUG - numlength = ',numLength)
    return numLength

#http://code.activestate.com/recipes/66472/
def frange(start, stop = None, step = 1):
    """frange generates a set of floating point or integer values over the 
    range [start, stop) with step size step

    frange([start,] stop [, step ])"""
    #avoid devide by zero and just yield start value endlessly
    #this is the same behavior as coreutils seq
    if step == 0:
        while True:
            yield start
    else:
        # create a generator expression for the index values
        indices = (i for i in range(0, int((stop-start)/step)))  
        # yield results rounding floats to 14 digits to avoid displaying most
        # floating point errors.
        for i in indices:
            yield round(start + step*i,14)


if __name__ == "__main__":
     main()
     
