# Copyright ©2013  Joel Cranston

import unittest
import argparse
from sequ import *
import random
import sys

class  Sequ_TestCase(unittest.TestCase):
    def setUp(self):
        self.argLists = [['sequ','1','1','5'],
                        ['sequ','1','5'],
                        ['sequ','-1'],
                        ['sequ','5'],
                        ['sequ','1.00','1.00','5.00'],
                        ['sequ','-3','1','3'],
                        ['sequ','10','-1','1'],
                        ['sequ','-f','abc%%def%-+0#2.2fabc','1','1','5'],
                        ['sequ','-s',':','5'],
                        ['sequ','-s','\\','1','5'],
                        ['sequ','-s','\n','1','1','5'],
                        ['sequ','-s',':-:','1','1','5'],
                        ['sequ','-s',':\t:','1','1','5'],
                        ['sequ','-s',':\n:','1','1','5'],
                        ['sequ','-w','-10','.1','1'],
                        ['sequ','-w','5','1','10'],
                        ['sequ','-f','%.3f','9.9','.01','10'],
                        ['sequ','-f','%.3F','9.9','.01','10'],
                        ['sequ','-f','%.3e','9.9','.01','10'],
                        ['sequ','-f','%.3E','9.9','.01','10'],
                        ['sequ','-f','%.3g','9.9','.01','10'],
                        ['sequ','-f','%.3G','9.9','.01','10'],
                        ]
        self.name = 'sequ'
        self.flags =['-f','-w','-s']
        self.formatStrings = ['%f','aa%%a%004.4faa','%++--g','%E',
                              '%F','%G','%#f','%0010.2f']
        self.separators=['','\n',':','a','\\','\t',' ',"'",',',':\n:','---','--\n']
        
        self.args = argparse.Namespace()
        self.args.equalWidth = False
        self.args.first = 1
        self.args.increment = 1
        self.args.last = 1
        self.args.format = None
        self.args.separator = DEFAULT_SEPARATOR

        
    def test_parseArgs(self):
        print('Testing parseArgs')
        for i in self.argLists:
           sys.argv = i
           parseArgs()
           
    def test_printSeq(self):
        print("Testing printSeq")
        print("Printing 1 to 4 with separators",self.separators)
        for i in range(len(self.separators)):
            print('separator = "%s"' % self.separators[i])
            self.args.separator = self.separators[i]
            printSeq(frange(1,1,5),self.args)
        self.args.separator=DEFAULT_SEPARATOR
        
        print("Testing with format strings")
        print(self.formatStrings)
        for i in range(len(self.formatStrings)):
            print('Formats string = "%s"' % self.formatStrings[i])
            self.args.format = self.formatStrings[i]
            printSeq(frange(1,1,5),self.args)
        
        self.args.equalWidth = True
        self.args.format=None
        self.args.first = -10
        self.args.last = 1
        self.args.increment = .1
        print("Printing equal width with args = %s" % str(self.args))
        printSeq(frange(-10,.1,1),self.args)
        
    def test_getMaxNumlength(self):
        startNum=-10#random.uniform(-10000,10000)
        endNum=10#random.uniform(randomStart,10000)
        increment=-.1#round(random.uniform(0,10),8)        
        iter = frange(startNum,increment,endNum)
        length = getMaxNumLength(startNum,increment,endNum)
        print(startNum,endNum,increment,length)
        for i in iter:
            assert len(str(i)) <= length
    
    def test_frange(self):
        randomStart=random.randrange(-100,100,1)
        randomEnd=random.randrange(randomStart,1000,1)          
        iter= frange(randomStart,1,randomEnd)
        for i in range(randomStart,randomEnd):
            assert i == next(iter)
    
    def test_numberType(self):
        for i in range(10):
            aRandomInt=random.randrange(100)
            aRandomFloat=random.uniform(-100,100) 
            assert type(numberType(str(aRandomInt))) == int
            assert type(numberType(str(aRandomFloat))) == float

    def test_sequ(self):
        print('start of full app test')
        for i in self.argLists:
            print(i)
            sys.argv = i
            main()
if __name__ == '__main__':
    unittest.main()

