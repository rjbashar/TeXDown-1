# -*- coding:utf-8 -*-

import re

metadataReg = re.compile(r'^\[(author|date|title):(.+?)\]$', re.IGNORECASE | re.MULTILINE)
anyTagReg = re.compile(r'^\[\w+(?:,.+?)*?\]$', re.MULTILINE)

codeEnvReg = re.compile(r'```([\w\d]+)*\n(.*?)\n```', re.DOTALL)

mathEnvReg = re.compile(r'$$($*)\n(.*?)\n($*)$$', re.DOTALL)
math

def makeHeader(source):
    # Compiled tex string
    global compiled
    compiled = ''
    def addLine(*args):
        global compiled
        for line in args:
            compiled += line + '\n'
    
    addLine(r'% Start of header.')

    # Libs to include in the TeX file.
    # Include some useful predefined ones.
    includedLibs = [
        ('inputenc','utf8'),
        ('amsmath',),
        ('amsthm',),
        ('amssymb',),
        ('url',)
    ]

    # MDTex files are always articles, as they're meant
    #   to be notes.
    addLine('\\documentclass{article}')

    # Check for user defined included packages
    tags = re.findall(r'^\[include:([\w\d]+)((?:,[\w\d]+)*?)\]$', source, re.MULTILINE)
    for tag in tags:
        newLib = []
        newLib.append(tag[0])
        if tag[1] != '':
            newLib += tag[1][1:].split(',')
        includedLibs.append(tuple(newLib))
    
    # If the code environment is used, include listings
    if codeEnvReg.match(source):
        includedLibs.append(('listings',))
    
    # Make library includes
    for lib in includedLibs:
        includeStr = r'\usepackage'
        if len(lib) > 1:
            includeStr += '['
            includeStr += ','.join(lib[1:])
            includeStr += ']'
        includeStr += '{{{}}}'.format(lib[0])

        addLine(includeStr)

    # Look for title, author, date tags.
    metadataTags = metadataReg.findall(source)
    if len(metadataTags) > 0:
        for tag in metadataTags:
            if tag[0] == 'title':
                addLine(r'\title{{{}}}'.format(tag[1]))
            elif tag[0] == 'author':
                addLine(r'\author{{{}}}'.format(tag[1]))
            elif tag[0] == 'date':
                addLine(r'\date{{{}}}'.format(tag[1]))
    
    # Define macros/newcommand
    macros = re.findall(r'^\[macro:(\w+?),(.+?)\]$', source, re.MULTILINE|re.IGNORECASE)
    for macro in macros:
        # Find the highest argument number used;
        #   that's the ammount of args required.
        numberOfArgs = 0
        argNums = re.findall(r'(?<!\\)#(\d+?)', macro[1])
        if len(argNums) > 0:
            numberOfArgs = max(argNums)
        # Make macro
        addLine(r'\newcommand{{\{}}}[{}]{{{}}}'.format(macro[0], numberOfArgs, macro[1]))

    addLine(r'% End of header')
    return compiled.strip()


def makeBody(source):
    # Valid LaTeX for body of document, in string form.
    global compiled
    compiled = ''
    def addLine(*args):
        global compiled
        for line in args:
            compiled += line + '\n'
    
    addLine(r'% Start of body.')
    addLine(r'\begin{document}')

    # If any metadata was specified, make title page.
    if metadataReg.match(source):
        addLine(r'\maketitle')
    
    # Get "actual" text, without any metadata tags
    clearSource = anyTagReg.sub('', source)

    # Replace all code envs. with lstlisting codes
    clearSource = codeEnvReg.sub(
r'''\\begin{lstlisting}[language=\1]
\2
\end{lstlisting}''', clearSource)

    # Replace all $$$ envs with gather* environments
    clearSource = mathEnvReg.sub(
r'''
\\begin{gather*}

\end{gather*}
'''
    , clearSource)

    addLine(r'\end{document}')
    addLine(r'% End of body.')

    return compiled.strip()

print makeBody(open('example.mtx').read())