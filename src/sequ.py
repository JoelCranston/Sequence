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
    seq = createSeq(args)
    printSeq(seq) 
   
    
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
    #parser.add_argument('-f', nargs=1, help='printf type format string')
    #parser.add_argument('--format=',nargs=1, help='printf type format string')
    #parser.add_argument('-s', nargs=1, help='charactor to separate numbers')
    #parser.add_argument('--separator=')
    parser.add_argument('-w','--equal-width', dest='w', action='append_const', const='w', help='Pad number with zeros')
    parser.add_argument('first', nargs='?', type=numberType, default='1', help='starting value')
    parser.add_argument('increment', nargs='?', type=numberType, default='1', help='increment')
    parser.add_argument('last', type=numberType, help='ending value')  
    args=parser.parse_args('1 1 10'.split())
    
    print('DEBUG - first: ',type(args.first),args.first)
    print('DEBUG - increment: ',type(args.increment),args.increment)
    print('DEBUG - last: ',type(args.last),args.last)
    return args

def numberType(argString):
    '''
    Takes a string and returns a float if there is a decimal point, otherwise returns a integer. 
    '''
    #http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
    num = float(argString) if '.' in argString else int(argString)    
    return num

def createSeq(args):
    """
    Returns a list containing the sequence.
    Returns an empty set if start number is greater then end number.
    """
     
    numSeq = list(frange(args.first,args.last + args.increment, args.increment ))
    return numSeq


def printSeq(lst):
    """
    Accepts one argument [lst] and prints the sequence of values in lst 
    with each element seporated by a newline
    """
    for i in lst:
        print(i)
 
      
#http://code.activestate.com/recipes/66472/
def frange(start, stop = None, step = 1):
    """frange generates a set of floating point values over the 
    range [start, stop) with step size step

    frange([start,] stop [, step ])"""
    assert step > 0
    if stop is None:
        for x in range(int(ceil(start))):
            yield x
    else:
        # create a generator expression for the index values
        indices = (i for i in range(0, int((stop-start)/step)))  
        # yield results
        for i in indices:
            yield start + step*i


if __name__ == "__main__":
     main()
     
