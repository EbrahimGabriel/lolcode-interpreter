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
        self.identifiers = [r'[a-zA-Z][a-zA-Z0-9_]*']

        self.literals = [r'(-?[1-9]+)|(0)', r'(-?[1-9][0-9]*\.[0.9]+)|(-?[0\.[0.9]+)', r'"[^"]*"', r'WIN|FAIL', r'NUMBA?R|YARN|TROOF']

        self.spacedkeywords = [r'I HAS A ', r'SUM OF ', r'DIFF OF ', r'PRODUKT OF ', r'QUOSHUNT OF ', r'MOD OF '
        , r'BIGGR OF ', r'SMALLR OF ', r'BOTH OF ', r'EITHER OF ', r'WON OF ', r'ANY OF ', r'ALL OF ', r'BOTH SAEM '
        , r'IS NOW A ', r'O RLY\? ', r'YA RLY ', r'NO WAI ', r'IM IN YR ', r'IM OUTTA YR ', r'HOW IZ I ', r'IF U SAY SO '
        , r'FOUND YR ', r'I IZ ']

        self.keywords = [r'HAI', r'KTHXBYE', r'WAZZUP', r'BUHBYE', r'ITZ', r'R', r'NOT', r'DIFFRINT', r'SMOOSH', r'MAEK', r'A'
        , r'VISIBLE', r'GIMMEH', r'MEBBE', r'OIC', r'WTF\?', r'OMG', r'OMGWTF', r'UPPIN', r'NERFIN', r'YR', r'TIL', r'WILE'
        , r'GTFO', r'MKAY']

        self.comments = r'( BTW .*\n)|(OBTW .*\n)|(TLDR\n)'
        
        '''
        notes:
        NUMBAR, NUMBR, YARN regex literals were changed to remove leading zeroes from NUMBR/NUMBARS and disallow " chars inside the YARN 
        
        categories:
        HAI/KTHXBYE = program start/end
        WAZZUP/BUHBYE = var declaration area start/end
        I HAS A/ITZ = var declaration/initialization
        NOOB/NUMBR/NUMBAR/YARN/TROOF = datatypes
        
        AN = operand separator
        VISIBLE/GIMMEH = I/O
        + = concatenation operator for VISIBLE
        SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF = arithmetic/mathematical 
        SMOOSH = concatenation
        BOTH OF, EITHER OF, WON OF, NOT, ALL OF, ANY OF = boolean
        MKAY = end of list for all of and any of?
        BOTH SAEM, DIFFRINT = comparison
        MAEK/IS NOW A = typecast/recast
        R = assignment
        O RLY?, YA RLY, MEBBE, NO WAI = if then
        WTF?, OMG, OMGWTF = switch 
        OIC = if then/switch end
        IM IN YR, IM OUTTA YR = loop start/end
        TIL/WILE = loop condition
        UPPIN/NERFIN = increment/decrement
        GTFO = break
        HOW IZ I/IF U SAY SO = function start/end
        YR = func parameters
        FOUND YR = return
        I IZ = function call
        '''
    
    #open a lolcode file
    def select_input(self):
        input_filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a File", filetypes=(("LOLCODE files", "*.lol"), ("all files", "*.*")))
        input_file = open(input_filename, "r")
        self.code = input_file.readlines()
        input_file.close()
    
    #tokenizes one line and returns its tokens
    def tokenize_line(self, line):
        #remove comments and replace with newline
        temp = re.sub(self.comments,  '\n', line)

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
        yarn = re.findall(self.literals[2], temp)
        if yarn: 
            for match in yarn:
                temp = re.sub(self.literals[2], "{"+str(count)+"}", temp, 1)
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
                if tokens[j] == tempstr2:
                    tokens[j] = substrings[i]+"\n"
                    
        print(tokens)
        return tokens
    
    #identifies a token
    def identify_token(self, token):
        pass

#testing
LOLCODE_Interpreter().tokenize_line('SUM OF 5 AN 7 BTW MEOWMEOW MEOW\n') #SUM OF, 5, AN, 7\n
LOLCODE_Interpreter().tokenize_line('ALL OF x AN y AN z MKAY\n') #ALL OF, x, AN, y, AN, z, MKAY\n
LOLCODE_Interpreter().tokenize_line('BOTH SAEM x AN BIGGR OF x AN y\n') #BOTH SAEM, x, AN, BIGGR OF, x, AN, y\n
LOLCODE_Interpreter().tokenize_line('VISIBLE "HELLO WORLD" + "MEOW MEOW"\n') #VISIBLE, "HELLO WORLD", +, "MEOW MEOW"\n

#starts the ui
# LOLCODE_Interpreter().mainloop()
