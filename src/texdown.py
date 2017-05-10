# -*- coding:utf-8 -*-

import interpreter
import sys, getopt
import os
import subprocess
from help import shortHelp,longHelp

try:
    opts, args = getopt.getopt(sys.argv[1:] ,"hi:o:s",["help","no-cleanup", "input=", "output=", "no-pdf", "silent", "no-head"])
except getopt.GetoptError as err:
    print err
    shortHelp()
    sys.exit(2)

inFile = ''
outPath = ''
noCleanup = False
noPdf = False
silent = False
noHead = False
for opt,arg in opts:
    if opt in ('-h', '--help'):
        longHelp()
        sys.exit()
    elif opt in ('-i', '--input'):
        inFile = arg
    elif opt in ('-o', '--output'):
        outPath = arg
    elif opt in ('-s', '--silent'):
        silent = True
    elif opt == '--no-cleanup':
        noCleanup = True
    elif opt == '--no-pdf':
        noPdf = True
    elif opt == '--no-head':
        noHead = True

if inFile == '':
    if len(args) > 0:
        inFile = args[0]
    else:
        print 'No input file given.'
        sys.exit(2)
inExtension = inFile[inFile.rfind('.'):]
inFile = inFile[:inFile.rfind('.')]

if outPath == '':
    if len(args) > 1:
        outPath = args[1]
    else:
        outPath = inFile + '-compiled' + ('-nohead' if noHead else '')

# Replace all in/out paths '\' for '/'
inFile = inFile.replace('\\', '/')
outPath = outPath.replace('\\', '/')

with open(inFile + inExtension) as sourceFile:
    source = sourceFile.read()

    print 'Outputting to ' + outPath + '.tex'

    with open(outPath + '.tex', 'w') as out:
        if not noHead:
            out.write(interpreter.makeHeader(source))
            out.write('\n')
        out.write(interpreter.makeBody(source))

    if not noHead and not noPdf:
        outDir = '' if outPath.rfind('/') < 0 else outPath[:outPath.rfind('/')+1]
        outName = outPath if outPath.rfind('/') < 0 else outPath[outPath.rfind('/')+1:]
        
        proc = subprocess.Popen(['pdflatex', 
            outName + '.tex',
            '--quiet' if silent else '',
            '--output-directory='+outDir]
        )
        proc.communicate()

        retcode = proc.returncode
        if not retcode == 0:
            os.unlink(outPath + '.tex')
            raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(proc))) 
    
        if not noCleanup:
            try:
                cleanupName = outDir + outName
                os.unlink(cleanupName + '.log')
                os.unlink(cleanupName + '.aux')
            except Exception as err:
                print 'Could not clean up: ' + str(err)

print 'Done!'