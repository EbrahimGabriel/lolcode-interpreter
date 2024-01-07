class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
    
    # Print in array form
    #def __str__(self):
    #    return f'[{self.value}, {self.children}]'
    
    #Print in tree form
    def __str__(self, level=0):
        ret = "\t" * level + f"[{repr(self.value)}]\n"
        for child in self.children:
            if isinstance(child, Node):
                ret += child.__str__(level + 1)
            else:
                ret += "\t" * (level + 1) + f"[{repr(child)}]\n"
        return ret
    
    def __repr__(self):
        return f'[{self.value}, {self.children}]'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        
    def parse(self):
        tree = self.parse_program()
        return tree
    
    def parse_program(self):
        root = Node('program')


        if self.tokens[self.index][0] != 'HAI':
           print('error')
        
        root.children.append(self.tokens[self.index][0])
        self.index += 1


        if self.tokens[self.index][0] != '\n':
           print('error')
        root.children.append(self.tokens[self.index][0])   
        self.index += 1

        # if self.tokens[self.index][0] != 'VARDECLARATION':
        #    print('error')
        # self.index += 1

        root.children.append(self.parse_statement())

        # if self.tokens[self.index][0] != 'LINEBREAK':
        #    print('error')
        # self.index += 1    

        if self.tokens[self.index][0] != 'KTHXBYE':
           print('error')
        root.children.append(self.tokens[self.index][0])
        self.index += 1

        return root
    
    def parse_statement(self):

        # parse expr
        # parse print
        # parse inputstatement
        # parse smooshstatement
        # ....

        tree = Node('statement')
        while self.tokens[self.index][0] != 'KTHXBYE':
            if self.tokens[self.index][1] == 'input':
                tree.children.append(self.parse_input_statement())
            elif self.tokens[self.index][1] == 'output':
                tree.children.append(self.parse_print())
            elif self.tokens[self.index + 1][0] == 'R':
                tree.children.append(self.parse_assignment())
            elif self.tokens[self.index][1] == 'arithmetic':
                tree.children.append(self.parse_arithoperation())
            elif self.tokens[self.index][1] == 'concatenation':
                tree.children.append(self.parse_smooshoperation())
            elif self.tokens[self.index][1] == 'boolean':
                tree.children.append(self.parse_booloperation())
            elif self.tokens[self.index][1] == 'typecast':
                tree.children.append(self.parse_typecaststatement())
        # tree.children.append(self.parse_expr())
        # tree.children.append(self.smooshstaement())
        return tree


    def parse_input_statement(self):
        tree = Node('inputstatement')
        if self.tokens[self.index][0] != 'GIMMEH':
            print('error')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1

        tree.children.append(self.tokens[self.index][0])
        self.index += 1

        return tree
    
    def parse_print(self):
        tree = Node('printstatement')
        if self.tokens[self.index][0] != 'VISIBLE':
            print('error')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1
        tree.children.append(self.parse_literal())
        return tree

    def parse_literal(self):
        tree = Node('literal')
        if self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error')
        return tree

    def parse_assignment(self):
        tree = Node('assignmentstatement')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1
        
        if self.tokens[self.index][0] != 'R':
            print('error')
        tree.children.append(self.tokens[self.index][0])
        self.index += 1

        tree.children.append(self.parse_literal())

        return tree

    def parse_arithoperation(self):
        tree = Node('arithoperation')

        if self.tokens[self.index][0] != 'SUM OF' and self.tokens[self.index][0] != 'DIFF OF' and self.tokens[self.index][0] != 'PRODUKT OF' and self.tokens[self.index][0] != 'QUOSHUNT OF' and self.tokens[self.index][0] != 'MOD OF' and self.tokens[self.index][0] != 'BIGGR OF' and self.tokens[self.index][0] != 'SMALLR OF':
            print('error')

        while self.tokens[self.index][0] == 'SUM OF' or self.tokens[self.index][0] == 'DIFF OF' or self.tokens[self.index][0] == 'PRODUKT OF' or self.tokens[self.index][0] == 'QUOSHUNT OF' or self.tokens[self.index][0] == 'MOD OF' or self.tokens[self.index][0] == 'BIGGR OF' or self.tokens[self.index][0] == 'SMALLR OF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

        while (self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof') and self.tokens[self.index + 1][0] == 'AN':
            tree.children.append(self.parse_literal())
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        
        while self.tokens[self.index][1] == 'identifier' and self.tokens[self.index + 1][0] == 'AN':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

        if self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
            tree.children.append(self.parse_literal())
        elif self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error')
        
        return tree
    
    def parse_smooshoperation(self):
        tree = Node('concatoperation')
        if self.tokens[self.index][0] == 'SMOOSH':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        else:
            print('error')
        
        if self.tokens[self.index][1] != 'identifier' or self.tokens[self.index + 1][0] != 'AN':
            print('error')

        while self.tokens[self.index][1] == 'identifier' and self.tokens[self.index + 1][0] == 'AN':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
        
        if self.tokens[self.index - 1][0] == 'AN' and self.tokens[self.index][1] == 'identifier':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1

        return tree
    
    def parse_booloperation(self):
        tree = Node('booloperation')
        if self.tokens[self.index][0] == 'BOTH OF' or self.tokens[self.index][0] == 'EITHER OF' or self.tokens[self.index][0] == 'WON OF':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error')
            
            if self.tokens[self.index][0] == 'AN':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            else:
                print('error')
            
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error')
        else:
            print('error')

        if self.tokens[self.index][0] == 'NOT':
            tree.children.append(self.tokens[self.index][0])
            self.index += 1
            if self.tokens[self.index][1] == 'identifier':
                tree.children.append(self.tokens[self.index][0])
                self.index += 1
            elif self.tokens[self.index][1] == 'numbr' or self.tokens[self.index][1] == 'yarn' or self.tokens[self.index][1] == 'numbar' or self.tokens[self.index][1] == 'troof':
                tree.children.append(self.parse_literal())
            else:
                print('error')
        else:
            print('error')

        return tree

    def parse_not(self)
        

lexemes = [['HAI', 'program start'], ['\n', 'linebreak'], ['GIMMEH', 'input'], ['x', 'identifier'], ['VISIBLE', 'output'], ['7', 'numbr'], 
            ['y', 'identifier'], ['R', 'assignment'], ['2', 'numbr'], ['SUM OF', 'arithmetic'], ['QUOSHUNT OF', 'arithmetic'], ['4', 'numbr'], ['AN', 'operand separator'], ['6', 'numbr'], 
            ['GIMMEH', 'input'], ['x', 'identifier'], ['SUM OF', 'arithmetic'], ['QUOSHUNT OF', 'arithmetic'], 
            ['PRODUKT OF', 'arithmetic'], ['3', 'numbr'], ['AN', 'operand separator'], ['4', 'numbr'], ['AN', 'operand separator'], ['2', 'numbr'], ['AN', 'operand separator'], ['1', 'numbr'],
            ['SMOOSH', 'concatenation'], ['a', 'identifier'], ['AN', 'operand separator'], ['b', 'identifier'],
            ['AN', 'operand separator'], ['c', 'identifier'], ['EITHER OF', 'boolean'], ['x', 'identifier'], ['AN', 'operand separator'], ['3', 'numbr'],
            ['KTHXBYE', 'program end']]

p = Parser(lexemes)
t = p.parse()
print(t)