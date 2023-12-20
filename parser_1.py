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

        tree = Node('statment')
        tree.children.append(self.parse_input_statement())
        tree.children.append(self.parse_print())
        tree.children.append(self.parse_assignment())
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



lexemes = [['HAI', 'program start'], ['\n', 'linebreak'], ['GIMMEH', 'input'], ['x', 'identifier'], ['VISIBLE', 'output'], ['7', 'numbr'], ['y', 'identifier'], ['R', 'assignment'], ['2', 'numbr'], ['KTHXBYE', 'program end']]
p = Parser(lexemes)
t = p.parse()
print(t)