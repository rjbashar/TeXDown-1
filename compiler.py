# -*- coding:utf-8 -*-

import interpreter
import sys, getopt
import os
import subprocess

def printHelp():
    print 'compile.py -i [--input=] inFile.txd [-o [--output=] outFile.tex] [--no-cleanup] [--no-pdf]'

try:
    opts, args = getopt.getopt(sys.argv[1:] ,"hi:o:",["help=","no-cleanup", "input=", "output=", "no-pdf"])
except getopt.GetoptError as err:
    print err
    printHelp()
    sys.exit(2)

inFile = ''
outName = ''
noCleanup = False
noPdf = False
for opt,arg in opts:
    if opt in ('-h', '--help'):
        printHelp()
        sys.exit()
    elif opt in ('-i', '--input'):
        inFile = arg
    elif opt in ('-o', '--output'):
        outName = arg
    elif opt == '--no-cleanup':
        noCleanup = True
    elif opt == '--no-pdf':
        noPdf = True

if inFile == '':
    if len(args) > 0:
        inFile = args[0]
    else:
        print 'No input file given.'
        sys.exit(2)
inExtension = inFile[inFile.rfind('.'):]
inFile = inFile[:inFile.rfind('.')]

if outName == '':
    if len(args) > 1:
        outName = args[1]
    else:
        outName = inFile + '-compiled'

with open(inFile + inExtension) as sourceFile:
    source = sourceFile.read()

    print 'Outputting to ' + outName + '.tex'

    with open(outName + '.tex', 'w') as out:
        out.write(interpreter.makeHeader(source))
        out.write('\n')
        out.write(interpreter.makeBody(source))
    
    if not noPdf:
        proc = subprocess.Popen(['pdflatex', outName + '.tex'])
        proc.communicate()

        retcode = proc.returncode
        if not retcode == 0:
            os.unlink(outName + '.tex')
            raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 
    
    if not noCleanup:
        try:
            os.unlink(outName + '.log')
            os.unlink(outName + '.aux')
        except:
            pass

print 'Done!'