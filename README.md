# TeXDown

## What is TeXDown

TeXDown, as a set of three python scripts, `interpreter.py`, `texdown.py` and `help.py`,
is a transpiler that converts a Markdown/LaTex hybrid to LaTeX.

As a languange, TeXDown intends to be a custom flavour of markdown, with simple documents
and easy typing in mind, while still retaining LaTeX files' professional presentation.

It obeys to most of the [github-flavoured markdown standards][1],
while including other elements
(such as tab-to-center, easily gathered equations or macro defining tags), so that while it
may serve as a Markdown-To-LaTeX transpiler, it can also go beyond standard Markdown
capabilities and offer tools that help in writing math and LaTeX files in general.

---

## Using the compiler

A TexDown file can be compiled using the `texdown.py` script.

In the same directory as the `interpreter.py`, `texdown.py` and `help.py` scripts, run

```cmd
python texdown.py --help
```

for more details.

---

## What can TeXDown do

As of the time of writing, TeXDown features:

+ Text formatting:
  + Bold
  + Emphasis/itallics
  + Underline
  + Strikeout
+ Multiple formulas
  + Numbered
  + Unumbered
  + Easy centered formulas
+ Inline code
+ block code
  + With caption
+ Author/Date/Title tags
+ Easy macro tags
+ Easy include tags
+ Easy
  + theorems
  + lemmas
  + corollaries
    + Named
    + Unnamed
+ Sections
+ Blockquotes
+ Lists
  + Ordered
  + Unordered
+ Tables
  + Ugly
  + Pretty
    + With captions
+ Pure LaTeX
+ Images

and does not yet implement

+ Links

These are always updated in the `todo.md` file.

---

## Example file

An example file, `example.txd`, is provided, showing off most of TeXDown's capabilities.

---

## Why TeXDown

TeXDown doesn't intend to replace either Markdown or LaTeX. In fact, it is more useful
when used in conjunction with raw LaTeX; it eases the creation of templates or rough
document drafts, while maintaining ease of code reading, that can then be
further tweaked.

In this sense, TeXDown intends to bridge a gap between the powerful, but sometimes
cumbersome, LaTeX language, and the easy to read and write Markdown language.

Nonetheless, pure LaTeX in TeXDown isn't touched (unless recognized as a markdown
command), so it can always be used in a TeXDown file.

---

## Unit cases

### WYSIWYG

A blank TeXDown file is valid, compiling to an empty (with boilerplate code)
LaTeX file.

Some commonly used packages are already included.

**TeXDown file:**

<details>
<summary>TeXDown Source</summary>

```markdown

```

</details>

**TeX output:**
<details>
<summary>TeX Source Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage{caption}
\usepackage{amsthm}

\setlength{\jot}{8pt}
% End of header
% Start of body.

\begin{document}


\end{document}
% End of body.
```

</details>

---

### Standard markdow elements

Most [github-flavoured markdown][1] elements are supported, with the following differences:

+ Subitems in lists can't be order or unordered; they're of the same type
  as the parent list, and indicated with tabs or 4 spaces.
+ Raw HTML isn't (for obvious reasons) supported; however, LaTeX is, as long
  as it can't be interpreted as Markdown.
+ Please refer to `todo.md` for updates.

**TeXDown file:**

<details>
<summary>TeXDown Source</summary>

```markdown
# This is a section

## This is a subsection

### Subsubsection

#### Paragraph

##### Subparagraph

This is text,
and this is still the same paragraph.

** BOLD **

// italics (same as emphasis) // or *emphasis*

__underline__

** Some //really// __nested__ and I mean __//nested//__ formats. **

~~~strikeout~~~

~~strikeout w/ 2 tildes~~

`Some inline code?`

\```python
# SHOULD BE A COMMENT
print 'This is some code'
\```

Horizontal ruler:

---

or

***

. An
. Unordered
. List
    with
    sub
    items
        and
        sub
        items

1. A
2. Really
    Sexy
3. Ordered
4. List

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | \$1600 |
| col 2 is      | centered      |   \$12 |
| zebra stripes | are neat      |    \$1 |

~~Markdown~~ TeXDown | Less | Pretty
:--- | --- | ---
*Still* | `renders` | **nicely**
 1 | 2 | 3

Blockquotes are also supported:
> Here is a quote,
> made using TeXDown.
```

</details>

**TeX output:**

<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage[normalem]{ulem}
\usepackage{listings}
\usepackage{caption}
\usepackage{tabulary}
\usepackage{csquotes}
\usepackage{amsthm}

\setlength{\jot}{8pt}
% End of header
% Start of body.

\begin{document}

\section{This is a section}

\subsection{This is a subsection}

\subsubsection{Subsubsection}

\paragraph{Paragraph}

\subparagraph{Subparagraph}

This is text,
and this is still the same paragraph.

\textbf{BOLD}

\emph{italics (same as emphasis)} or \emph{emphasis}

\underline{underline}

\textbf{Some \emph{really} \underline{nested} and I mean \underline{\emph{nested}} formats.}

\sout{strikeout}

\sout{strikeout w/ 2 tildes}

\lstinline[columns=fixed]$Some inline code?$

\begin{lstlisting}[language=python,]
# SHOULD BE A COMMENT
print 'This is some code'
\end{lstlisting}

Horizontal ruler:

\vspace{0.2mm}\rule{\textwidth}{0.4pt}
\vspace{0.2mm}

or

\vspace{0.2mm}\rule{\textwidth}{0.4pt}
\vspace{0.2mm}

\begin{itemize}
\item An
\item Unordered
\item List
\begin{itemize}
\item with
\item sub
\item items
\begin{itemize}
\item and
\item sub
\item items
\end{itemize}
\end{itemize}
\end{itemize}
\begin{enumerate}
\item A
\item Really
\begin{enumerate}
\item Sexy
\end{enumerate}
\item Ordered
\item List
\end{enumerate}

\begin{table}[hbpt]
\noindent\makebox[\textwidth]{
\centering
\setlength{\tabcolsep}{10pt}
\renewcommand{\arraystretch}{1.5}
\begin{tabulary}{\paperwidth}{ |L|C|R|L| }
\hline
Tables & Are & Cool \\ \hline \hline
col 3 is & right-aligned & \$1600 \\ \hline
col 2 is & centered & \$12 \\ \hline
zebra stripes & are neat & \$1 \\ \hline
\end{tabulary}
}
\label{table1}
\end{table}

\begin{table}[hbpt]
\noindent\makebox[\textwidth]{
\centering
\setlength{\tabcolsep}{10pt}
\renewcommand{\arraystretch}{1.5}
\begin{tabulary}{\paperwidth}{ |L|L|L| }
\hline
\sout{Markdown} TeXDown & Less & Pretty \\ \hline \hline
\emph{Still} & \lstinline[columns=fixed]$renders$ & \textbf{nicely} \\ \hline
1 & 2 & 3 \\ \hline
\end{tabulary}
}
\label{table2}
\end{table}

Blockquotes are also supported:
\begin{displayquote}
Here is a quote,

made using TeXDown.
\end{displayquote}

\end{document}
% End of body.
```

</details>

---

### Inclusion of metadata and packages

Name, author or date of writing are all optional and can be defined at
any point in the document, using the tags:

```texdown
[author:My Name]
[title:My Title]
[date:The Date]
```

Packages can at any point be included, with optional arguments, using:

```texdown
[include:packageName,argument,argument]
```

**TeXDown file:**

<details>
<summary>TeXDown Source</summary>

```tex
Content.

[title:TeXDown Tests]
[author:Miguel Murça]
% Date is suppressed, but does not cause error!

More content.

[include:library, argument]
```

</details>

**LaTeX Output:**

<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage[argument]{library}
\usepackage{amssymb}
\usepackage{caption}
\usepackage{amsthm}

\setlength{\jot}{8pt}

\title{TeXDown Tests}
\author{Miguel Murça}
\date{}
% End of header
% Start of body.

\begin{document}

\maketitle
Content.

% Date is suppressed, but does not cause error!

More content.
\end{document}
% End of body.
```

</details>

---

### Easily define Commands

Custom commands can at any time be defined using any of the tags

```texdown
[define:command]
[macro:otherCommand]
```

They can include arguments, which are identified by `#number`:

**TeXDown file:**

<details>
<summary>TeXDown Source</summary>

```texdown
[define:myMacro,\LaTeX{} expanded content]

\myMacro

[define:macroWithArg, my name is #1]

\macroWithArg{TeXDown}
```

</details>

**LaTeX output:**

<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage{caption}
\usepackage{amsthm}

\newcommand{\myMacro}[0]{\LaTeX{} expanded content}
\newcommand{\macroWithArg}[1]{my name is #1}

\setlength{\jot}{8pt}
% End of header
% Start of body.

\begin{document}

\myMacro

\vspace{5mm}

\macroWithArg{TeXDown}
\end{document}
% End of body.
```

</details>

---

### Captions

Code and tables can easily be captioned:

**TeXDown code:**

<details>
<summary>TeXDown Source</summary>

```markdown
| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | \$1600 |
| col 2 is      | centered      |   \$12 |
| zebra stripes | are neat      |    \$1 |
    Table caption

```python

myStr = 'example'
def longExample:
    foo = input()
    bar = raw_input()

    for i in range(1,input()):
        pass
    # Long

```Code caption

```

</details>

**LaTeX output:**


<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage{listings}
\usepackage{caption}
\usepackage{tabulary}
\usepackage{amsthm}

\setlength{\jot}{8pt}
% End of header
% Start of body.

\begin{document}

\begin{table}[hbpt]
\noindent\makebox[\textwidth]{
\centering
\setlength{\tabcolsep}{10pt}
\renewcommand{\arraystretch}{1.5}
\begin{tabulary}{\paperwidth}{ |L|C|R|L| }
\hline
Tables & Are & Cool \\ \hline \hline
col 3 is & right-aligned & \$1600 \\ \hline
col 2 is & centered & \$12 \\ \hline
zebra stripes & are neat & \$1 \\ \hline
\end{tabulary}
}
\caption{
    Table caption
}
\label{table1}
\end{table}

\begin{lstlisting}[language=python,caption=Code caption]

myStr = 'example'
def longExample:
    foo = input()
    bar = raw_input()

    for i in range(1,input()):
        pass
    # Long

\end{lstlisting}
\end{document}
% End of body.
```

</details>

---

### Math

Inline math, block math, and gathered formulas are suported,
with or without numbering (using the `amsthm` package).

Braced equations are also supported, using the `empheq` package.

**TeXDown code:**

<details>
<summary>TeXDown Source</summary>

```markdown

Inline math:

$\sqrt{a^2 + b^2} = c$

Block math:

$$ \nabla^2 \psi = \frac{1}{v^2} \frac{\partial^2 \psi}{\partial t^2} $$

Multiple lines (numbered):

$$$
(x-1)^2 + y^2 = 1

x^2 - 2x + 1 + y^2 = 1

x^2 - 2x + y^2 = 0

r^2 - 2r \cos \theta = 0

r = 0 \lor r = 2 \cos \theta
$$$

Multiple lines (unnumbered):

$$$*
x^2 + (y-1)^2 = 1

x^2 + y^2 -2y = 0

r^2 - 2r \sin \theta = 0

r = 0 \lor r = 2 \sin \theta
$$$

Braced equations:

[braces]
    x^2 + (y-1)^2 = 1
    x^2 + y^2 -2y = 0
    r^2 - 2r \sin \theta = 0
    r = 0 \lor r = 2 \sin \theta

```

</details>

**LaTeX output:**


<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage{empheq}
\usepackage{caption}
\usepackage{amsthm}

\setlength{\jot}{8pt}
% End of header
% Start of body.

\begin{document}

Inline math:

$\sqrt{a^2 + b^2} = c$

Block math:

$$ \nabla^2 \psi = \frac{1}{v^2} \frac{\partial^2 \psi}{\partial t^2} $$

Multiple lines (numbered):

\begin{gather}
(x-1)^2 + y^2 = 1\\
x^2 - 2x + 1 + y^2 = 1\\
x^2 - 2x + y^2 = 0\\
r^2 - 2r \cos \theta = 0\\
r = 0 \lor r = 2 \cos \theta
\end{gather}

Multiple lines (unnumbered):

\begin{gather*}
x^2 + (y-1)^2 = 1\\
x^2 + y^2 -2y = 0\\
r^2 - 2r \sin \theta = 0\\
r = 0 \lor r = 2 \sin \theta
\end{gather*}

Braced equations:

\begin{empheq}[left=\empheqlbrace\,]{align}
& x^2 + (y-1)^2 = 1\\
& x^2 + y^2 -2y = 0\\
& r^2 - 2r \sin \theta = 0\\
& r = 0 \lor r = 2 \sin \theta
\end{empheq}

\end{document}
% End of body.
```

</details>

---

### Theorems, lemmas, and similar

Theorems, lemmas, and similar relevant blocks can be defined
with one of the following tags:

**TeXDown file:**

<details>
<summary>TeXDown Source</summary>

```texdown

[Theorem]
    Unnamed theorem.

[theorem:Name]
    A named theorem

[Lemma]
    A lemma

For example:

[theorem:Pythagorean Theorem]
    A rectangle triangle of sides $a$, $b$ and $c$ must be
    such that $a^2 + b^2 = c^2$

```

</details>

**LaTeX output:**

<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage{caption}
\usepackage{amsthm}

\setlength{\jot}{8pt}

\newtheorem{theorem0}{Theorem}
\newtheorem*{theorem1}{Name}
\newtheorem{theorem2}{Lemma}
\newtheorem*{theorem3}{Pythagorean Theorem}
% End of header
% Start of body.

\begin{document}

\begin{theorem0}
    Unnamed theorem.
\end{theorem0}

\begin{theorem1}
    A named theorem
\end{theorem1}

\begin{theorem2}
    A lemma
\end{theorem2}

For example:

\begin{theorem3}
    A rectangle triangle of sides $a$, $b$ and $c$ must be
    such that $a^2 + b^2 = c^2$
\end{theorem3}
\end{document}
% End of body.
```

</details>

---

### Images

Images can be included using standard Markdown syntax.

Images are automatically fit to the width of the page, as well as
labeled (with `\label`) with the name of the file (without the extension).

The image tags are `minipage` aware, so that two (or more) figures can be shown
side by side.

**TeXDown file:**

<details>
<summary>TeXDown Source</summary>

(A folder named `figures` is in the same directory as
the source file, and contains `graphA.png` and `graphB.png`.)

```texdown
[figpath:./figures/]

![A caption.](graphA)

![This figure has a longer caption
    because a lot of the time, science documents
    caption their figures with really long captions.](graphB)

\begin{minipage}[0.5\textwidth]
    ![Caption 1](img1)
\end{minipage}
\begin{minipage}[0.5\textwidth]
    ![Caption 2](img2)
\end{minipage}
```

</details>

**LaTeX output:**

<details>
<summary>TeX Output</summary>

```tex
% Start of header.
\documentclass{article}
\usepackage{lmodern}
\usepackage{graphicx}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{amssymb}
\usepackage{caption}
\usepackage{amsthm}

\setlength{\jot}{8pt}
\graphicspath{{./figures/}}
% End of header
% Start of body.

\begin{document}

\begin{figure}[hbtp]
\includegraphics[width=\textwidth,keepaspectratio]{graphA}
	\caption{A caption.}
	\label{graphA}
\end{figure}

\begin{figure}[hbtp]
\includegraphics[width=\textwidth,keepaspectratio]{graphB}
	\caption{This figure has a longer caption
		because a lot of the time, science documents
		caption their figures with really long captions.}
	\label{graphB}
\end{figure}

\begin{minipage}[0.5\textwidth]
	\centering
	\includegraphics[width=\textwidth,keepaspectratio]{img1}
	\captionof{figure}{Caption 1}
	\label{img1}

\end{minipage}
\begin{minipage}[0.5\textwidth]
	\centering
	\includegraphics[width=\textwidth,keepaspectratio]{img2}
	\captionof{figure}{Caption 2}
	\label{img2}

\end{minipage}
\end{document}
% End of body.
```

</details>

---

[1]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
