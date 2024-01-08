import re

class Semantic:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = [] #JUST VARIABLES
        self.condition_block = [] #CONTAINS IF-ELSE STATEMENTS
        self.loop_block = [] #CONTAINS LOOP STATEMENTS
        self.function_block = [] #CONTAINS FUNCTION STATEMENTS
        self.error = False
        self.end = False

        #list of categories that have an operation associated with it
        self.operation_categories = [
        'variable declaration', 
        'addition', 'difference', 'multiplication', 'division', 'modulo', 'max', 'min'
        'boolean', 'compare equal', 
        'output']
        
        self.arithmetic_categories = ['addition', 'difference', 'multiplication', 'division', 'modulo', 'max', 'min'] 

    def read_code(self):
        while not self.error and not self.end:
            for line in self.tokens:
                # print(line)
                self.check_operation(line)
        
        #do error related stuff here
    
    def check_operation(self, args):
        # print(args)
        if args[0][1] in self.operation_categories:
            if args[0][1] == 'variable declaration':
                self.var_dec(args)
            if args[0][1] in self.arithmetic_categories:
                self.arithmetic(args)
            if args[0][1] == 'boolean':
                self.and_all(args)
            if args[0][1] == 'compare equal':
                self.comparison(args)
            if args[0][1] == 'output':
                self.lol_print(args)
        if args[0][1] == 'program end':
            self.end = True

    def read_symbol_table(self, name):
        for symbol in self.symbol_table:
            if name == symbol[0]: #if match the identifier in symbol table
                return symbol #return the value
        else:
            return False

    def implicit_typecast(self, val, stype, etype): #start type, end type 
        ###NOT YET DONE
        if stype == 'numbar':
            if etype == 'troof':
                if val != 0:
                    return True
                else:
                    return False
            if etype == 'yarn':
                return str(val)
    
        if stype == 'numbr':
            if etype == 'numbar':
                return float(val)
            if etype == 'troof':
                if val != 0:
                    return True
                else:
                    return False
            if etype == 'yarn':
                return str(val)
        
        if stype == 'troof':
            if etype == 'numbar':
                if val == 'WIN':
                    return 1.0
                else:
                    return 0.0
            
            if etype == 'numbr':
                if val == 'WIN':
                    return 1
                else:
                    return 0
        
        if stype == 'yarn':
            if val.isdigit():
                if etype == 'numbar':
                    return float(val)
                if etype == 'numbr':
                    return int(val)

    #-----VAR DECLARATION-----
    def var_dec(self, args):
        if len(args) == 3: #keyword, identifier, linebreak
            temp = [args[1][0], 'NOOB']
            self.symbol_table.append(temp)
        elif len(args) == 5: #keyword, identifier, keyword, init value, linebreak
            #convert numbar and numbr into numeric, troof and yarns stay in string format
            if args[3][1] == 'numbar':
                val = float(args[3][0])
            elif args[3][1] == 'numbr':
                val = int(args[3][0])
            else:
                val = args[3][0]
            temp = [args[1][0], args[3][1], val]
            self.symbol_table.append(temp)
        else: #it has an expression
            
            ###CHECK WHAT KIND OF EXPRESSION
            if args[3][1] in self.arithmetic_categories:
                temp = []
                count = 3
                while args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                
                val = self.arithmetic(temp)
                if isinstance(val, float):
                    temp2 = 'numbar'
                else:
                    temp2 = 'numbr'

                temp = [args[1][0], temp2, val]
                self.symbol_table.append(temp)

    #-------------------------

#ADD NOOB CONSIDERATION

    #-----ARITHMETIC-----
    #NOT INFINITE ARITY! BUT CAN NEST INFINITELY(?)
    def arithmetic(self, args):

        numbar = False
        i = 3 #for nesting

        #check for numbar
        for arg in args:
            if arg[1] == 'identifier':
                symbol = self.read_symbol_table(arg[0])
                if symbol[1] == 'numbar':
                    numbar = True

            if arg[1] == 'numbar':
                numbar = True

        #1st value
        #if a variable, look it up in symbol table
        if args[1][1] == 'identifier':
            symbol = self.read_symbol_table(args[1][0])
            if symbol:
                if symbol[1] == 'numbar':
                    val1 = symbol[2]
                if symbol[1] == 'numbr':
                    if numbar:
                        val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    else:
                        val1 = symbol[2]
                if symbol[1] == 'troof':
                    if numbar:
                        val1 = self.implicit_typecast(symbol[2], 'troof', 'numbar')
                    else:
                        val1 = self.implicit_typecast(symbol[2], 'troof', 'numbr')
                if symbol[1] == 'yarn':
                    if numbar:
                        val1 = self.implicit_typecast(symbol[2], 'yarn', 'numbar')
                    else:
                        val1 = self.implicit_typecast(symbol[2], 'yarn', 'numbr')
                #NOOB
                else:
                    self.error = True
            else:
                self.error = True
        #not a variable, raw value is in the args
        elif args[1][1] in self.arithmetic_categories:
            temp = []
            temp.append(args[1])
            temp.append(args[2])
            temp.append(args[3])
            temp.append(args[4])

            val1 = self.arithmetic(temp)
            i += 3

        else:
            if args[1][1] == 'numbar':
                val1 = float(args[1][0])
            if args[1][1] == 'numbr':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                else:
                    val1 = int(args[1][0])
            if args[1][1] == 'troof':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'troof', 'numbar')
                else:
                    val1 = self.implicit_typecast(symbol[2], 'troof', 'numbr')
            if args[1][1] == 'yarn':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'yarn', 'numbar')
                else:
                    val1 = self.implicit_typecast(symbol[2], 'yarn', 'numbr')
        
        #2nd value
        if args[i][1] == 'identifier':
            symbol = self.read_symbol_table(args[i][0])
            if symbol:
                if symbol[1] == 'numbar':
                    val2 = symbol[2]
                if symbol[1] == 'numbr':
                    if numbar:
                        val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    else:
                        val2 = symbol[2]
                if symbol[1] == 'troof':
                    if numbar:
                        val2 = self.implicit_typecast(symbol[2], 'troof', 'numbar')
                    else:
                        val2 = self.implicit_typecast(symbol[2], 'troof', 'numbr')
                if symbol[1] == 'yarn':
                    if numbar:
                        val2 = self.implicit_typecast(symbol[2], 'yarn', 'numbar')
                    else:
                        val2 = self.implicit_typecast(symbol[2], 'yarn', 'numbr')
            else:
                self.error = True

        elif args[i][1] in self.arithmetic_categories:
            temp = []
            temp.append(args[i])
            temp.append(args[i+1])
            temp.append(args[i+2])
            temp.append(args[i+3])

            val2 = self.arithmetic(temp)

        else:
            if args[i][1] == 'numbar':
                val2 = float(args[i][0])
            if args[i][1] == 'numbr':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'numbr', 'numbar')
                else:
                    val2 = int(args[i][0])
            if args[i][1] == 'troof':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'troof', 'numbar')
                else:
                    val2 = self.implicit_typecast(symbol[2], 'troof', 'numbr')
            if args[i][1] == 'yarn':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'yarn', 'numbar')
                else:
                    val2 = self.implicit_typecast(symbol[2], 'yarn', 'numbr')

        if args[0][1] == 'addition':
            return val1 + val2
        elif args[0][1] == 'difference':
            return val1 - val2
        elif args[0][1] == 'multiplication':
            return val1 * val2
        elif args[0][1] == 'division':
            return val1 / val2
        elif args[0][1] == 'modulo':
            return val1 % val2
        elif args[0][1] == 'max':
            if val1 >= val2:
                return val1
            else:
                return val2
        elif args[0][1] == 'min':
            if val1 >= val2:
                return val2
            else:
                return val1
    #--------------------

    #-----BOOLEAN-----
    #NO CONSIDERATION FOR OTHER EXPRESSIONS WITHIN YET
    def and_all(self, args):
        count = 0
        values = []
        #iterate through all operands and append to values list
        while args[count][1] != 'end of operands':
            if args[count][1] == 'identifier':
                symbol = self.read_symbol_table(args[count][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        values.append(self.implicit_typecast(symbol[2], 'numbar', 'troof'))
                    if symbol[1] == 'numbr':
                        values.append(self.implicit_typecast(symbol[2], 'numbr', 'troof'))
                    if symbol[1] == 'troof':
                        if symbol[2] == 'WIN':
                            values.append(True)
                        else:
                            values.append(False) 
                    if symbol[1] == 'yarn':
                        values.append(self.implicit_typecast(symbol[2], 'yarn', 'troof'))
                else:
                    self.error = True
            else:
                if args[count][1] == 'numbar':
                    values.append(self.implicit_typecast(args[count][0], 'numbar', 'troof'))
                if args[count][1] == 'numbr':
                    values.append(self.implicit_typecast(args[count][0], 'numbr', 'troof'))
                if args[count][1] == 'troof':
                    if args[count][0] == 'WIN':
                        values.append(True)
                    else:
                        values.append(False) 
                if args[count][1] == 'yarn':
                    values.append(self.implicit_typecast(args[count][0], 'yarn', 'troof'))
            count += 1

        result = values[0]
        #use and comparison for all values
        for value in values:
            result = result and value
        print(result)


   #-----------------

   #-----COMPARISON-----
    #covers >= <= and ==
    #ONLY ASSUMES VALUES ARE NUMBR/NUMBAR, NO TROOF or YARN
    #NO CONSIDERATION FOR val2 IS NUMBAR YET!
    def comparison(self, args):
        numbar = False
        # not relational, ==
        if len(args) == 5: #keyword identifier keyword identifier linebreak
            #get values
            if args[1][1] == 'identifier':
                symbol = self.read_symbol_table(args[1][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val1 = symbol[2]
                        numbar = True
                    if symbol[1] == 'numbr':
                        if numbar:
                            val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                        else:
                            val1 = symbol[2]
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[1][1] == 'numbar':
                    numbar = True
                    val1 = float(args[1][0])
                if args[1][1] == 'numbr':
                    if numbar:
                        val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                    else:
                        val1 = int(args[1][0])
                if args[1][1] == 'troof':
                    self.error = True
                if args[1][1] == 'yarn':
                    self.error = True
            
            if args[3][1] == 'identifier':
                symbol = self.read_symbol_table(args[3][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val2 = symbol[2]
                        numbar = True
                    if symbol[1] == 'numbr':
                        if numbar:
                            val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                        else:
                            val2 = symbol[2]
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[3][1] == 'numbar':
                    numbar = True
                    val2 = float(args[3][0])
                if args[3][1] == 'numbr':
                    if numbar:
                        val2 = self.implicit_typecast(args[3][0], 'numbr', 'numbar')
                    else:
                        val2 = int(args[3][0])
                if args[3][1] == 'troof':
                    self.error = True
                if args[3][1] == 'yarn':
                    self.error = True

            print(val1 == val2)

        #is relational
        if len(args) == 8: #keyword identifier keyword keyword identifier keyword identifier linebreak
            #the first 2 values should be the same
            if args[1][0] != args[4][0]:
                self.error = True

            if args[1][1] == 'identifier':
                symbol = self.read_symbol_table(args[1][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val1 = symbol[2]
                        numbar = True
                    if symbol[1] == 'numbr':
                        if numbar:
                            val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                        else:
                            val1 = symbol[2]
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[1][1] == 'numbar':
                    numbar = True
                    val1 = float(args[1][0])
                if args[1][1] == 'numbr':
                    if numbar:
                        val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                    else:
                        val1 = int(args[1][0])
                if args[1][1] == 'troof':
                    self.error = True
                if args[1][1] == 'yarn':
                    self.error = True
            
            if args[6][1] == 'identifier':
                symbol = self.read_symbol_table(args[6][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val2 = symbol[2]
                        numbar = True
                    if symbol[1] == 'numbr':
                        if numbar:
                            val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                        else:
                            val2 = symbol[2]
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[6][1] == 'numbar':
                    numbar = True
                    val2 = float(args[6][0])
                if args[6][1] == 'numbr':
                    if numbar:
                        val2 = self.implicit_typecast(args[6][0], 'numbr', 'numbar')
                    else:
                        val2 = int(args[3][0])
                if args[6][1] == 'troof':
                    self.error = True
                if args[6][1] == 'yarn':
                    self.error = True
            
            #check if biggr of or smallr of and return proper expression
            if args[3][1] == 'max':
                print(val1 >= val2)
            else:
                print(val1 <= val2)
    #-----------------

    #-----OUTPUT-----
    def lol_print(self, args):
        count = 0
        values = []
        #iterate until find linebreak
        while(args[count][1] != 'linebreak'):
            if args[count][1] == 'identifier':
                symbol = self.read_symbol_table(args[count][0])
                if symbol:
                    #only need to typecast numbr/numbar into yarn
                    if symbol[1] == 'numbar':
                        values.append(self.implicit_typecast(symbol[2], 'numbar', 'yarn'))
                    if symbol[1] == 'numbr':
                        values.append(self.implicit_typecast(symbol[2], 'numbr', 'yarn'))
                    if symbol[1] == 'troof': #stored as string, no need to typecast
                        values.append(symbol[2])
                    if symbol[1] == 'yarn': #need to remove quotes
                        temp = re.sub("\"", "", symbol[2])
                        values.append(temp)
                    if symbol[1] == 'NOOB':
                        values.append("NOOB")
                else:
                    self.error = True

            elif args[count][1] in self.arithmetic_categories:
                temp = []
                while args[count][1] != 'concatenation operator (VISIBLE)' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1

                values.append(self.implicit_typecast(self.arithmetic(temp), 'numbar', 'yarn'))

            else: #raw value
                if args[count][1] == 'numbar':
                    values.append(self.implicit_typecast(args[count][0], 'numbar', 'yarn'))
                if args[count][1] == 'numbr':
                    values.append(self.implicit_typecast(args[count][0], 'numbr', 'yarn'))
                if args[count][1] == 'troof':
                    values.append(args[count][0])
                if args[count][1] == 'yarn':
                    temp = re.sub("\"", "", args[count][0])
                    values.append(temp)
            count += 1
        
        string = ''
        for value in values:
            string = string + value
        print(string)
    #----------------

SAMPLE_CODE = [
    [['HAI', 'program start'], ['\n', 'linebreak']], [['WAZZUP', 'variable declaration area start'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['I HAS A', 'variable declaration'], ['x', 'identifier'], ['ITZ', 'variable initialization'], ['3', 'numbr'], ['\n', 'linebreak']], 
    [['I HAS A', 'variable declaration'], ['y', 'identifier'], ['ITZ', 'variable initialization'], ['4', 'numbr'], ['\n', 'linebreak']], 
    [['BUHBYE', 'variable declaration area end'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['"+"', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['" = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['SUM OF', 'addition'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['"-"', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['" = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['DIFF OF', 'difference'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['"*"', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['" = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['PRODUKT OF', 'multiplication'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['"/"', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['" = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['QUOSHUNT OF', 'division'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['"%"', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['" = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['MOD OF', 'modulo'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['"max("', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['","', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['") = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['BIGGR OF', 'max'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['"min("', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['x', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['","', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['y', 'identifier'], ['+', 'concatenation operator (VISIBLE)'], ['") = "', 'yarn'], ['+', 'concatenation operator (VISIBLE)'], ['SMALLR OF', 'min'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['SUM OF', 'addition'], ['PRODUKT OF', 'multiplication'], ['x', 'identifier'], ['AN', 'operand separator'], ['x', 'identifier'], ['AN', 'operand separator'], ['PRODUKT OF', 'multiplication'], ['y', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['PRODUKT OF', 'multiplication'], ['SUM OF', 'addition'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['AN', 'operand separator'], ['SUM OF', 'addition'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['DIFF OF', 'difference'], ['BIGGR OF', 'max'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['AN', 'operand separator'], ['SMALLR OF', 'min'], ['x', 'identifier'], ['AN', 'operand separator'], ['y', 'identifier'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['SUM OF', 'addition'], ['x', 'identifier'], ['AN', 'operand separator'], ['SUM OF', 'addition'], ['QUOSHUNT OF', 'division'], ['y', 'identifier'], ['AN', 'operand separator'], ['x', 'identifier'], ['AN', 'operand separator'], ['FAIL', 'troof'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['SUM OF', 'addition'], ['x', 'identifier'], ['AN', 'operand separator'], ['SUM OF', 'addition'], ['QUOSHUNT OF', 'division'], ['"17"', 'yarn'], ['AN', 'operand separator'], ['x', 'identifier'], ['AN', 'operand separator'], ['FAIL', 'troof'], ['\n', 'linebreak']], 
    [['KTHXBYE', 'program end'], ['\n', 'linebreak']]
    ]

s = Semantic(SAMPLE_CODE)
s.read_code()

