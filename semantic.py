import re

'''
NO GIMMEH
ARITHMETIC NOT INFINITE ARITY
'''


class Semantic:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = [['IT', 'NOOB']] #JUST VARIABLES
        self.condition_block = [] #CONTAINS IF-ELSE STATEMENTS
        self.loop_block = [] #CONTAINS LOOP STATEMENTS
        self.function_block = [] #CONTAINS FUNCTION STATEMENTS
        self.toprint = []
        self.error = False
        self.end = False

        #list of categories that have an operation associated with it
        self.operation_categories = [
        'variable declaration', 
        'addition', 'difference', 'multiplication', 'division', 'modulo', 'max', 'min'
        'boolean', 'compare equal', 
        'output']
        
        self.arithmetic_categories = ['addition', 'difference', 'multiplication', 'division', 'modulo', 'max', 'min'] 
        self.comparison_categories = ['compare equal', 'compare diff']
    def read_code(self):
        while not self.error and not self.end:
            for line in self.tokens:
                self.check_operation(line)
        
        #do error related stuff here
    
    def check_operation(self, args):
        if args[0][1] in self.operation_categories:
            if args[0][1] == 'variable declaration':
                self.var_dec(args)
            if args[0][1] in self.arithmetic_categories:
                self.arithmetic(args)
            if args[0][1] == 'boolean':
                self.boolean(args)
            if args[0][1] in self.comparison_categories:
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
        ### NOT YET DONE
        if stype == 'numbar':
            if etype == 'numbr':
                return int(val)

            if etype == 'troof':
                if val != 0:
                    return True
                else:
                    return False
            if etype == 'yarn':
                return "\"" + str(val) + "\""
    
        if stype == 'numbr':
            if etype == 'numbar':
                return float(val)
            if etype == 'troof':
                if val != 0:
                    return True
                else:
                    return False
            if etype == 'yarn':
                return "\"" + str(val) + "\""
        
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
            
            if etype == 'yarn':
                return "\"" + val + "\""
        
        if stype == 'yarn':
            temp = val[1:-1]
            if temp.isdigit() and (etype == 'numbar' or etype == 'numbr'):
                if etype == 'numbar':
                    return float(temp)
                if etype == 'numbr':
                    return int(temp)
            
            elif etype == 'troof':
                return temp
            
            else: #yarn -> numbar/numbr while not a digit
                self.error = True
        
        if stype == 'NOOB':
            if etype == 'troof':
                return 'WIN'
            else: #no typecasting to other types
                self.error = True

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

        elif args[1][1] in self.arithmetic_categories:
            temp = []
            j = 2
            count = 0 #count how many values we've encountered
            #deeper nesting!
            if args[2][1] in self.arithmetic_categories:
                while count < 2:
                    if args[j][1] in self.arithmetic_categories:
                        count -= 1
                    if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                        count += 1
                    temp.append(args[j])
                    j += 1
                    i += 1
                i += 1
                val1 = self.arithmetic(temp)
            else:
                temp.append(args[1])
                temp.append(args[2])
                temp.append(args[3])
                temp.append(args[4])

                val1 = self.arithmetic(temp)
                i += 3

        #not a variable, raw value is in the args
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
                    val1 = self.implicit_typecast(args[1][0], 'troof', 'numbr')
            if args[1][1] == 'yarn':
                if numbar:
                    val1 = self.implicit_typecast(args[1][0], 'yarn', 'numbar')
                else:
                    val1 = self.implicit_typecast(args[1][0], 'yarn', 'numbr')
        
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
            j = i+1
            count = 0 #count how many values we've encountered
            #deeper nesting!
            if args[j][1] in self.arithmetic_categories:
                while count < 2:
                    if args[j][1] in self.arithmetic_categories:
                        count -= 1
                    if args[j][1] == 'identifier' or args[j][1] == 'numbar' or args[j][1] == 'numbr' or args[j][1] == 'troof' or args[j][1] == 'yarn':
                        count += 1
                    temp.append(args[j])
                    j += 1
                val2 = self.arithmetic(temp)

            else:
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
                    val2 = self.implicit_typecast(args[i][0], 'troof', 'numbr')
            if args[i][1] == 'yarn':
                if numbar:
                    val2 = self.implicit_typecast(args[i][0], 'yarn', 'numbar')
                else:
                    val2 = self.implicit_typecast(args[i][0], 'yarn', 'numbr')

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
    def boolean(self, args):
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
    #typecasts everthing into numbar, 2 = 2.0 and 3.5 = 3.5 so it shouldnt matter
    def comparison(self, args):
        temp = args
        if args[-1][1] == 'linebreak':
            del temp[-1]
        # not relational, == or !=
        if len(temp) == 4: #keyword identifier keyword identifier
            #get values
            if args[1][1] == 'identifier':
                symbol = self.read_symbol_table(args[1][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val1 = symbol[2]
                    if symbol[1] == 'numbr':
                        val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[1][1] == 'numbar':
                    val1 = float(args[1][0])
                if args[1][1] == 'numbr':
                    val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                if args[1][1] == 'troof':
                    self.error = True
                if args[1][1] == 'yarn':
                    self.error = True
            
            if args[3][1] == 'identifier':
                symbol = self.read_symbol_table(args[3][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val2 = symbol[2]
                    if symbol[1] == 'numbr':
                        val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[3][1] == 'numbar':
                    val2 = float(args[3][0])
                if args[3][1] == 'numbr':
                    val2 = self.implicit_typecast(args[3][0], 'numbr', 'numbar')
                if args[3][1] == 'troof':
                    self.error = True
                if args[3][1] == 'yarn':
                    self.error = True

            if args[0][1] == 'compare equal':
                if val1 == val2:
                    return 'WIN'
                else:
                    return 'FAIL'
            else:
                if val1 != val2:
                    return 'WIN'
                else:
                    return 'FAIL'

        #is relational
        if len(temp) == 7: #keyword identifier keyword keyword identifier keyword identifier
            #the first 2 values should be the same
            if args[1][0] != args[4][0]:
                self.error = True

            if args[1][1] == 'identifier':
                symbol = self.read_symbol_table(args[1][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val1 = symbol[2]
                    if symbol[1] == 'numbr':
                            val1 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[1][1] == 'numbar':
                    val1 = float(args[1][0])
                if args[1][1] == 'numbr':
                    val1 = self.implicit_typecast(args[1][0], 'numbr', 'numbar')
                if args[1][1] == 'troof':
                    self.error = True
                if args[1][1] == 'yarn':
                    self.error = True
            
            if args[6][1] == 'identifier':
                symbol = self.read_symbol_table(args[6][0])
                if symbol:
                    if symbol[1] == 'numbar':
                        val2 = symbol[2]
                    if symbol[1] == 'numbr':
                        val2 = self.implicit_typecast(symbol[2], 'numbr', 'numbar')
                    if symbol[1] == 'troof':
                        #make an error for now
                        self.error = True
                    if symbol[1] == 'yarn':
                        self.error = True
                else:
                    self.error = True
            else:
                if args[6][1] == 'numbar':
                    val2 = float(args[6][0])
                if args[6][1] == 'numbr':
                    val2 = self.implicit_typecast(args[6][0], 'numbr', 'numbar')
                if args[6][1] == 'troof':
                    self.error = True
                if args[6][1] == 'yarn':
                    self.error = True
            
            #check if biggr of or smallr of and return proper expression
            if args[0][1] == 'compare equal':
                if args[3][1] == 'max':
                    if val1 >= val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
                else:
                    if val1 <= val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
            else:
                if args[3][1] == 'max':
                    if val1 > val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
                else:
                    if val1 < val2:
                        return 'WIN'
                    else:
                        return 'FAIL'
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
                        values.append(self.implicit_typecast(symbol[2], 'troof', 'yarn'))
                    if symbol[1] == 'yarn':
                        values.append(symbol[2])
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
            
            elif args[count][1] in self.comparison_categories:
                temp = []
                while args[count][1] != 'concatenation operator (VISIBLE)' and args[count][1] != 'linebreak':
                    temp.append(args[count])
                    count += 1
                count -= 1
                values.append(self.implicit_typecast(self.comparison(temp), 'troof', 'yarn'))

            else: #raw value
                if args[count][1] == 'numbar':
                    values.append(self.implicit_typecast(args[count][0], 'numbar', 'yarn'))
                if args[count][1] == 'numbr':
                    values.append(self.implicit_typecast(args[count][0], 'numbr', 'yarn'))
                if args[count][1] == 'troof':
                    values.append(args[count][0])
                if args[count][1] == 'yarn':
                    values.append(args[count][0])
            count += 1
        
        string = ''
        # print(values)
        for value in values:
            # print(value)
            temp = value[1:-1]
            # print(temp)
            string = string + temp 
        string = "\"" + string + "\""
        self.toprint.append(string)
        print(string)
    #----------------

SAMPLE_CODE = [
    [['HAI', 'program start'], ['\n', 'linebreak']], [['WAZZUP', 'variable declaration area start'], ['\n', 'linebreak']], 
    [['BTW .', 'comment'], ['\n', 'linebreak']], 
    [['I HAS A', 'variable declaration'], ['x', 'identifier'], ['ITZ', 'variable initialization'], ['3', 'numbr'], ['\n', 'linebreak']], 
    [['I HAS A', 'variable declaration'], ['y', 'identifier'], ['ITZ', 'variable initialization'], ['4', 'numbr'], ['\n', 'linebreak']], 
    [['BUHBYE', 'variable declaration area end'], ['\n', 'linebreak']], 
    [['VISIBLE', 'output'], ['BOTH SAEM', 'compare equal'], ['x', 'identifier'], ['AN', 'noonecares'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['VISIBLE', 'output'], ['DIFFRINT', 'compare diff'], ['x', 'identifier'], ['AN', 'noonecares'], ['y', 'identifier'], ['\n', 'linebreak']],
    [['KTHXBYE', 'program end'], ['\n', 'linebreak']]
    ]

s = Semantic(SAMPLE_CODE)
s.read_code()

