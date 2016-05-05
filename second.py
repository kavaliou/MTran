from __future__ import absolute_import

from sys import argv

import re
from ply.lex import LexToken

from first import tokens, lexer
from ply import yacc

from custom_exceptions import *


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


variables = []


def token_in_stack(name, stack):
    for item in stack:
        if isinstance(item, LexToken) and item.value == name:
            return True
    return False


def p_function(p):
    '''function : func_header func_body
    '''
    p[0] = Node('function', p[1:])


def p_func_header(p):
    '''func_header : FUNCTION VARIABLE LPAREN args RPAREN'''
    p[0] = Node('func_declaration', [p[2], p[4]])


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
    '''block : LFIGURPAREN body RFIGURPAREN'''
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
    '''multiline : while_statement'''
    p[0] = p[1]


def p_line(p):
    '''line : assign
            | func
            | RETURN expr
            | RETURN func'''
    if len(p) == 3:
        p[0] = Node('return', [p[2]])
    else:
        p[0] = p[1]


def p_while_statement(p):
    '''while_statement : WHILE LPAREN condition RPAREN block
                       | WHILE LPAREN condition RPAREN line semicolons'''
    p[0] = Node('while', [p[3], p[5]])


def p_condition(p):
    '''condition : expr cond_sign expr'''
    p[0] = Node('condition', [p[1], p[2], p[3]])


def p_cond_sign(p):
    '''cond_sign : NOTEQUAL
                 | EQUAL'''
    p[0] = p[1]


def p_assign(p):
    '''assign : variable EQUAL expr
              | VAR variable EQUAL expr
              | VAR variable EQUAL function'''
    if len(p) == 5:
        value = p[2]
        if value in variables:
            raise VariableOverridingError(value, lexer.lineno)
        else:
            variables.append(value)
        p[0] = Node('assign', [p[2], p[4]])
    else:
        value = p[1]
        if value not in variables:
            raise NotAssignedVariableError(value, lexer.lineno)
        p[0] = Node('assign', [p[1], p[3]])


def p_func(p):
    '''func : VARIABLE LPAREN args RPAREN'''
    p[0] = Node('func_call', [p[1], p[3]])


def p_expr(p):
    '''expr : fact
            | expr OPERATOR fact'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_fact(p):
    '''fact : term
            | fact OPERATOR term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_term(p):
    '''term : arg
            | LPAREN expr RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_arg(p):
    '''arg : STRING
           | variable
           | INT
           | FLOAT
           | method
           | func'''
    value = p[1]
    if isinstance(value, str):
        if token_in_stack('function', p.stack):
            variables.append(value)
        elif value not in variables:
            raise NotAssignedVariableError(value, lexer.lineno)
    p[0] = Node('arg', [p[1]])


def p_method(p):
    '''method : variable_or_arg DOT func'''
    p[0] = Node('method', [p[1], p[3]])


def p_variable_or_arg(p):
    '''variable_or_arg : variable
                       | arg'''
    p[0] = p[1]


def p_variable(p):
    """variable : VARIABLE"""
    p[0] = p[1]

parser_errors = []

def p_error(p):
    print 'Unexpected token in line %d: %s' % (p.lineno, p)

# def p_error(p):
#     if p is None:
#         parser_errors.append("Syntax error at EOI")
#         e = yacc.YaccSymbol()
#         e.type = 'error'
#         e.value = None
#         parser.errok()
#         return e
#     elif p.type == 'error':
#         parser.errok()
#         return
#     elif hasattr(p, 'value'):
#         parser_errors.append("Syntax error at '%s' in line %s" % (p.value, p.lineno))
#         e = yacc.YaccSymbol()
#         e.type = 'error'
#         e.value = p.value
#         parser.errok()
#         return e
#

parser = yacc.yacc()


def build_tree(code):
    p = parser.parse(code)
    return p

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

__variables = {}

def parse_tree(tree):
    try:
        tree_type = tree.type
        parts = tree.parts
    except AttributeError:
        return tree
    if tree_type == 'assign':
        __variables[parts[0]] = parse_tree(parts[1])
        return
    if tree_type == 'arg':
        arg = parts[0]
        if isinstance(arg, int):
            return arg
        elif arg in __variables:
            return __variables[arg]
        else:
            return 'method'
    if tree_type in operations:
        first = parse_tree(parts[0])
        second = parse_tree(parts[1])
        if tree_type == '/' and second == 0:
            raise CustomZeroDivisionError(-1)
        return operations[tree_type](first, second)
    for part in parts:
        parse_tree(part)

if __name__ == '__main__':
    assert len(argv) == 2
    filename = argv[1]
    inp = open(filename)
    characters = inp.read()
    inp.close()
    try:
        tree = build_tree(characters)
        parse_tree(tree)
    except CustomException as e:
        print e.message
        tree = None
    print tree

    print
    for error in parser_errors:
        print error