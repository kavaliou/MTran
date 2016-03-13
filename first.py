import re

RESERVED = 'RESERVED'
NUMBER = 'NUMBER'
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
]

literals = [
    (r'#.*', None),
    (r'\"([^\']+)?\"?', STRING),
    (r'\'([^\"]+)?\'?', STRING),
    ('[0-9]+$', NUMBER),
    ('[A-Za-z][A-Za-z0-9_]*$', ID),
]


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


def main():
    filename = "input.txt"
    inp = open(filename)
    characters = inp.read()
    inp.close()

    position = 0
    buff = ''
    old_reserved, new_reserved, old_literals, new_literals = (None, ) * 4
    result = []
    while position < len(characters):
        buff += characters[position]
        if characters[position] == '\n':
            new_reserved = new_literals = None
            position += 1
        else:
            new_reserved = filter_on_text_search(buff, token_expressions)
            new_literals = filter_matches(buff, literals)

        if not new_reserved and not new_literals:
            if old_reserved and old_reserved[0][0] == buff[:-1]:
                if old_reserved[0][1]:
                    result.append(old_reserved[0])
            else:
                if old_literals and old_literals[0][1]:
                    entry = [i for i in old_literals[0]]
                    entry[0] = buff[:-1]
                    result.append(entry)
            buff = ''
            old_reserved = None
            old_literals = None
        else:
            old_reserved = new_reserved
            old_literals = new_literals
            position += 1
    return result

if __name__ == '__main__':
    print main()
