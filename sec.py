from sys import argv

from first import tokens
from ply import yacc


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


def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    '''factor : INT
              | FLOAT'''
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


parser_errors = []

def p_error(p):
    if p is None:
        parser_errors.append("Syntax error at EOI")
        e = yacc.YaccSymbol()
        e.type = 'error'
        e.value = None
        parser.errok()
        return e
    elif p.type == 'error':
        parser.errok()
        return
    elif hasattr(p, 'value'):
        parser_errors.append("Syntax error at '%s' in line %s" % (p.value, p.lineno))
        e = yacc.YaccSymbol()
        e.type = 'error'
        e.value = p.value
        parser.errok()
        return e


parser = yacc.yacc()


def build_tree(code):
    p = parser.parse(code)
    return p


if __name__ == '__main__':
    assert len(argv) == 2
    filename = argv[1]
    inp = open(filename)
    characters = inp.read()
    inp.close()
    print build_tree(characters)

    print
    for error in parser_errors:
        print error