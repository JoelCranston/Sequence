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
                        ['sequ','1.00','1.01','5.00'],
                        ['sequ','-3','1','3'],
                        ['sequ','10','-1','1'],
                        ['sequ','-f','abc%%def%-+0#2.2fabc','1','1','5'],
                        ['sequ','-s',':','5'],
                        ['sequ','-s','\\','1','5'],
                        ['sequ','-s','\n','1','1','5'],
                        ['sequ','--separator=',':--:','1','1','5'],
                        ['sequ','--separator',':\t:','1','1','5'],
                        ['sequ','-s',':\n:','1','1','5'],
                        ['sequ','--equal-width','-1','1','2'],
                        ['sequ','--format=','%.3f','9.9','.01','10.0'],
                        ['sequ','--format','%.3F','9.9','.01','10.0'],
                        ['sequ','-f','%.3e','9.9','.01','10.'],
                        ['sequ','-f','%.3E','9.9','.01','10.'],
                        ['sequ','-f','%.3g','9.9','.01','10.'],
                        ['sequ','-f','%.3G','9.9','.01','10.'],
                        ['sequ','-W','-1','1','3'],
                        ['sequ','--words','-1','1','3'],
                        ['sequ','-W','-s','\n','-1','1','3'],
                        ['sequ','-p','*','-1','1','3'],
                        ['sequ','-P','-1','1','3'],
                        ['sequ','--pad-spaces','-1','1','3'],
                        ['sequ','--pad','#','-1','1','3'],
                        ['sequ','--words','-p','#','-1','1','3'],                        
                        ['sequ','-w','5','1','10'],
                        ['sequ','-w','.1','0.01','.13'],
                        ['sequ','-w','-F','floating','1','10000','2'],
                        ['sequ','-w','-F','floating','5.01','1','10'],
                        ['sequ','-F','arabic','1','10'],
                        ['sequ','-F','floating','1','10'],
                        ['sequ','-F','alpha','e'],
                        ['sequ','-F','alpha','x','-1','n'],
                        ['sequ','-F','alpha','b','2','f'],
                        ['sequ','-F','alpha','a','e'],  
                        ['sequ','-F','ALPHA','C'],
                        ['sequ','-F','ALPHA','A','C'],
                        ['sequ','-F','ALPHA','B','2','F'],
                        ['sequ','-F','ALPHA','Z','-2','N'],
                        ['sequ','-s',': :','-F','ALPHA','A','1','D'],
                        ['sequ','--words','-F','ALPHA','A','1','D'],
                        ['sequ','-F','roman','10000','2'],
                        ['sequ','-F','ROMAN','1','10'],
                        ['sequ','-F','ROMAN','v'],
                        ['sequ','-F','ROMAN','i','v'],
                        ['sequ','-F','ROMAN','V','I','x'],
                        ['sequ','-F','ROMAN','--words','V','I','X'],
                        ['sequ','-s',': :','-F','ROMAN','I','I','V'],
                        ['sequ','-w','-F','ROMAN','I','I','V'],
                        ['sequ','-p','#','-F','ROMAN','I','I','V'],
                        ['sequ','-P','-F','ROMAN','I','I','V'],
                        ['sequ','-s',': :','-F','roman','v'],
                        ['sequ','-w','-F','roman','v'],
                        ['sequ','-p','#','-F','roman','v'],
                        ['sequ','-P','-F','roman','v'],
                        ['sequ','C'],
                        ['sequ','c'],
                        ]
        self.errors = [['sequ','-w','-10','.1','0'],
                       ['sequ','-F','alpha','1'],
                       ['sequ','-F','ALPHA','c'],
                       ['sequ','-F','ALPHA','4'],
                       ['sequ','-F','ROMAN','-1','I','V'],
                       ]                
        self.name = 'sequ'
        self.flags =['-f','-w','-s','-W','-p']
        self.formatStrings = ['%f','aa%%a%004.4faa','%++--g','%E',
                              '%F','%G','%#f','%0010.2f']
        self.separators=['','\n',':','a','\\','\t',' ',"'",',',':\n:','---','--\n']
        self.pads=[' ','0','#','-','\\']
        self.args = argparse.Namespace()
        self.args.equalWidth = False
        self.args.first = 1
        self.args.increment = 1
        self.args.last = 1
        self.args.format = None
        self.args.separator = DEFAULT_SEPARATOR
        self.args.pad = None

    def test_drange(self):
        print('Testing drange')
        print(list(drange('0','.10','1.2')))
        
    def test_parseArgs(self):
        print('Testing parseArgs')
        for i in self.argLists:
           sys.argv = i
           parseArgs()
        print()
           
    def DISABLEDtest_printSeq(self):
        self.args.pad = '0'
        print("Testing printSeq")
        print("Printing 1 to 4 with separators",self.separators)
        for i in range(len(self.separators)):
            print('separator = "%s"' % self.separators[i])
            self.args.separator = self.separators[i]
            printSeq(drange(1,1,5),self.args)
        self.args.separator=DEFAULT_SEPARATOR
        self.args.pad=None
        
        print("Testing with format strings")
        print(self.formatStrings)
        for i in range(len(self.formatStrings)):
            print('Formats string = "%s"' % self.formatStrings[i])
            self.args.format = self.formatStrings[i]
            printSeq(drange(1,1,5),self.args)
        
        self.args.equalWidth = True
        self.args.format=None
        self.args.first = decimal.Decimal("6")
        self.args.increment = decimal.Decimal("1")
        self.args.last = decimal.Decimal("10")
        
        print(self.pads)
        
        for i in self.pads:
            self.args.pad = i
            print("Printing equal width pads with args = %s" % str(self.args))
            iter= drange(self.args.first, self.args.increment, self.args.last)
            printSeq(iter,self.args)
        self.args.pad=None
        
    
    def test_drange(self):
        randomStart=random.randrange(-100,100,1)
        randomEnd=random.randrange(randomStart,1000,1)          
        iter= drange(randomStart,1,randomEnd)
        for i in range(randomStart,randomEnd):
            assert i == next(iter)
    

    def test_sequ(self):
        print('start of full app test')
        for i in self.argLists:
            print(i)
            sys.argv = i
            main()
if __name__ == '__main__':
    unittest.main()

