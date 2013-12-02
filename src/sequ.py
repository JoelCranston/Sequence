#!usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright ©2013 Joel Cranston
#
# sequ Prints a sequence of numbers or letters to standard output.

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
    printSeq(args) 
    return 1 


# Parces the command line arguments and returns a Namespace object with the options.   
def parseArgs():
    #The preparser processes the nonepositional arguments.
    preparser = argparse.ArgumentParser(description='Prints a sequence of numbers or letters to standard output')
    preparser.add_argument('-v','--version', action='version', version=VERSION)
    preparser.add_argument('-f','--format','--format=',type=formatString, metavar='FORMAT', dest='format', help='use printf style floating-point FORMAT')
    preparser.add_argument('-F','--format-word', type=formatWords, metavar='TYPE', dest='seqType', help='specifies a sequence type')
    preparser.add_argument('-s','--separator','--separator=', metavar='STRING', type=str, dest='separator', default = DEFAULT_SEPARATOR, help='use STRING to separate numbers')
    preparser.add_argument('-w','--equal-width', dest='equalWidth', action='store_true', help='equalize width by padding with leading zeros')
    preparser.add_argument('-W','--words', dest='words', action='store_true', help='Output the sequence as single space separated line')
    preparser.add_argument('-p','--pad', dest='pad', metavar='PAD', help='equalize width by padding with leading PAD char')
    preparser.add_argument('-P','--pad-spaces', dest='pad', action='store_const', const=' ', help='equalize width by padding with leading spaces')
    preArgs=preparser.parse_known_args()
    #print('DEBUG-',preArgs)
    formatType = preArgs[0].seqType
    argList = preArgs[1]
    #CHECK FOR INVALID COMBOS (Parser,args)
    
    
    #if there was no format type specified look at last positional arg to determine type, and update preArgs
    if formatType is None:
        try:
            formatType = getType(argList[-1])
            preArgs[0].seqType = formatType
        except ValueError:
            preparser.error('[%s] is not a valid ending value' % argList[-1])
    #print("DEBUG-TypeCheck- ",formatType)  
    
    #The positional arguments need to know what types they should accept.
    parser = argparse.ArgumentParser()
    types=[floating,roman,LowerAlpha,UpperAlpha,int]
    parser.set_defaults(first='1')  
    limitType = 0
    incType = 0
    #limitType and incType are indexes into types[], which is a list of functions.
    if formatType.upper() == 'ROMAN':
        limitType = 1
        incType = 1
    if formatType == 'alpha':
        parser.set_defaults(first='a')
        limitType = 2
        incType = 4
    if formatType == 'ALPHA':
        parser.set_defaults(first='A')
        limitType = 3
        incType = 4
    if formatType == 'arabic':
        limitType = 4
        incType = 4 
    #print('Debug-types-',limitType,incType)     
    parser.add_argument('first', nargs='?', type=types[limitType], help='starting value')
    parser.add_argument('increment', nargs='?', type=types[incType], default='1', help='increment')
    parser.add_argument('last', type=types[limitType], help='ending value') 
    args=parser.parse_args(args=argList,namespace=preArgs[0])
    #print('DEBUG-Final Args-',args)
    return args



#used by argparse to determine if format word is valid.
def formatWords(formatWord):
    match = re.search('arabic|floating|alpha|ALPHA|roman|ROMAN',formatWord)
    if match is None:
        print('DEBUG - ',match.group())
        raise argparse.ArgumentTypeError('Invalid format word')
    return formatWord
            
#used by argparse to determine if a format string is valid.
def formatString(formatStr):
    match = re.search('\w*%[+0#-]*(\d*)(\.\d*)?[FfGgEe]\w*',formatStr)
    # if it matches the above regex then it can be passed to print safely
    if match is None:
        raise argparse.ArgumentTypeError('[%s] is not a valid format string' % formatStr)
    #print('DEBUG - ',match.group())    
    return formatStr

#used by argparse to determine valid roman numerals, uppercase or lowercase. Or integers
# Always returns an integer or raises an exception
def roman(arg): 
    #print('DEBUG -roman()-',arg )
    if isUpperRoman(arg.upper()):
       return fromRoman(arg.upper())
    #print('DEBUG -roman()- not roman, checking int()')
    #int() will raise a valueError if it can not be converted to a int.
    value = int(arg)
    if value < 1:
        raise argparse.ArgumentTypeError('[%s] is not a valid roman numeral' % arg)
    return value

#used by argparse to determine valid LowerCase alphabetic chars.
def LowerAlpha(arg):
    if isLowerAlpha(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError('[%s] is not a valid lowercase alphabetic character' % arg)
    
#used by argparse to determine valid Uppercase alphabetic chars
def UpperAlpha(arg):
    if isUpperAlpha(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError('[%s] is not a valid uppercase alphabetic character' % arg) 
    
#used by argparse to determine if a floating point value is valid.
def floating(arg): 
    try:  
        return decimal.Decimal(arg)
    except:       
        raise argparse.ArgumentTypeError('[%s] is not a valid number' % arg)
    
#used by argparse to determine valid integer values.
#def arabic(formatWord):
#    return int(formatWord)


#
# These test if a string is a member of a type.
#
#Upper case roman numeral
def isUpperRoman(value):
    #print('DEBUG-isUpperRoman()',value)
    match = re.search('(^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$)',str(value))
    if match is None:
        return False
    return True
#Lower case roman numeral
def isLowerRoman(value):
    #print('DEBUG-isLoworRoman()',value)
    match = re.search('(^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$)',str(value))
    if match is None:
        return False
    return True
#single uppercase A-Z character
def isUpperAlpha(value):
    #print('DEBUG -isUpperAlpha(string)-',value)
    match = re.match('^([A-Z])$',value)
    if match is None:
        return False
    return True
#single lowercase a-z character
def isLowerAlpha(value):
    #print('DEBUG -isLowerAlpha(string)-',value)
    match = re.match('^([a-z])$',str(value))
    if match is None:
        return False
    return True
#Try to match the input to avalible types.
def getType(string):
    if isUpperAlpha(string):
        return "ALPHA"
    if isLowerAlpha(string):
        return "alpha"
    if isUpperRoman(string):
        return "ROMAN"
    if isLowerRoman(string):
        return "roman"
    try:
        int(string)
        return "arabic"
    except: 
        pass 
    try:
        decimal.Decimal(string)
        return "floating"
    except:
        raise ValueError()
    
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

        
# returns the max possible number length including sign.
def getMaxNumLength(first,increment,last):
    #make sure they are decimal before calling quantize()
    first = decimal.Decimal(first)
    last = decimal.Decimal(last)
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
            
            
            
            
#Define digit mapping for roman numerals
romanNumeralMap = (('M',  1000),('CM', 900),('D',  500),('CD', 400),('C',  100),('XC', 90),
                   ('L',  50),('XL', 40),('X',  10),('IX', 9),('V',  5),('IV', 4),('I',  1))

#converts a roman numeral to an int.
#http://www.diveintopython.net/unit_testing/stage_4.html
def fromRoman(s):
    """convert Roman numeral to integer"""
    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result

# convert a int to a roman numeral
#http://www.diveintopython.net/unit_testing/stage_2.html
def toRoman(n):
    """convert integer to Roman numeral"""
    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result



def printSeq(args):
    """
    Accepts a iterator and Namespace object.
    Prints each element seporated by seporator char and 
    displayed with printf style format string.
    """  
      
    numLength = 1  
    if args.equalWidth: 
        #if we need to do equal witdth on roman, check the length of each element produced by the generator.
        if args.seqType.upper() == "ROMAN":
            for i in drange(args.first, args.increment, args.last + args.increment):
                numLength = max(len(toRoman(i)),numLength)
        #for non roman we can use the function.
        else:      
            numLength = getMaxNumLength(args.first,args.increment,args.last)   
    
    ##Prints alphabetic 
    if args.seqType.upper() == 'ALPHA':
        iter = drange(ord(args.first), args.increment, ord(args.last) + args.increment)
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(str(chr(i)))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            return 
    
    #Create the sequence generator.
    iter = drange(args.first, args.increment, args.last + args.increment)
    
    ##print in uppercase roman numerals.
    if args.seqType == 'ROMAN':
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(toRoman(i)),numLength,args.pad))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            return   
        
    ##Print in lowercase roman numerals
    if args.seqType == 'roman':
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(toRoman(i).lower()),numLength,args.pad))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            return

    ##Prints integers and floats without format string
    #if no format string is specified use the default precision handling 
    if args.format is None:   
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(i),numLength,args.pad))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            
    ##Prints integers and floats with format string
    else:    
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(args.format % i)
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()


if __name__ == "__main__":
     main()
     
