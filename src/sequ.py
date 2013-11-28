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
import decimal
DEFAULT_SEPARATOR = '\n'
WORD_SEPARATOR = ' '
DEFAULT_PAD = '0'
VERSION = '%(prog)s "Compliance Level 3"'
float()
def main():
    args = parseArgs()
        
    if args.separator is not DEFAULT_SEPARATOR:
        args.separator = processSeparator(args.separator)
    if args.words is True:
        args.separator = WORD_SEPARATOR    
    # if no pad is specified use defalut 0 for use with -w. If one is specified
    # set equal width to true so it will be used.
    if args.pad is None:
        args.pad = DEFAULT_PAD 
    else:
        args.equalWidth=True
    
    seqIterator = drange(args.first, args.increment, args.last + args.increment)
    printSeq(seqIterator,args) 
    return 1


# Parces the command line arguments and returns a Namespace object with the options.   
def parseArgs():
    #http://docs.python.org/dev/library/argparse.html
    parser = argparse.ArgumentParser(description='Prints a sequence of numbres to standard output')
    parser.add_argument('-v','--version', action='version', version=VERSION)
    parser.add_argument('-f','--format','--format=',type=formatString, metavar='FORMAT', dest='format', help='use printf style floating-point FORMAT')
    parser.add_argument('-F','--format-word', type=formatWords, metavar='TYPE', dest='seqType', help='specifies a sequence type')
    parser.add_argument('-s','--separator','--separator=', metavar='STRING', type=str, dest='separator', default = DEFAULT_SEPARATOR, help='use STRING to separate numbers')
    parser.add_argument('-w','--equal-width', dest='equalWidth', action='store_true', help='equalize width by padding with leading zeros')
    parser.add_argument('-W','--words', dest='words', action='store_true', help='Output the sequence as single space separated line')
    parser.add_argument('-p','--pad', dest='pad', metavar='PAD', help='equalize width by padding with leading PAD char')
    parser.add_argument('-P','--pad-spaces', dest='pad', action='store_const', const=' ', help='equalize width by padding with leading spaces')
    parser.add_argument('first', nargs='?', type=decimal.Decimal, default='1', help='starting value')
    parser.add_argument('increment', nargs='?', type=decimal.Decimal, default='1', help='increment')
    parser.add_argument('last', type=decimal.Decimal, help='ending value') 
    args=parser.parse_args()
    #print('DEBUG-',args)
    return args

#used by argparse to determine if format word is valid.
def formatWords(formatWord):
    
    match = re.search('arabic|floating|alpha|ALPHA|roman|ROMAN',formatWord)
    if match is None:
        raise ValueError('Invalid format word')
    return formatWord
            
#used by argparse to determine if a format string is valid.
def formatString(formatStr):

    match = re.search('\w*%[+0#-]*(\d*)(\.\d*)?[FfGgEe]\w*',formatStr)
    # if it matches the above regex then it can be passed to print safely
    if match is None:
        raise ValueError('Invalid format string') 
    #print('DEBUG - ',match.group())    
    return formatStr
         
    
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
 
    
# Takes a string and pads the front after the sign to length, with pad char.    
def charfill(x, length, pad):
    if x[0] is '-':
        return '-' + x[1:].rjust(length-1,pad)
    return x.rjust(length,pad)

def printSeq(iter,args):
    """
    Accepts a iterator and Namespace object.
    Prints each element seporated by seporator char and 
    displayed with printf style format string.
    """
      
    numLength=1
    if args.equalWidth:       
        numLength = getMaxNumLength(args.first,args.increment,args.last)
    #print('DEBUG - numlength=',numLength)
    #if no format string is specified use the default precision handling 
    #we check for the existance of the next iter before printing the separator.
    if args.format == None:     
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(i),numLength,args.pad))
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


# returns the max possible number length including sign.
def getMaxNumLength(first,increment,last):
    #y.quantize(x) returns y with a mantissa the length x's mantissa
    lenFI=len(str(first.quantize(increment)))
    lenF=len(str(first))
    lenL=len(str(last))
    lenLI=len(str(last.quantize(increment)))
    #print('DEBUG - F, FI, L, LI:',lenF,lenFI,lenL,lenLI)
    return max(lenF,lenFI,lenL,lenLI)
    
        
            
#http://code.activestate.com/recipes/66472/
def drange(start, step = 1, stop = None, precision = None):
    """drange generates a set of Decimal values over the
    range [start, stop) with step size step
    drange([start,]  step, stop [,precision]])"""
    # convert values to decimals if not already 
    start = decimal.Decimal(start)
    stop = decimal.Decimal(stop)
    step = decimal.Decimal(step)

    if step is 0:
        while True:
            yield start
    else:
        # find precision (NOT USED YET.)
        if precision is not None:
            decimal.getcontext().prec = precision
        # create a generator expression for the index values
        indices = (i for i in range(0,(int((stop-start)/step)))) 
        # yield results
        for i in indices:
            yield start + step*i
            
if __name__ == "__main__":
     main()
     
