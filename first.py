from sys import argv

import re
from ply import lex


# This is the list of token names.
from ply.lex import TOKEN

tokens = (
    'VARIABLE', 'INT', 'FLOAT', 'BIN_NUMBER', 'OCT_NUMBER',
    'HEX_NUMBER', 'STRING', 'LPAREN', 'RPAREN',
    'OPERATOR', 'SEMICOLON', 'DOT', 'COMMA',
    'VAR', 'FUNCTION', 'RETURN', 'WHILE',
    'LFIGURPAREN', 'RFIGURPAREN',
)

reserved = {
    'return': 'RETURN',
    'function': 'FUNCTION',
    'var': 'VAR',
    'while': 'WHILE'
}

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LFIGURPAREN = r'{'
t_RFIGURPAREN = r'}'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_COMMA = r','


@TOKEN(r'[A-Za-z][A-Za-z0-9_]*')
def t_VARIABLE(t):
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


t_BIN_NUMBER = r'0b[01]+'
t_OCT_NUMBER = r'0o[0-7]+'
t_HEX_NUMBER = r'0x[0-9a-fA-F]+'
t_OPERATOR = r'\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|' \
             r'(<<|>>>?|=>|==?|!=?|[-<>+*%&|^/])=?'


def t_FLOAT(t):
    r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'("(\\\\|\\"|[^"])*")|(\'(\\\\|\\\'|[^\'])*\')'
    escaped = 0
    str = t.value[1:-1]
    new_str = ""
    for i in range(0, len(str)):
        c = str[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = 0
        else:
            if c == "\\":
                escaped = 1
            else:
                new_str += c
    t.value = new_str
    return t


def t_comment(t):
    r'[//][^\n]*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'


def t_error(t):
    print "Illegal character '%s' at line %s" % (t.value[0], t.lineno)
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.DOTALL | re.UNICODE | re.MULTILINE)


if __name__ == '__main__':
    assert len(argv) == 2
    filename = argv[1]
    inp = open(filename)
    characters = inp.read()
    inp.close()
    lexer.input(characters)
    for tok in iter(lexer.token, None):
        print '{0:20}   {1}'.format(repr(tok.type), repr(tok.value))
