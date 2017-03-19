# -*- coding:utf-8 -*-

def shortHelp():
     print 'compile.py -i [--input=] inFile.txd [-o [--output=] outFile.tex] [-s [--silent]] [--no-cleanup] [--no-pdf]'

def longHelp():
    print '''python compile.py -i [--input=] inFile.txd [-o [--output=] outFile.tex] [-s [--silent]] [--no-cleanup] [--no-pdf]

Compiles a TeXDown file (.txd, .texd, .texdown) to a TeX file + PDF

Commands:

Input [-i] [--input]
    The TeXDown file to take as input. Accepts both relative and absolute paths.

Output [-o] [--output]
    The location and name to write to.
    If omitted, defaults to <input name>-compiled.tex
    Example:
        python compile.py -i path/foo.txd -o my/path/bar
        
        Produces bar.tex + bar.pdf at my/path/.

Silent [-s] [--silent]
    Reduces output of pdflatex compiler, not omitting errors.

No Cleanup [--no-cleanup]
    Prevents removal of .aux and .log files after compilation.

No PDF [--no-pdf]
    Does not produce PDF file from pdflatex after .tex compilation.'''