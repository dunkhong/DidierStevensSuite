#!/usr/bin/env python

__description__ = 'This is essentially a wrapper for xml.etree.ElementTree'
__author__ = 'Didier Stevens'
__version__ = '0.0.4'
__date__ = '2020/01/12'

"""

Source code put in public domain by Didier Stevens, no Copyright
https://DidierStevens.com
Use at your own risk

History:
  2017/11/03: start
  2017/12/16: refactoring
  2017/12/16: 0.0.2 added elementtext and attributes command
  2017/12/31: added option -u
  2018/04/01: 0.0.3 added support for xmlns with single quote
  2018/06/29: 0.0.4 ProcessFile for Linux/OSX
  2020/01/12: added pretty print

Todo:
"""

import optparse
import glob
import collections
import time
import sys
import textwrap
import xml.etree.ElementTree
import re
import xml.dom.minidom

def PrintManual():
    manual = r'''
Manual:

xmldump.py can be used to extract information from XML files, it is essentially a wrapper for xml.etree.ElementTree.

This Python script was developed with Python 2.7 and tested with Python 2.7 and 3.7.

It reads one or more files or stdin to parse XML files. If no file arguments are provided to this tool, it will read data from standard input (stdin). This way, this tool can be used in a piped chain of commands.

The first argument to the tool is a command, which can be:
 text
 wordtext
 elementtext
 attributes
 pretty

Command text will extract all text from the elements in the XML file.
Example:
zipdump.py -s 4 -d test.docx | xmldump.py text

This is a test document.Second line.Third linehttps://DidierStevens.comLast line

Command wordtext will extract all text from <w:p> elements in the XML file and print each on a separate line.
Example:
zipdump.py -s 4 -d test.docx | xmldump.py wordtext

This is a test document.
Second line.
Third line
https://DidierStevens.com
Last line

Command elementtext will extract all elements with their text from the XML file.
Example:
zipdump.py -s 4 -d test.docx | xmldump.py elementtext

w:document: This is a test document.Second line.Third linehttps://DidierStevens.comLast line
w:body: This is a test document.Second line.Third linehttps://DidierStevens.comLast line
w:p: This is a test document.
w:r: This is a test document.
w:t: This is a test document.
w:p: Second line.
w:r: Second line.
w:t: Second line.
w:p: Third line
w:r: Third line
w:t: Third line
w:bookmarkStart:
w:bookmarkEnd:
w:p: https://DidierStevens.com
w:hyperlink: https://DidierStevens.com
w:r: https://DidierStevens.com
w:rPr:
w:rStyle:
w:t: https://DidierStevens.com
w:p: Last line
w:r: Last line
w:t: Last line
w:sectPr:
w:pgSz:
w:pgMar:
w:cols:
w:docGrid:

By default, the namespace URI (xmlns) is suppressed. Use option -u to include it.
Example:
zipdump.py -s 4 -d test.docx | xmldump.py -u elementtext

{http://schemas.openxmlformats.org/wordprocessingml/2006/main}document: This is a test document.Second line.Third linehttps://DidierStevens.comLast line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body: This is a test document.Second line.Third linehttps://DidierStevens.comLast line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p: This is a test document.
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r: This is a test document.
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t: This is a test document.
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p: Second line.
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r: Second line.
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t: Second line.
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p: Third line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r: Third line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t: Third line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkStart:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkEnd:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p: https://DidierStevens.com
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink: https://DidierStevens.com
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r: https://DidierStevens.com
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rStyle:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t: https://DidierStevens.com
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p: Last line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r: Last line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t: Last line
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgSz:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgMar:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cols:
{http://schemas.openxmlformats.org/wordprocessingml/2006/main}docGrid:

Command attributes will extract all attributes from the elements in the XML file.
Example:
zipdump.py -s 4 -d test.docx | xmldump.py attributes

w:document
  mc:Ignorable: w14 w15 w16se w16cid wp14
w:body
w:p
  w:rsidRDefault: 006E3AD4
  w:rsidR: 00F41D2A
w:r
w:t
w:p
  w:rsidRDefault: 006E3AD4
  w:rsidR: 006E3AD4
w:r
w:t
w:p
  w:rsidRDefault: 006E3AD4
  w:rsidR: 006E3AD4
w:r
w:t
w:bookmarkStart
  w:id: 0
  w:name: _GoBack
w:bookmarkEnd
  w:id: 0
w:p
  w:rsidRDefault: 006D313B
  w:rsidR: 006E3AD4
w:hyperlink
  w:history: 1
  r:id: rId4
w:r
  w:rsidRPr: 0074025F
  w:rsidR: 006E3AD4
w:rPr
w:rStyle
  w:val: Hyperlink
w:t
w:p
  w:rsidRDefault: 006E3AD4
  w:rsidR: 006E3AD4
w:r
w:t
w:sectPr
  w:rsidR: 006E3AD4
w:pgSz
  w:h: 15840
  w:w: 12240
w:pgMar
  w:left: 1440
  w:header: 720
  w:top: 1440
  w:right: 1440
  w:bottom: 1440
  w:footer: 720
  w:gutter: 0
w:cols
  w:space: 720
w:docGrid
  w:linePitch: 360

Command pretty will just perform a pretty print of the XML file.

By default, output is printed to the consolde (stdout). It can be directed to a file using option -o.
'''
    for line in manual.split('\n'):
        print(textwrap.fill(line))

def File2Strings(filename):
    try:
        f = open(filename, 'r')
    except:
        return None
    try:
        return map(lambda line:line.rstrip('\n'), f.readlines())
    except:
        return None
    finally:
        f.close()

def ProcessAt(argument):
    if argument.startswith('@'):
        strings = File2Strings(argument[1:])
        if strings == None:
            raise Exception('Error reading %s' % argument)
        else:
            return strings
    else:
        return [argument]

# CIC: Call If Callable
def CIC(expression):
    if callable(expression):
        return expression()
    else:
        return expression

# IFF: IF Function
def IFF(expression, valueTrue, valueFalse):
    if expression:
        return CIC(valueTrue)
    else:
        return CIC(valueFalse)

class cOutput():
    def __init__(self, filename=None):
        self.filename = filename
        if self.filename and self.filename != '':
            self.f = open(self.filename, 'w')
        else:
            self.f = None

    def Line(self, line):
        if self.f:
            self.f.write(line + '\n')
        else:
            try:
                print(line)
            except UnicodeEncodeError:
                encoding = sys.stdout.encoding
                print(line.encode(encoding, errors='backslashreplace').decode(encoding))
#            sys.stdout.flush()

    def Close(self):
        if self.f:
            self.f.close()
            self.f = None

def ExpandFilenameArguments(filenames):
    return list(collections.OrderedDict.fromkeys(sum(map(glob.glob, sum(map(ProcessAt, filenames), [])), [])))

class cOutputResult():
    def __init__(self, options):
        if options.output:
            self.oOutput = cOutput(options.output)
        else:
            self.oOutput = cOutput()
        self.options = options

    def Line(self, line):
        self.oOutput.Line(line)

    def Close(self):
        self.oOutput.Close()

def ProcessFile(fIn, fullread):
    if fullread:
        yield fIn.read()
    else:
        for line in fIn:
            yield line.strip('\n\r')

def XMLGetText(element):
    if sys.version_info[0] > 2:
        encoding = 'unicode'
    else:
        encoding = 'utf8'
    return xml.etree.ElementTree.tostring(element, encoding=encoding, method='text')

def TransformTag(tag, dXMLNS, includeURI):
    if includeURI:
        return tag
    elif tag.startswith('{'):
        uri, separator, remainder = tag[1:].partition('}')
        if uri in dXMLNS:
            if dXMLNS[uri] == '':
                return remainder
            else:
                return dXMLNS[uri] + ':' + remainder
        else:
            return tag
    else:
        return tag

def AnalyzeXMLNS(data):
    dXMLNS = {}
    for match in re.findall('xmlns(:([^=]+))?="([^"]+)"', data):
        dXMLNS[match[2]] = match[1]
    for match in re.findall("xmlns(:([^=]+))?='([^']+)'", data):
        dXMLNS[match[2]] = match[1]
    root = xml.etree.ElementTree.fromstring(data)
    return root, dXMLNS

def ExtractText(data, oOutput, options):
    root, dXMLNS = AnalyzeXMLNS(data)
    oOutput.Line(XMLGetText(root))

def ExtractWordText(data, oOutput, options):
    root, dXMLNS = AnalyzeXMLNS(data)
    for element in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        oOutput.Line(XMLGetText(element))

def ExtractElementText(data, oOutput, options):
    root, dXMLNS = AnalyzeXMLNS(data)
    for element in root.iter():
        oOutput.Line('%s: %s' % (TransformTag(element.tag, dXMLNS, options.includeuri), XMLGetText(element)))

def ExtractElementAttributes(data, oOutput, options):
    root, dXMLNS = AnalyzeXMLNS(data)
    for element in root.iter():
        oOutput.Line('%s' % (TransformTag(element.tag, dXMLNS, options.includeuri)))
        for key, value in element.items():
            oOutput.Line('  %s: %s' % (TransformTag(key, dXMLNS, options.includeuri), value))

def PrettyPrint(data, oOutput, options):
    oOutput.Line(xml.dom.minidom.parseString(data).toprettyxml())

dCommands = {'text': ExtractText, 'wordtext': ExtractWordText, 'elementtext': ExtractElementText, 'attributes': ExtractElementAttributes, 'pretty': PrettyPrint}

def ProcessTextFileSingle(command, filenames, oOutput, options):
    for filename in filenames:
        if filename == '':
            fIn = sys.stdin
        else:
            fIn = open(filename, 'r')
        data = fIn.read()
        if fIn != sys.stdin:
            fIn.close()

        dCommands[command](data, oOutput, options)

def ProcessTextFile(command, filenames, options):
    oOutput = cOutputResult(options)
    ProcessTextFileSingle(command, filenames, oOutput, options)
    oOutput.Close()

def Main():
    moredesc =  '\nCommands:\n%s' % ' '.join(dCommands.keys()) + '''

Arguments:
@file: process each file listed in the text file specified
wildcards are supported

Source code put in the public domain by Didier Stevens, no Copyright
Use at your own risk
https://DidierStevens.com'''

    oParser = optparse.OptionParser(usage='usage: %prog [options] command [[@]file ...]\n' + __description__ + moredesc, version='%prog ' + __version__)
    oParser.add_option('-m', '--man', action='store_true', default=False, help='Print manual')
    oParser.add_option('-u', '--includeuri', action='store_true', default=False, help='Include URI for the tags')
    oParser.add_option('-o', '--output', type=str, default='', help='Output to file')
    (options, args) = oParser.parse_args()

    if options.man:
        oParser.print_help()
        PrintManual()
        return

    if len(args) == 0:
        oParser.print_help()
        print('')
        print('  %s' % __description__)
        return

    command = args[0]

    if not command in dCommands:
        print('Invalid command: %s' % command)
        print('List of valid commands: %s' % ' '.join(dCommands.keys()))
        return

    if len(args) == 1:
        ProcessTextFile(command, [''], options)
    else:
        ProcessTextFile(command, ExpandFilenameArguments(args), options)

if __name__ == '__main__':
    Main()
