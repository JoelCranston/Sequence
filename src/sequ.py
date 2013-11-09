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
    print('DEBUG - ',args)
    
    
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
    parser.add_argument('-s', '--separator=',metavar='STRING',dest='seporator', help='use STRING to separate numbers')
    parser.add_argument('-w','--equal-width', dest='equalWidth', action='store_true',help='equalize width by padding with leading zeros')
    parser.add_argument('first', nargs='?', type=numberType, default='1', help='starting value')
    parser.add_argument('increment', nargs='?', type=numberType, default='1', help='increment')
    parser.add_argument('last', type=numberType, help='ending value') 
    #args=parser.parse_args('--f %#f 1 1 10'.split())
    args=parser.parse_args()
    
    print('DEBUG - first: ',type(args.first),args.first)
    print('DEBUG - increment: ',type(args.increment),args.increment)
    print('DEBUG - last: ',type(args.last),args.last)
    print('DEBUG - format: ',type(args.format),args.format)
    print('DEBUG - seporator: ',type(args.seporator),args.seporator)
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
    precision = 15 #default floating point precision.
    
    #if no format specified or equal width flag use the default handling
    if ~args.equalWidth and args.format == None:
        for i in iter:
            print(round(i,precision))#add end=seporator
    else:
        #test for precision?
        for i in iter:
            print(args.format % round(i,precision))#add end=seporator
    
    if args.seporator != '/n':
        print()
        
      
#http://code.activestate.com/recipes/66472/
def frange(start, stop = None, step = 1):
    """frange generates a set of floating point values over the 
    range [start, stop) with step size step

    frange([start,] stop [, step ])"""
    #avoid devide by zero
    assert step != 0
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
     
