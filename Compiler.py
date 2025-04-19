import re

# Token types
KEYWORDS = ["if", "else", "void", "int", "while", "break", "return"]
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']
DOUBLE_SYMBOLS = ['==']
WHITESPACES = {' ', '\n', '\r', '\t', '\v', '\f'}

# Initialize symbol table with keywords
symbol_table = KEYWORDS.copy()
tokens_by_line = {}
lexical_errors = []

# Read input
with open("input.txt", "r") as f:
    input_lines = f.readlines()

line_number = 1
line_index = 0

def is_keyword(word):
    return word in KEYWORDS

def add_symbol_table(token):
    if token not in symbol_table:
        symbol_table.append(token)

def save_files():
    with open("token.txt", "w") as tok:
        for line in sorted(tokens_by_line.keys()):
            token_line = f"{line}.\t" + ' '.join([f"({t[0]}, {t[1]})" for t in tokens_by_line[line]])
            tok.write(token_line + "\n")

    with open("lexical_errors.txt", "w") as err:
        if lexical_errors:
            for line, lex in lexical_errors:
                err.write(f"{line}.\t({lex}, Invalid input)\n")
        else:
            err.write("There is no lexical error.\n")

    with open("symbol_table.txt", "w") as sym:
        for idx, symb in enumerate(symbol_table, 1):
            sym.write(f"{idx}.\t{symb}\n")

def get_next_token(line, index):
    ch = line[index]

    if ch in WHITESPACES:
        return ('WHITESPACE', ch), index + 1

    if ch == '/':
        if index + 1 < len(line) and line[index + 1] == '*':
            end_index = line.find('*/', index + 2)
            if end_index != -1:
                return ('COMMENT', line[index:end_index + 2]), end_index + 2
            else:
                lexical_errors.append((line_number, line[index:].strip()))
                return None, len(line)

    # Double-character symbol
    if line[index:index + 2] in DOUBLE_SYMBOLS:
        return ('SYMBOL', line[index:index + 2]), index + 2

    if ch in SYMBOLS:
        return ('SYMBOL', ch), index + 1

    if ch.isdigit():
        match = re.match(r'[0-9]+', line[index:])
        if match:
            value = match.group(0)
            return ('NUM', value), index + len(value)

    if ch.isalpha():
        match = re.match(r'[A-Za-z][A-Za-z0-9]*', line[index:])
        if match:
            value = match.group(0)
            if is_keyword(value):
                add_symbol_table(value)
                return ('KEYWORD', value), index + len(value)
            else:
                add_symbol_table(value)
                return ('ID', value), index + len(value)

    # Panic mode: skip until a known token
    start = index
    while index < len(line) and line[index] not in WHITESPACES and \
            not re.match(r'[A-Za-z0-9]', line[index]) and line[index:index + 2] not in DOUBLE_SYMBOLS and \
            line[index] not in SYMBOLS:
        index += 1

    if index == start:
        index += 1
    lexical_errors.append((line_number, line[start:index].strip()))
    return None, index

while line_index < len(input_lines):
    line = input_lines[line_index]
    index = 0
    tokens_this_line = []

    while index < len(line):
        token_result, new_index = get_next_token(line, index)
        if token_result and token_result[0] != 'WHITESPACE' and token_result[0] != 'COMMENT':
            tokens_this_line.append(token_result)
        index = new_index

    if tokens_this_line:
        tokens_by_line[line_number] = tokens_this_line

    line_number += 1
    line_index += 1

save_files()
