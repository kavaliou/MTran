from sys import argv

from ply import yacc

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


def p_function(p):
    '''function : func_header func_body
    '''
    p[0] = Node('function', p[1:])

def p_func_header(p):
    '''func_header : FUNCDECL VAR LPAR args RPAR'''
    p[0] = Node('func_declaration',[p[2], p[4]])

def p_args(p):
    '''args :
            | expr
            | args COMMA expr'''
    if len(p) <= 2:
        p[0] = Node('args', p[1:] if p[1:] else ['EMPTY'])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_func_body(p):
    '''func_body : block'''
    p[0] = p[1]

def p_block(p):
    '''block : LCURL body RCURL'''
    p[0] = Node('block', [p[2]])

def p_body(p):
    '''body :
            | body line semicolons
            | body multiline'''
    if len(p) > 1:
        if p[1] is None:
            p[1] = Node('body', [])
        p[0] = p[1].add_parts([p[2]])
    else:
        p[0] = Node('body', [])

def p_semicolons(p):
    '''semicolons : SEMICOLON
                  | semicolons SEMICOLON'''

def p_multiline(p):
    '''multiline : if_statement
                 | while_statement'''
    p[0] = p[1]

def p_line(p):
    '''line : assign
            | func'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAR condition RPAR block
                    | IF LPAR condition RPAR block ELSE block'''
    if len(p) == 4:
        p[0] = p[1].add_parts(Node('else', [p[3]]))
    else:
        p[0] = Node('if', [p[3], p[5]])

def p_while_statement(p):
    '''while_statement : WHILE LPAR condition RPAR block'''
    p[0] = Node('while', [p[3], p[5]])

def p_condition(p):
    '''condition : expr cond_sign expr'''
    p[0] = Node('condition', [p[1], p[2], p[3]])

def p_cond_sign(p):
    '''cond_sign : DEQUAL
                 | GT
                 | LT
                 | GE
                 | LE
                 | NOTEQUAL'''
    p[0] = p[1]

def p_assign(p):
    '''assign : var EQUAL expr
              | VARWORD var EQUAL expr'''
    if len(p) == 5:
        p[0] = Node('assign', [p[2], p[4]])
    else:
        p[0] = Node('assign', [p[1], p[3]])

def p_func(p):
    '''func : VAR LPAR args RPAR'''
    p[0] = Node('func_call', [p[1], p[3]])

def p_expr(p):
    '''expr : fact
            | expr PLUSMINUS fact'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_fact(p):
    '''fact : term
            | fact DIVMUL term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_term(p):
    '''term : arg
            | LPAR expr RPAR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_arg(p):
    '''arg : STRING
           | var
           | NUMBER
           | func'''
    p[0] = Node('arg', [p[1]])


def p_var(p):
    '''var : VAR'''
    p[0] = p[1]


def p_error(p):
    print 'Unexpected token in line %d: %s' % (p.lineno, p)


parser = yacc.yacc()

def build_tree(code):
    return parser.parse(code)


if __name__ == '__main__':
    assert len(argv) == 2
    filename = argv[1]
    inp = open(filename)
    characters = inp.read()
    inp.close()
