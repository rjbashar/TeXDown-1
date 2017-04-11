# -*- coding:utf-8 -*-

import re

commentsReg = re.compile(r' *?%.+(?:\n|$)')

addToHeaderReg = re.compile(r'\[header\]\n((?:(?:\t| {4}).*(?:\n|$))+)', re.IGNORECASE | re.MULTILINE)
metadataReg = re.compile(r'^\[(author|date|title): *(.+?)\](?:\n|$)', re.IGNORECASE | re.MULTILINE)
macroTagReg = re.compile(r'^\[(?:macro|define): *(\w+?), *(.+?)\](?:\n|$)', re.MULTILINE|re.IGNORECASE)
includeTagReg = re.compile(r'^\[include: *([\w\d]+)((?:, ?[\w\d]+)*?)\](?:\n|$)', re.MULTILINE)
unincludeTagReg = re.compile(r'^\[(?:remove|uninclude): *([\w\d]+)\](?:\n|$)', re.MULTILINE)

theoremEnvReg = re.compile(r'\[(theorem|corollary|lemma|definition)(?:\:(.+?))*\]\n((?:(?:\t| {4}).*(?=\n|$))+)', re.IGNORECASE)
codeEnvReg = re.compile(r'(```|~~~~)([\w\d]+)*\n(.*?)\n\1([^\n]+)*', re.DOTALL)
mathEnvReg = re.compile(r'\$\$\$(\*)*(.*?)\$\$\$\*?', re.DOTALL)

sectionReg = re.compile(r'^(#+)(\*)? *(.+)', re.MULTILINE)

# These 3 could probably be fused and then get context from \1,
#   but it's much safer to have reg #1 and #2 separated
emphasisReg = re.compile(r'(\*|//) *((?:(?!\1).)+?) *\1(?!\1)')
boldReg = re.compile(r'(\*\*) *((?:(?!\1).)+?) *\1')
underlinedReg = re.compile(r'(__) *((?:(?!\1).)+?) *\1')

crossedReg = re.compile(r'(~{2,})(.+)\1')
inlineCodeReg = re.compile(r'`(.*?)`')

listTabSize = 4
ulistReg = re.compile(r'^(?:([\*\-+.]) +.+(?:\n|$)(?:(?:\t| {4}).+\n*)*)+', re.MULTILINE)
olistReg = re.compile(r'^(?:\d+\. *.+(?:\n|$)(?:(?:\t| {4}).+\n*)*)+', re.MULTILINE)

hlineReg = re.compile(r'^-{3,}|\+{3,}|\*{3,}$', re.MULTILINE)

# Markdown table regex
prettyTableReg = re.compile(r'^\s*\|\s*(.+)\n\s*\|(\s*[-:]+[-|\s:]*)\n((?:\s*\|.*(?:\n|$|\|))*)((?:.+\n|$)+)*', re.MULTILINE)
uglyTableReg = re.compile(r'^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)', re.MULTILINE)
tableAlignReg = re.compile(r':?-{3,}:?')

# Blockquote
blockquoteReg = re.compile(r'(?:^ *> *[^\n]+(?:\n|$))+', re.MULTILINE)

# Center aligned eqs.
centerEq = re.compile(r'^(?:\t| {4,})+(\$.+\$)$', re.MULTILINE)

def makeHeader(source):
    # Remove comments
    source = commentsReg.sub('', source)

    # Compiled tex string
    def addLine(*args):
        for line in args:
            addLine.compiled += line + '\n'
    addLine.compiled = ''

    addLine(r'% Start of header.')

    # Libs to include in the TeX file.
    # Include some useful predefined ones.
    includedLibs = {
        ('fontenc','T1'),
        ('inputenc','utf8'),
        ('amsmath',),
        ('amsthm',),
        ('amssymb',)
    }

    # MDTex files are always articles, as they're meant
    #   to be notes.
    addLine('\\documentclass{article}')

    # Check for user defined do not include packages
    tags = unincludeTagReg.findall(source)
    for tag in tags:
        found = False
        for included in includedLibs:
            if included[0] == tag:
                includedLibs.remove(included)
                found = True
                break
        if not found:
            raise Exception('Could not remove package {}, because it is not included!'.format(tag))

    # Check for user defined included packages
    tags = includeTagReg.findall(source)
    for tag in tags:
        newLib = []
        newLib.append(tag[0])
        if tag[1] != '':
            newLib += tag[1][1:].split(',')
        includedLibs.add(tuple(newLib))
    
    # If the code environment is used, include listings
    if codeEnvReg.search(source) or inlineCodeReg.search(source):
        includedLibs.add(('listings',))

    # If strikeout is used, include ulem
    if crossedReg.search(source):
        includedLibs.add(('ulem','normalem'))
    
    # If blockquote is used, include csquotes
    if blockquoteReg.search(source):
        includedLibs.add(('csquotes',))

    # Make library includes
    for lib in includedLibs:
        includeStr = r'\usepackage'
        if len(lib) > 1:
            includeStr += '['
            includeStr += ','.join(lib[1:])
            includeStr += ']'
        includeStr += '{{{}}}'.format(lib[0])

        addLine(includeStr)

    # Define macros/newcommand
    macros = macroTagReg.findall(source)
    if len(macros) > 0:
        addLine('')
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
        addLine('')
        theoremNumber = 0
        for theorem in theorems:
            newTheoremCommand = ''
            if theorem[1] != '':
                newTheoremCommand += r'\newtheorem*{{theorem{}}}'.format(theoremNumber)
                newTheoremCommand += r'{{{}}}'.format(theorem[1])
            else:
                newTheoremCommand += r'\newtheorem{{theorem{}}}'.format(theoremNumber)
                newTheoremCommand += r'{{{}}}'.format(theorem[0].lower().capitalize())
            addLine(newTheoremCommand)
            theoremNumber += 1

    # Look for title, author, date tags.
    #   LaTeX requires all or none.
    metadataTags = metadataReg.findall(source)
    if len(metadataTags) > 0:
        addLine('')
        title, author, date = '', '', ''
        for tag in metadataTags:
            if tag[0] == 'title':
                title = tag[1]
            elif tag[0] == 'author':
                author = tag[1]
            elif tag[0] == 'date':
                date = tag[1]
        addLine(r'\title{{{}}}'.format(title))
        addLine(r'\author{{{}}}'.format(author))
        addLine(r'\date{{{}}}'.format(date))
    
    # Look and add any custom header contents
    headerContents = addToHeaderReg.findall(source)
    if len(headerContents) > 0:
        addLine('')
        addLine(r'% Start of custom header contents')
        for match in headerContents:
            print match
            addLine(match.strip())
        addLine(r'% End of custom header contents')
        addLine('')

    addLine(r'% End of header')
    addLine('')
    return addLine.compiled.strip()


def makeBody(source):
    # Valid LaTeX for body of document, in string form.
    def addLine(*args):
        for line in args:
            addLine.compiled += line + '\n'
    addLine.compiled = ''
    
    addLine(r'% Start of body.')
    addLine('')
    addLine(r'\begin{document}')
    addLine('')

    # If any metadata was specified, make title page.
    if metadataReg.search(source):
        addLine(r'\maketitle')
    
    # "Clear" source copy without metadata tags
    clearSource = metadataReg.sub('', source)

    # Remove macro tags
    clearSource = macroTagReg.sub('', clearSource)

    # Remove uninclude tags
    clearSource = unincludeTagReg.sub('', clearSource)

    # Remove include tags
    clearSource = includeTagReg.sub('', clearSource)

    # Remove header tags
    clearSource = addToHeaderReg.sub('', clearSource)

    # strip
    clearSource = clearSource.strip()

    # Replace all code envs. with lstlisting codes
    def makelstlisting(match):
        language = r'language={}'.format(match.group(2)) if match.group(2) is not None else ''
        caption = r'caption={}'.format(match.group(4)) if match.group(4) is not None else ''
        code = match.group(3)
        return r'''\begin{{lstlisting}}[{}]
{}
\end{{lstlisting}}'''.format(','.join([language,caption]), code)
    clearSource = codeEnvReg.sub(makelstlisting, clearSource)

    # Define function to know if we're inside code env.
    def inCodeEnv(pos):
        if clearSource.count(r'\begin{lstlisting}', 0, pos) > clearSource.count(r'\end{lstlisting}', 0, pos):
            return True
        return False

    # Make inline code
    clearSource = inlineCodeReg.sub(r'\\lstinline[columns=fixed]$\1$', clearSource)

    # Replace all $$$ envs with equation environments
    #   and $$$* with equation* environements
    def returnEqEnv(match):
        return '\\begin{{gather{star}}}\n{}\n\\end{{gather{star}}}'.format(
            '\\\\\n'.join(
                map(lambda eq: ' '.join(eq.split('\n')), match.group(2).split('\n\n'))
            ).strip(),
            star = '*' if match.group(1) is not None else ''
        )
    clearSource = mathEnvReg.sub(returnEqEnv, clearSource)

    # Replace all theorem tags with theorem envs.
    # Matching order from leftmost assures correct theorem name order
    #   but I'd enjoy something cleaner, while still detatching
    #   makeHead from makeBody
    global theoremNumber
    theoremNumber = -1
    def replaceWithName(match):
        if inCodeEnv(match.end(0)):
            return match.group(0)
        global theoremNumber
        theoremNumber += 1
        return '\\begin{{theorem{}}}\n{}\n\\end{{theorem{}}}\n'.format(theoremNumber,match.group(3), theoremNumber)
    clearSource = theoremEnvReg.sub(replaceWithName, clearSource)

    # Make emphasis, bolds, underline and crossed out
    def makeFormat(command):
        def subFormat(match):
            if inCodeEnv(match.end(0)):
               return match.group(0) 
            return '\\{}{{{}}}'.format(command, match.group(2))
        return subFormat
    clearSource = boldReg.sub(makeFormat('textbf'), clearSource)
    clearSource = emphasisReg.sub(makeFormat('emph'), clearSource)
    clearSource = underlinedReg.sub(makeFormat('underline'), clearSource)
    clearSource = crossedReg.sub(makeFormat('sout'), clearSource)

    # Make all (sub)*sections
    def makeSection(match):
        if inCodeEnv(match.end(0)):
            return match.group(0)
        sectionDepth = match.group(1).count('#')
        depthKey = {
            1:'section',
            2:'subsection',
            3:'subsubsection',
            4:'paragraph',
            5:'subparagraph'
        }
        sectionType = depthKey.get(sectionDepth, 'subparagraph')
        return r'\{}{}{{{}}}'.format(sectionType, '' if match.group(2) is None else '*', match.group(3))
    clearSource = sectionReg.sub(makeSection, clearSource)

    # Make lists
    def makeList(group, elemRegex):
        def makeGroupList(match):
            if inCodeEnv(match.end(0)):
                return match.group(0)
            output = ''
            curDepth = -1
            for line in filter(None, match.group(0).split('\n')):
                depth = 0
                contentStart = 0
                for char in line:
                    if char not in (' ','\t'):
                        break
                    if char == ' ':
                        depth += 1
                    elif char == '\t':
                        depth += listTabSize
                    contentStart += 1
                depth/=listTabSize

                while depth > curDepth:
                    output += '\\begin{{{}}}\n'.format(group)
                    curDepth = depth
                while depth < curDepth:
                    output += '\\end{{{}}}\n'.format(group)
                    curDepth -= 1
                
                output += '\\item {}\n'.format(re.search(elemRegex, line).group(1))
            while curDepth > -1:
                output += '\\end{{{}}}\n'.format(group)
                curDepth -= 1
            return output
        return makeGroupList

    clearSource = ulistReg.sub(makeList('itemize', r'(?:[\*\-+.]?[ \t]*)?(.+)'), clearSource)
    clearSource = olistReg.sub(makeList('enumerate', r'(?:(?:\d+\.?)|[ \t])* *(.+)'), clearSource)

    # Make hotizontal line breaks
    clearSource = hlineReg.sub(r'\\rule{\\textwidth}{0.4pt}', clearSource)

    # Make tables
    def makeTables(match):
        if inCodeEnv(match.end(0)):
            return match.group(0)
        out = r'''\begin{table}[hbpt]
\setlength{\tabcolsep}{10pt}
\renewcommand{\arraystretch}{1.5}'''

        out += '\n\\begin{tabular}'
        
        # Get alignments
        alignLine = match.group(2)
        alignmentsWithSeparator = re.search(r'\s*\|?(.+)\|?\s*', alignLine).group(1)
        alignments = {}
        columns = alignmentsWithSeparator.split('|')
        position = 0
        for align in columns:
            align = align.strip()
            colonCount = align.count(':')
            if colonCount == 1 and align.find(':') * 1.0 / len(align) > 0.5:
                alignments[position] = 'r'
            elif colonCount == 2:
                alignments[position] = 'c'
            position += 1
        
        # Create tags
        out += '{ |' + '|'.join([alignments.get(i, 'l') for i in range(len(columns))]) + '| }'
        out += '\n\\hline\n'
        
        # Create table "header"
        header = match.group(1)
        if header[0] == '|':
            header = header[1:]
        if header[-1] == '|':
            header = header[:-1]
        elems = header.split('|')
        elems = map(lambda x: x.strip(), elems)
        out += ' & '.join(elems) + ' \\\\ \\hline \\hline\n'

        # Create actual table (skipping alignment lines)
        for line in match.group(3).splitlines():
            if line == '':
                continue
            line = line.strip()
            if line[0] == '|':
                line = line[1:]
            if line[-1] == '|':
                line = line[:-1]
            elems = line.split('|')
            elems = map(lambda x: x.strip(), elems)
            out += ' & '.join(elems) + ' \\\\ \\hline\n'
        
        # Find caption if available
        caption = '\\caption{{{}}}\n'.format(match.group(4)) if (len(match.groups()) > 3 and match.group(4) is not None) else ''

        out += r'''\end{{tabular}}
{}\label{{table{}}}
\end{{table}}
'''.format(caption, makeTables.tableNumber)
        makeTables.tableNumber += 1
        return out
    
    makeTables.tableNumber = 1

    clearSource = prettyTableReg.sub(makeTables, clearSource)
    clearSource = uglyTableReg.sub(makeTables, clearSource)
    
    # Make blockquotes
    def makeBq(match):
        if inCodeEnv(match.end(0)):
            return match.group(0)
        out = '\\begin{displayquote}\n'
        out += '\n\n'.join(map(lambda match: match[1], re.findall(r'( *> *)(.+)', match.group(0))))
        out += '\n\\end{displayquote}\n'
        return out
    clearSource = blockquoteReg.sub(makeBq, clearSource)

    # Make align shortcuts
    def makeAlign(match):
        if inCodeEnv(match.end(0)):
            return match.group(0)
        return '\\begin{{center}}\n{}\n\\end{{center}}'.format(match.group(1))
    clearSource = centerEq.sub(makeAlign, clearSource)

    # Escape double linebreaks as vspaces
    def makeVspaces(match):
        if inCodeEnv(match.end(0)):
            return match.group(0)
        return '\n\\vspace{5mm}\n\n'
    clearSource = re.sub(r'^\n\n', makeVspaces, clearSource, 0, re.MULTILINE)

    # Add handled text
    addLine(clearSource)

    addLine(r'\end{document}')
    addLine(r'% End of body.')

    return addLine.compiled.strip()