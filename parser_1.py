class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
    def __str__(self):
        return f'[{self.value}, {self.children}]'
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

        tree = Node('statment')
        tree.children.append(self.parse_input_statement())
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




lexemes = [['HAI', 'program start'], ['\n', 'linebreak'], ['GIMMEH', 'input'], ['x', 'identifier'], ['KTHXBYE', 'program end']]
p = Parser(lexemes)
t = p.parse()
print(t)