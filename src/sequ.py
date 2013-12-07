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
VERSION = '%(prog)s "Compliance Level 4"'

# Define digit mapping for roman numerals
romanNumeralMap = (('M',  1000),('CM', 900),('D',  500),('CD', 400),('C',  100),('XC', 90),
                   ('L',  50),('XL', 40),('X',  10),('IX', 9),('V',  5),('IV', 4),('I',  1))


def main():
    
    args = parseArgs()   
    
    #Default separator for -n is space rather then newline.
    if args.separator is not DEFAULT_SEPARATOR:       
        args.separator = processSeparator(args.separator)
    else:
        if args.file is not None:
            args.separator = WORD_SEPARATOR
            
    if args.words is True:
        args.separator = WORD_SEPARATOR    
    # if no pad is specified use default of 0 for arabic and " " for roman
    # If one is specified set equal width to true so the pad will be used.
    if args.pad is None:
        if args.seqType.upper() == "ROMAN":
            args.pad = ' '
        else:  
            args.pad = DEFAULT_PAD 
    else:
        args.equalWidth=True 
        
    if args.equalWidth is True:
        args = getMaxSequenceLength(args)
    else:
        args.numLength=1
    
    if args.file is None:
        if args.seqType.upper() == "ALPHA":
            printAlphaSeq(args)
        else:
            printNumSeq(args) 
    else:
        printFromFile(args)
    return 1 


##
## Parses the command line arguments and returns a Namespace object with the options.
##
def parseArgs():
    #The parser first only processes the nonepositional arguments.
    parser = argparse.ArgumentParser(description='Prints a sequence of numbers or letters to standard output')
    parser.add_argument('-v','--version', action='version', version=VERSION)
    parser.add_argument('-f','--format','--format=',type=formatString, metavar='FORMAT', dest='format', help='use printf style floating-point FORMAT')
    parser.add_argument('-F','--format-word', type=formatWords, metavar='TYPE', dest='seqType', help='specifies a sequence type')
    parser.add_argument('-s','--separator','--separator=', metavar='STRING', type=str, dest='separator', default = DEFAULT_SEPARATOR, help='use STRING to separate numbers')
    parser.add_argument('-w','--equal-width', dest='equalWidth', action='store_true', help='equalize width by padding with leading zeros')
    parser.add_argument('-W','--words', dest='words', action='store_true', help='Output the sequence as single space separated line')
    parser.add_argument('-p','--pad', dest='pad', metavar='PAD', help='equalize width by padding with leading PAD char')
    parser.add_argument('-P','--pad-spaces', dest='pad', action='store_const', const=' ', help='equalize width by padding with leading spaces')
    parser.add_argument('-n','--number_lines', dest='file', help='Reads from a file inserting line numbers')
    preArgs=parser.parse_known_args()   
    #print('DEBUG-',preArgs)
    formatType = preArgs[0].seqType
    limitArgs = preArgs[1]
    
    #if there was no format type specified look at last positional arg to determine type, and update preArgs
    #if a file was specified then use the first limit arg rather then the last.
    if formatType is None:
        try:
            if preArgs[0].file is None:
                formatType = getType(limitArgs[-1])
            else:
                formatType = getType(limitArgs[0])
            preArgs[0].seqType = formatType
        except ValueError:
            parser.error('[%s] is not a valid ending value' % limitArgs[-1])
        except:
            #If there was not any limit argumnts provided.
            parser.error('a valid limit argument is required if [-F | --format-word] is not provided') 
    #can not accept alpha when numbering a file, as it could have more then 26 lines.        
    if formatType.upper() == 'ALPHA' and preArgs[0].file is not None:
        parser.error('format word [alpha | ALPHA] is incompatible with [-n | --number_lines]')
    #The positional arguments need to know what types they should accept.
    types=[floating,roman,LowerAlpha,UpperAlpha,arabic]
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
    if preArgs[0].file is None:
        parser.add_argument('last', type=types[limitType], help='ending value')
    else:
        preArgs[0].last=None
    args=parser.parse_args(args=limitArgs,namespace=preArgs[0])
    args.parser = parser
    #print('DEBUG-Final Args-',args)
    return args

##
## used by argparse to determine if format word is valid.
##
def formatWords(formatWord):
    match = re.search('arabic|floating|alpha|ALPHA|roman|ROMAN',formatWord)
    if match is None:
        raise argparse.ArgumentTypeError('Invalid format word')
    return formatWord
   
   
##            
## used by argparse to determine if a format string is valid.
##
def formatString(formatStr):
    match = re.search('\w*%[+0#-]*(\d*)(\.\d*)?[FfGgEe]\w*',formatStr)
    # if it matches the above regex then it can be passed to print safely
    if match is None:
        raise argparse.ArgumentTypeError('[%s] is not a valid format string' % formatStr)
    #print('DEBUG - ',match.group())    
    return formatStr


##
## Used by argparse to determine valid roman numerals, uppercase or lowercase. Or integers
## Always returns an integer or raises an exception
def roman(arg): 
    #print('DEBUG -roman()-',arg )
    if isUpperRoman(arg.upper()):
       return fromRoman(arg.upper())
    #print('DEBUG -roman()- not roman, checking int()')
    #int() will raise a valueError if it can not be converted to a int.
    try:
        value = int(arg)
    except:
         raise argparse.ArgumentTypeError('[%s] is not a valid roman numeral' % arg)
    if value < 1:
        raise argparse.ArgumentTypeError('[%s] is not a valid roman numeral' % arg)
    return value


##
## Used by arpParse ot determine valid arabic numerals
##
def arabic(arg):
    try:
        return int(arg)
    except:
        raise argparse.ArgumentTypeError('[%s] is not a valid integer' % arg)
 

##    
## used by argparse to determine valid LowerCase alphabetic chars.
##
def LowerAlpha(arg):
    if isLowerAlpha(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError('[%s] is not a valid lowercase alphabetic character' % arg)
    
    
##
## used by argparse to determine valid Uppercase alphabetic chars
##
def UpperAlpha(arg):
    if isUpperAlpha(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError('[%s] is not a valid uppercase alphabetic character' % arg) 
  
  
##    
## Used by argparse to determine if a floating point value is valid.
##
def floating(arg): 
    try:  
        return decimal.Decimal(arg)
    except:       
        raise argparse.ArgumentTypeError('[%s] is not a valid number' % arg)


##
## Upper case roman numeral
##
def isUpperRoman(value):
    #print('DEBUG-isUpperRoman()',value)
    match = re.search('(^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$)',str(value))
    if match is None:
        return False
    return True


##
## Lower case roman numeral
##
def isLowerRoman(value):
    #print('DEBUG-isLoworRoman()',value)
    match = re.search('(^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$)',str(value))
    if match is None:
        return False
    return True


##
## single uppercase A-Z character
##
def isUpperAlpha(value):
    #print('DEBUG -isUpperAlpha(string)-',value)
    match = re.match('^([A-Z])$',value)
    if match is None:
        return False
    return True


##
## single lowercase a-z character
##
def isLowerAlpha(value):
    #print('DEBUG -isLowerAlpha(string)-',value)
    match = re.match('^([a-z])$',str(value))
    if match is None:
        return False
    return True


##
## Matches the input to an avalible type.
##
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
    
    
##    
## converts from double backslash to escape char.
##
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
 
 
##    
## Takes a string and pads the front after the sign to length, with pad char.
##
def charfill(x, length, pad):
    if x[0] is '-':
        return '-' + x[1:].rjust(length-1,pad)
    return x.rjust(length,pad)


##        
## returns the max possible length of a numeric sequence including sign.
##
def maxNumLength(first,increment,last):
    first = decimal.Decimal(first)
    last = decimal.Decimal(last)
    #y.quantize(x) returns y with a mantissa the length x's mantissa
    lenFI=len(str(first.quantize(increment)))
    lenF=len(str(first))
    lenL=len(str(last))
    lenLI=len(str(last.quantize(increment)))
    #print('DEBUG - F, FI, L, LI:',lenF,lenFI,lenL,lenLI)
    return max(lenF,lenFI,lenL,lenLI)


##
## find the max length of a number or roman numeral sequence.
##
def getMaxSequenceLength(args):
    #alpha is limited to a single character.
    args.numLength = 1 
    if args.seqType.upper() == 'ALPHA':
        return args
    #for roman numerals check the length of each element produced by the generator.
    if args.seqType.upper() == "ROMAN":
        for i in drange(args.first, args.increment, args.last + args.increment):
            args.numLength = max(len(toRoman(i)),args.numLength)
    #for non roman we can use the maxNumLength function.
    else:      
        args.numLength = maxNumLength(args.first,args.increment,args.last)
    return args
   
            
##
## A decimal.Decimal based range function.
## http://code.activestate.com/recipes/66472/
def drange(start, step = 1, stop = None, precision = None):
    """drange generates a set of Decimal values over the
    range [start, stop) with step size step
    drange([start,]  step, stop [,precision]])"""
    # convert values to decimals if not already 
    start = decimal.Decimal(start)
    stop = decimal.Decimal(stop)
    step = decimal.Decimal(step)
    if step == decimal.Decimal('0'):
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
            

##
## converts a roman numeral to an int.
## http://www.diveintopython.net/unit_testing/stage_4.html
def fromRoman(s):
    """convert Roman numeral to integer"""
    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result

##
## converts a int to a roman numeral
## http://www.diveintopython.net/unit_testing/stage_2.html
def toRoman(n):
    """convert integer to Roman numeral"""
    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result

##
## Prints a Sequence of numbers based on defined args
##
def printNumSeq(args):
            
    #Create the sequence generator
    iter = drange(args.first, args.increment, args.last + args.increment)
    
    #print in uppercase roman numerals.
    if args.seqType == 'ROMAN':
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(toRoman(i)),args.numLength,args.pad))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            return   
        
    #Print in lowercase roman numerals
    if args.seqType == 'roman':
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(toRoman(i).lower()),args.numLength,args.pad))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            return

    #Prints integers and floats without format string
    #if no format string is specified use the default precision handling 
    if args.format is None:   
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(charfill(str(i),args.numLength,args.pad))
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()
            
    #Prints integers and floats with format string
    else:    
        try: 
            i = next(iter)
            while True:
                sys.stdout.write(args.format % i)
                i = next(iter)
                sys.stdout.write(args.separator)
        except StopIteration:
            print()


##
## Prints contents of a file to stdout inserting line numbering
##
def printFromFile(args):  
    filename = args.file 
    #Try to open the file and read the number of lines
    try:
        args.last = numberOfLines(filename)*args.increment
    except:
        args.parser.error('The file [%s] can not be opened' % filename) 
    
    #we can assume file is ok becase we already opened it to get number of lines.
    with open(filename, 'r') as file:        

        #print in uppercase roman numerals.
        if args.seqType == 'ROMAN':
            for lineNum in drange(args.first, args.increment, args.last+args.increment):
                number = charfill(str(toRoman(lineNum)),args.numLength,args.pad)
                buffer = file.readline()
                sys.stdout.write(args.separator.join((number,buffer)))
            return

        #Print in lowercase roman numerals
        if args.seqType == 'roman':
            for lineNum in drange(args.first, args.increment, args.last+args.increment):
                number = charfill(str(toRoman(lineNum).lower()),args.numLength,args.pad)
                buffer = file.readline()
                sys.stdout.write(args.separator.join((number,buffer)))
            return

        #Prints integers and floats without format string
        #if no format string is specified use the default precision handling 
        if args.format is None:   
            for lineNum in drange(args.first, args.increment, args.last+args.increment):
                number = charfill(str(lineNum),args.numLength,args.pad)
                buffer = file.readline()
                sys.stdout.write(args.separator.join((number,buffer)))

        #Prints integers and floats with format string
        else:  
            for lineNum in drange(args.first, args.increment, args.last+args.increment):
                number = (args.format % lineNum)
                buffer = file.readline()
                sys.stdout.write(args.separator.join((number,buffer)))
    #file.close() automaticaly called by using with
##
## Prints a sequence of letters
##
def printAlphaSeq(args):
    iter = drange(ord(args.first), args.increment, ord(args.last) + args.increment)
    try: 
        i = next(iter)
        while True:
            sys.stdout.write(str(chr(i)))
            i = next(iter)
            sys.stdout.write(args.separator)
    except StopIteration:
        print()     
        
##
## returns the number of text lines in a file.
## Throws FileNotFoundError if the file is not present.
def numberOfLines(filename):   
    with open(filename, 'r') as file:
        numberOfLines = 0
        for lines in file:
            numberOfLines += 1
    return numberOfLines


if __name__ == "__main__":
     main()
     
