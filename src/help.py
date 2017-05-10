# -*- coding:utf-8 -*-

def shortHelp():
     print 'texdown.py -i [--input=] inFile.txd [-o [--output=] outFile.tex] [-s [--silent]] [--no-cleanup] [--no-pdf] [--no-head]'

def longHelp():
    print '''python texdown.py -i [--input=] inFile.txd [-o [--output=] outFile.tex] [-s [--silent]] [--no-cleanup] [--no-pdf] [--no-head]

Compiles a TeXDown file (.txd, .texd, .texdown) to a TeX file + PDF

Commands:

Input [-i] [--input]
    The TeXDown file to take as input. Accepts both relative and absolute paths.

Output [-o] [--output]
    The location and name to write to.
    If omitted, defaults to <input name>-compiled.tex
    Example:
        python texdown.py -i path/foo.txd -o my/path/bar
        
        Produces bar.tex + bar.pdf at my/path/.

Silent [-s] [--silent]
    Reduces output of pdflatex compiler, not omitting errors.

No Cleanup [--no-cleanup]
    Prevents removal of .aux and .log files after compilation.

No PDF [--no-pdf]
    Does not produce PDF file from pdflatex after .tex compilation.

No Head [--no-head]
    Outputs content between \begin{document} and \end{document} only.
'''