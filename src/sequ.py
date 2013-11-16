#!usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright ©2013 Joel Cranston
#
# sequ Prints a sequence of numbers to standard output.

__author__="Joel Cranston"
__date__ ="$2013$"

import argparse
import re
import sys

DEFAULT_SEPARATOR = '\n'

def main():
    args = parseArgs()
    # Check the format string if it is supplied, returns None if invalid.
    if args.format != None:
        args.format = checkFormatString(args.format)
        if args.format == None:            
            return 0
    if args.separator != DEFAULT_SEPARATOR:
        args.separator = processSeparator(args.separator)
    seqIterator = frange(args.first, args.increment, args.last + args.increment)
    printSeq(seqIterator,args) 
    return 1


# Parces the command line arguments and returns a Namespace object with the options.   
def parseArgs():
    #http://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Prints a sequence of numbres to standard output')
    parser.add_argument('-v','--version', action='version', version='%(prog)s "Compliance Level 1"')
    parser.add_argument('-f','--format=',metavar='FORMAT',dest='format', help='use printf style floating-point FORMAT')
    parser.add_argument('-s','--separator=',metavar='STRING',dest='separator', default = DEFAULT_SEPARATOR, help='use STRING to separate numbers')
    parser.add_argument('-w','--equal-width', dest='equalWidth', action='store_true',help='equalize width by padding with leading zeros')
    parser.add_argument('first', nargs='?', type=numberType, default='1', help='starting value')
    parser.add_argument('increment', nargs='?', type=numberType, default='1', help='increment')
    parser.add_argument('last', type=numberType, help='ending value') 
    args=parser.parse_args()
    return args


# this function is only used by argparse to deturmine if the numbers are valid ints or floats.
def numberType(argString):
    '''
    Takes a string and returns a float if there is a decimal point, otherwise returns a integer. 
    '''
    #http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
    num = float(argString) if '.' in argString else int(argString)    
    return num


#converts from double backslash to escape char.
def processSeparator(separator):
    separator = separator.replace(r"\\",'\\')
    separator = separator.replace(r"\n",'\n')
    separator = separator.replace(r"\t",'\t')
    separator = separator.replace(r"\r",'\r')
    separator = separator.replace(r"\v",'\v')
    separator = separator.replace(r"\f",'\f')
    separator = separator.replace(r"\s",' ')
    separator = separator.replace(r"\'","'") 
    return separator
 
 
# This function checks the format string and edits it if nessasary
def checkFormatString(formatStr):

    match = re.search('\w*%[+0#-]*(\d*)(\.\d*)?[FfGgEe]\w*',formatStr)
    # if it matches the above regex then it can be passed to print safely
    if match is not None: 
        #print('DEBUG - ',match.group())
        return formatStr
    else:
        print("format string <%s> is not valid" % formatStr)
        return None
  
    
def printSeq(iter,args):
    """
    Accepts a iterator and Namespace object.
    Prints each element seporated by seporator char and 
    displayed with printf style format string.
    """
      
    numLength=1
    if args.equalWidth:       
        numLength = getMaxNumLength(args.first,args.increment,args.last)
    #zfill pads zeros to the front after the sign
    #if no format string is specified use the default precision handling 
    #we check for the existance of the next iter before printing the separator.
    if args.format == None:     
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(str(i).zfill(numLength))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()

    else:    
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(args.format % i)
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()

        
# returns the max lengh of a number between first and last by increment.
def getMaxNumLength(first,increment,last):
    lenInc = len(str(increment))
    lenFI = len(str(first+increment))
    lenLI = len(str(last-increment))
    if type(increment) == float:
        lenFirst = len(str(float(first)))
        lenLast = len(str(float(last)))
    else:
        lenFirst = len(str(first))
        lenLast = len(str(last))
    return max(lenInc,lenLast,lenFirst,lenFI,lenLI)



#http://code.activestate.com/recipes/66472/
def frange(start, step = 1, stop = None):
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
     
