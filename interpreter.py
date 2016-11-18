# -*- coding:utf-8 -*-

import re

metadataReg = re.compile(r'^\[(author|date|title): *(.+?)\]\n', re.IGNORECASE | re.MULTILINE)

codeEnvReg = re.compile(r'```([\w\d]+)*\n(.*?)\n```', re.DOTALL)
theoremEnvReg = re.compile(r'\[(?:theorem|corollary|lemma)(?:\:(.+?))*(?:, *(\d+))*\]\n((?:(?:\t| {4}).*\n+?)+)', re.IGNORECASE)
macroTagReg = re.compile(r'^\[macro:(\w+?), *(.+?)\]\n', re.MULTILINE|re.IGNORECASE)
includeTagReg = re.compile(r'^\[include: *([\w\d]+)((?:,[\w\d]+)*?)\]\n', re.MULTILINE)

mathEnvReg = re.compile(r'$$$\n(.*?)\n$$$', re.DOTALL)
emphasisReg = re.compile(r'(?:(?<!\*)\*(.*?)\*(?!\*))|(?:(?<!_)_(.*?)_(?!_))')
boldReg = re.compile(r'(?:\*\*(.*?)\*\*)|(?:__(.*?)__)')


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
    tags = includeTagReg.findall(source)
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
    macros = macroTagReg.findall(source)
    for macro in macros:
        # Find the highest argument number used;
        #   that's the ammount of args required.
        numberOfArgs = 0
        argNums = re.findall(r'(?<!\\)#(\d+?)', macro[1])
        if len(argNums) > 0:
            numberOfArgs = max(argNums)
        # Make macro
        addLine(r'\newcommand{{\{}}}[{}]{{{}}}'.format(macro[0], numberOfArgs, macro[1]))
    
    # Define theorems
    theorems = theoremEnvReg.findall(source)
    if len(theorems) > 0:
        theoremNumber = 0
        for theorem in theorems:
            newTheoremCommand = r'\newtheorem{{theorem{}}}'.format(theoremNumber)
            if theorem[0] != '':
                newTheoremCommand += r'{{{}}}'.format(theorem[0])
            if theorem[1] != '':
                newTheoremCommand += r'[{}]'.format(theorem[1])
            addLine(newTheoremCommand)
            theoremNumber += 1

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
    
    # "Clear" source copy without metadata tags
    clearSource = metadataReg.sub('', source)

    # Remove macro tags
    clearSource = macroTagReg.sub('', clearSource)

    # Remove include tags
    clearSource = includeTagReg.sub('', clearSource)

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

    # Replace all theorem tags with theorem envs.
    # Matching order from leftmost assures correct theorem name order
    #   but I'd enjoy something cleaner, while still detatching
    #   makeHead from makeBody
    global theoremNumber
    theoremNumber = -1
    def replaceWithName(match):
        global theoremNumber
        theoremNumber += 1
        return '\\begin{{theorem{}}}\n{}\\end{{theorem{}}}\n'.format(theoremNumber,match.group(3), theoremNumber)
    clearSource = theoremEnvReg.sub(replaceWithName, clearSource)

    # Add handled text
    addLine(clearSource)

    addLine(r'\end{document}')
    addLine(r'% End of body.')

    return compiled.strip()

print makeBody(open('example.txd').read())