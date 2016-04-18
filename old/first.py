from sys import argv
import re

RESERVED = 'RESERVED'
NUMBER = 'NUMBER'
FLOAT = 'FLOAT'
EXPONENTA = 'EXPONENTA'
STRING = 'STRING'
ID = 'ID'

token_expressions = [
    (' ', None),
    ('\n', None),
    ('\t', None),
    ('=', RESERVED),
    (',', RESERVED),
    ('(', RESERVED),
    (')', RESERVED),
    (';', RESERVED),
    ('+', RESERVED),
    ('-', RESERVED),
    ('*', RESERVED),
    ('/', RESERVED),
    ('%', RESERVED),
    ('<', RESERVED),
    ('<=', RESERVED),
    ('>', RESERVED),
    ('>=', RESERVED),
    ('!=', RESERVED),
    ('and', RESERVED),
    ('or', RESERVED),
    ('not', RESERVED),
    ('if', RESERVED),
    ('else', RESERVED),
    ('print', RESERVED),
    ('while', RESERVED),
    ('do', RESERVED),
    ('for', RESERVED),
    ('in', RESERVED),
    ('end', RESERVED),
    (':', RESERVED),
    ('[', RESERVED),
    (']', RESERVED),
    ('{', RESERVED),
    ('}', RESERVED),

    ('var', RESERVED),
]

pol = [
    (r'//.*', None),
    ('[A-Za-z][A-Za-z0-9_]*$', ID),
]

literals = [
    (r'\"([^\']+)?\"$', STRING),
    (r'\'([^\"]+)?\'$', STRING),
    ('[-+]?[0-9]+$', NUMBER),
    ('[-+]?[0-9]*\.([0-9]+)?$', FLOAT),
    ('[-+]?[0-9]*(\.[0-9]+)?[eE]([+-]?[0-9]+)?$', EXPONENTA),
]

separators = (';', '\n')

for_IDs = [NUMBER, FLOAT, EXPONENTA, STRING, ID]


def filter_on_text_search(text, mass):
    def l(expression):
        regexp = re.compile(r'%s' % escape(text))
        match = regexp.match(expression[0])
        if match:
            return True
    return filter(l, mass)


def filter_matches(text, mass):
    def l(expression):
        regexp = re.compile(expression[0])
        match = regexp.match(text)
        if match:
            return True
    return filter(l, mass)


def escape(text):
    result_text = ''
    for i in text:
        if re.search(r'[-[\]{}()*+?.,\\^$|#\s]', i):
            result_text += '\\%s' % i
        else:
            result_text += i
    return result_text


def work(chars):
    def check_literals(buff, position):
        full_text = filter_matches(buff, literals)
        if full_text:
            new_full_text = full_text
            while full_text:
                new_full_text = full_text
                position += 1
                buff += chars[position] if chars[position] != '\n' else ' '
                full_text = filter_matches(buff, literals)
            position -= 1
            entry = [i for i in new_full_text[0]]
            entry[0] = buff[:-1]
            result.append(entry)
            buff = ''
        return buff, position

    position = 0
    buff = ''
    old_reserved, new_reserved, old_pols, new_pols = (None, ) * 4
    result, ID_result = [], []
    while position < len(chars):
        buff += chars[position]
        if chars[position] in separators:
            new_reserved = new_pols = None
            position += 1
        else:
            new_reserved = filter_on_text_search(buff, token_expressions)
            new_pols = filter_matches(buff, pol)

        if not new_reserved and not new_pols:
            if not old_reserved and not old_pols and not any([x in buff for x in separators]):
                buff, position = check_literals(buff, position)
                position += 1
            else:
                if old_reserved and old_reserved[0][0] == buff[:-1]:
                    if old_reserved[0][1]:
                        result.append(old_reserved[0])
                else:
                    if old_pols and old_pols[0][1]:
                        entry = [i for i in old_pols[0]]
                        entry[0] = buff[:-1]
                        result.append(entry)
                buff = ''
                old_reserved = None
                old_pols = None
        else:
            old_reserved = new_reserved
            old_pols = new_pols
            position += 1
    return result


if __name__ == '__main__':
    assert len(argv) == 2
    filename = argv[1]
    inp = open(filename)
    characters = inp.read()
    inp.close()
    result = work(characters)
    for i in result:
        print i[0], i[1]
