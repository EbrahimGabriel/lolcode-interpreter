'''
CMSC 124 Project
Hello World Group
Cid Jezreel Ceradoy, Ebrahim Gabriel, Reynaldo Isaac Jr.
'''

import re
import os as os
import tkinter as tk
from tkinter import filedialog

class LOLCODE_Interpreter(tk.Tk):
    def __init__(self):
        #ui stuff
        tk.Tk.__init__(self)
        self.title("LOLCODE Lexer")
        self.geometry("500x500")

        code_textbox = tk.Text(self, height = 12, width = 40)
        code_textbox.pack(expand=True)
        
        #contains identified lexemes and their tokens
        self.lexemes = []

        #regexes to consider
        #categorized
        self.identifiers = r'^([a-zA-Z][a-zA-Z0-9_]*)$'
        self.numbr = r'^((-?[1-9]+)|(0))$'
        self.numbar = r'^((-?[1-9][0-9]*\.[0.9]+)|(-?[0\.[0.9]+))$'
        self.yarn = r'^"[^"]*"$'
        self.troof = r'^(WIN|FAIL)$'
        self.datatype = r'^(NOOB|NUMBA?R|YARN|TROOF)$'
        self.progstart = r'^HAI$'
        self.progend = r'^KTHXBYE$'
        self.vardecstart = r'^WAZZUP$'
        self.vardecend = r'^BUHBYE$'
        self.vardec = r'^I HAS A$'
        self.varinit = r'^ITZ$'
        self.input = r'^GIMMEH$'
        self.output = r'^VISIBLE$'
        self.concatoperator = r'^\+$'
        self.arithmetic = r'^(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)$'
        self.opsep = r'^AN$'
        self.concat = r'^SMOOSH$'
        self.boolean = r'^(BOTH OF|EITHER OF|WON OF|NOT|ALL OF|ANY OF)$'
        self.endlist = r'^MKAY$'
        self.comparison = r'^(BOTH SAEM|DIFFRINT)$'
        self.typecast = r'^MAEK$'
        self.recast = r'^IS NOW A$'
        self.assign = r'^R$'
        self.ifstart = r'^O RLY\?$'
        self.ifif = r'^YA RLY$'
        self.elseif = r'^MEBBE$'
        self.elsekey = r'^NO WAI$'
        self.flowend = r'^OIC$'
        self.switchstart = r'^WTF\?'
        self.switchcase = r'^OMG$'
        self.switchdef = r'^OMGWTF$'
        self.loopstart = r'^IM IN YR$'
        self.loopend = r'^IM OUTTA YR$'
        self.increment = r'^UPPIN$'
        self.decrement = r'^NERFIN$'
        self.loopcond = r'^(TIL|WILE)$'
        self.breakkey = r'^GTFO$'
        self.funcstart = r'^HOW IZ I$'
        self.funcend = r'^IF U SAY SO$'
        self.params = r'^YR$'
        self.returnkey = r'^FOUND YR$'
        self.funccall = r'^I IZ$'
        self.linebreak = r'^\n$'

        self.comments = r'(( BTW .*\n)|(OBTW .*\n)|(TLDR\n))'

        #used in tokenizing
        self.spacedkeywords = [r'I HAS A ', r'SUM OF ', r'DIFF OF ', r'PRODUKT OF ', r'QUOSHUNT OF ', r'MOD OF '
        , r'BIGGR OF ', r'SMALLR OF ', r'BOTH OF ', r'EITHER OF ', r'WON OF ', r'ANY OF ', r'ALL OF ', r'BOTH SAEM '
        , r'IS NOW A ', r'O RLY\? ', r'YA RLY ', r'NO WAI ', r'IM IN YR ', r'IM OUTTA YR ', r'HOW IZ I ', r'IF U SAY SO '
        , r'FOUND YR ', r'I IZ ']

        self.spacedyarn = r'"[^"]*"'

        '''
        notes:
        + is the concat operator for VISIBLE
        NUMBAR, NUMBR, YARN regex literals were changed to remove leading zeroes from NUMBR/NUMBARS and disallow " chars inside the YARN 
        '''

    #open a lolcode file
    def select_input(self):
        input_filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a File", filetypes=(("LOLCODE files", "*.lol"), ("all files", "*.*")))
        input_file = open(input_filename, "r")
        self.code = input_file.readlines()
        input_file.close()
    
    #tokenizes one line and returns its tokens
    def tokenize_line(self, line):
        #remove comments
        temp = re.sub(self.comments,  '', line)
        temp = re.sub('\n', '', temp)

        count = 0
        substrings = []
        #get spaced keywords
        for regex in self.spacedkeywords:
            #extract the spaced keywords and place them in list to return them later
            if re.search(regex, temp) != None:
                regexstring = regex[:-1]
                temp = re.sub(regex, "{"+str(count)+"} ", temp)
                count = count + 1
                substrings.append(regexstring)
        
        #get YARNs with spaces between
        yarn = re.findall(self.spacedyarn, temp)
        if yarn: 
            for match in yarn:
                temp = re.sub(self.spacedyarn, "{"+str(count)+"}", temp, 1)
                count = count+1
                substrings.append(match)
        
        #split the line into its tokens, then return the spaced keywords to their original place
        tokens = re.split(' ', temp)
        for i in range(len(substrings)):
            tempstr = "{"+str(i)+"}"
            tempstr2 = "{"+str(i)+"}\n"
            for j in range(len(tokens)):
                if tokens[j] == tempstr:
                    tokens[j] = substrings[i]
        tokens.append('\n')
        return tokens
    
    #identifies a token
    def identify_token(self, token):
        if re.search(self.identifiers, token) != None:
            category = 'identifier'
        if re.search(self.numbr, token) != None:
            category = 'numbr'
        if re.search(self.numbar, token) != None:
            category = 'numbar'
        if re.search(self.yarn, token) != None:
            category = 'yarn'
        if re.search(self.troof, token) != None:
            category = 'troof'
        if re.search(self.datatype, token) != None:
            category = 'datatype'
        if re.search(self.progstart, token) != None:
            category = 'program start'
        if re.search(self.progend, token) != None:
            category = 'program end'
        if re.search(self.vardecstart, token) != None:
            category = 'variable declaration area start'
        if re.search(self.vardecend, token) != None:
            category = 'variable declaration area end'
        if re.search(self.vardec, token) != None:
            category = 'variable declaration'
        if re.search(self.varinit, token) != None:
            category = 'variable initialization'
        if re.search(self.input, token) != None:
            category = 'input'
        if re.search(self.output, token) != None:
            category = 'output'
        if re.search(self.concatoperator, token) != None:
            category = 'concatenation operator (VISIBLE)'
        if re.search(self.arithmetic, token) != None:
            category = 'arithmetic'
        if re.search(self.opsep, token) != None:
            category = 'operand separator'
        if re.search(self.concat, token) != None:
            category = 'concatenation'
        if re.search(self.boolean, token) != None:
            category = 'boolean'
        if re.search(self.endlist, token) != None:
            category = 'end of operands'
        if re.search(self.comparison, token) != None:
            category = 'comparison'
        if re.search(self.typecast, token) != None:
            category = 'typecast'
        if re.search(self.recast, token) != None:
            category = 'recast'
        if re.search(self.assign, token) != None:
            category = 'assignment'
        if re.search(self.ifstart, token) != None:
            category = 'if then start'
        if re.search(self.ifif, token) != None:
            category = 'if'
        if re.search(self.elseif, token) != None:
            category = 'else if'
        if re.search(self.elsekey, token) != None:
            category = 'else'
        if re.search(self.flowend, token) != None:
            category = 'flow control end'
        if re.search(self.switchstart, token) != None:
            category = 'switch start'
        if re.search(self.switchcase, token) != None:
            category = 'switch case'
        if re.search(self.switchdef, token) != None:
            category = 'switch default'
        if re.search(self.loopstart, token) != None:
            category = 'loop start'
        if re.search(self.loopend, token) != None:
            category = 'loop end'
        if re.search(self.increment, token) != None:
            category = 'increment'
        if re.search(self.decrement, token) != None:
            category = 'decrement'
        if re.search(self.loopcond, token) != None:
            category = 'loop condition'
        if re.search(self.breakkey, token) != None:
            category = 'break'
        if re.search(self.funcstart, token) != None:
            category = 'function start'
        if re.search(self.funcend, token) != None:
            category = 'function end'
        if re.search(self.params, token) != None:
            category = 'parameter'
        if re.search(self.returnkey, token) != None:
            category = 'function return'
        if re.search(self.funccall, token) != None:
            category = 'function call'
        if re.search(self.linebreak, token) != None:
            category = 'linebreak'

        return [token, category]

#testing
tokens = LOLCODE_Interpreter().tokenize_line('SUM OF 5 AN 7 BTW MEOWMEOW MEOW\n') #SUM OF, 5, AN, 7\n
for token in tokens:
    print(LOLCODE_Interpreter().identify_token(token))
LOLCODE_Interpreter().tokenize_line('ALL OF x AN y AN z MKAY\n') #ALL OF, x, AN, y, AN, z, MKAY\n
LOLCODE_Interpreter().tokenize_line('BOTH SAEM x AN BIGGR OF x AN y\n') #BOTH SAEM, x, AN, BIGGR OF, x, AN, y\n
LOLCODE_Interpreter().tokenize_line('VISIBLE "HELLO WORLD" + "MEOW MEOW"\n') #VISIBLE, "HELLO WORLD", +, "MEOW MEOW"\n

#starts the ui
# LOLCODE_Interpreter().mainloop()

#test-Rey
