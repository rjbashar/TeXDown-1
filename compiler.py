# -*- coding:utf-8 -*-

import sys
import interpreter
import os
import subprocess

with open(sys.argv[1]) as sourceFile:
    source = sourceFile.read()
    outName = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1][:sys.argv[1].rfind('.')] + '-compiled'

    print 'Outputting to ' + outName + '.tex'

    with open(outName + '.tex', 'w') as out:
        out.write(interpreter.makeHeader(source))
        out.write('\n')
        out.write(interpreter.makeBody(source))
    
    proc = subprocess.Popen(['pdflatex', outName + '.tex'])
    proc.communicate()

    retcode = proc.returncode
    if not retcode == 0:
        os.unlink(outName + '.tex')
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 
    
    os.unlink(outName + '.log')
    os.unlink(outName + '.aux')

print 'Done!'