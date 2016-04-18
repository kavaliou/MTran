from sys import argv

import re
from ply import lex


# This is the list of token names.
tokens = (
    'VARIABLE',
    'BUILTIN',
    'DECLARATION',
    'KEYWORD',
    'OPERATOR',
    'PUNCTUATION',
    'RESERVED',
    'CONSTANT',
    'INT',
    'FLOAT',
    'BIN_NUMBER',
    'OCT_NUMBER',
    'HEX_NUMBER',
    'STRING',
    'LPAREN',
    'RPAREN'
)
# These are regular expression rules for simple tokens.
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_RESERVED = r'(abstract|boolean|byte|char|class|const|debugger|double|enum|export|' \
             r'extends|final|float|goto|implements|import|int|interface|long|native|' \
             r'package|private|protected|public|short|static|super|synchronized|throws|' \
             r'transient|volatile)\b'
t_CONSTANT = r'(true|false|null|NaN|Infinity|undefined)\b'
t_BIN_NUMBER = r'0b[01]+'
t_OCT_NUMBER = r'0o[0-7]+'
t_HEX_NUMBER = r'0x[0-9a-fA-F]+'
t_BUILTIN = r'(Array|Boolean|Date|Error|Function|Math|netscape|' \
             r'Number|Object|Packages|RegExp|String|Promise|Proxy|sun|decodeURI|' \
             r'decodeURIComponent|encodeURI|encodeURIComponent|' \
             r'Error|eval|isFinite|isNaN|isSafeInteger|parseFloat|parseInt|' \
             r'document|this|window)\b'
t_DECLARATION = r'(var|let|with|function)\b'
t_KEYWORD = r'(for|in|while|do|break|return|continue|switch|case|default|if|else|' \
             r'throw|try|catch|finally|new|delete|typeof|instanceof|void|yield|' \
             r'this|of)\b'
t_OPERATOR = r'\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|' \
             r'(<<|>>>?|=>|==?|!=?|[-<>+*%&|^/])=?'
# t_VARIABLE = r'[$a-zA-Z_][\w.$]*\s*(:|[+\-*/]?\=)?\b'
t_VARIABLE = r'[A-Za-z][A-Za-z0-9_]*'
t_PUNCTUATION = r'(\.\.\.|[{(\[;,]|[})\].])'



# Read in a float.  This rule has to be done before the int rule.
def t_FLOAT(t):
    r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?'
    t.value = float(t.value)
    return t


# Read in an int.
def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


# Read in a string, as in C.  The following backslash sequences have their
# usual special meaning: \", \\, \n, and \t.
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


# Ignore comments.
def t_comment(t):
    r'[//][^\n]*'
    pass


# Track line numbers.
def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

# These are the things that should be ignored.
t_ignore = ' \t'


# Handle errors.
def t_error(t):
    raise SyntaxError("syntax error on line %d near '%s'" %
                      (t.lineno, t.value))


lexer = lex.lex(reflags=re.DOTALL | re.UNICODE | re.MULTILINE)


if __name__ == '__main__':
    assert len(argv) == 2
    filename = argv[1]
    inp = open(filename)
    characters = inp.read()
    inp.close()
    lexer.input(characters)
    for tok in iter(lexer.token, None):
        print repr(tok.type), repr(tok.value)
