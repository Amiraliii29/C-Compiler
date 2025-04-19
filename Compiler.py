import re

KEYWORDS = ["if", "else", "void", "int", "while", "break", "return"]
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']
DOUBLE_SYMBOLS = ['==']
WHITESPACES = {' ', '\n', '\r', '\t', '\v', '\f'}

symbol_table = KEYWORDS.copy()
tokens_by_line = {}
lexical_errors = []

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
            for entry in lexical_errors:
                if isinstance(entry, tuple):
                    err.write(f"{entry[0]}.\t({entry[1]}, {entry[2]})\n")
                else:
                    # Unclosed comment
                    truncated = entry[:7] + "..." if len(entry) > 7 else entry
                    err.write(f"{line_number}.\t({truncated}, Unclosed comment)\n")
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
            end_line = line_number
            end_index = line.find('*/', index + 2)
            if end_index != -1:
                return ('COMMENT', line[index:end_index + 2]), end_index + 2
            else:
                # Unclosed comment
                lexical_errors.append(line[index:].strip())
                return None, len(line)
        elif index + 1 < len(line) and line[index + 1] == '/':
            return ('COMMENT', line[index:]), len(line)
        elif index + 1 < len(line) and line[index + 1] != '*':
            return ('SYMBOL', '/'), index + 1
        elif index + 1 == len(line):
            return ('SYMBOL', '/'), index + 1
        else:
            lexical_errors.append((line_number, '*/', 'Unmatched comment'))
            return None, index + 2

    # Double-character symbol
    if line[index:index + 2] in DOUBLE_SYMBOLS:
        return ('SYMBOL', line[index:index + 2]), index + 2

    if ch in SYMBOLS:
        return ('SYMBOL', ch), index + 1

    if ch.isdigit():
        match = re.match(r'[0-9]+', line[index:])
        if match:
            value = match.group(0)
            next_char = index + len(value)
            if next_char < len(line) and line[next_char].isalpha():
                # Invalid number like 123d
                match_full = re.match(r'[0-9]+[A-Za-z0-9]*', line[index:])
                invalid = match_full.group(0)
                lexical_errors.append((line_number, invalid, 'Invalid number'))
                return None, index + len(invalid)
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

    # Unmatched comment end
    if ch == '*' and index + 1 < len(line) and line[index + 1] == '/':
        lexical_errors.append((line_number, '*/', 'Unmatched comment'))
        return None, index + 2

    # Panic mode for invalid single characters
    lexical_errors.append((line_number, ch, 'Invalid input'))
    return None, index + 1

while line_index < len(input_lines):
    line = input_lines[line_index]
    index = 0
    tokens_this_line = []

    while index < len(line):
        token_result, new_index = get_next_token(line, index)
        if token_result and token_result[0] not in ['WHITESPACE', 'COMMENT']:
            tokens_this_line.append(token_result)
        index = new_index

    if tokens_this_line:
        tokens_by_line[line_number] = tokens_this_line

    line_number += 1
    line_index += 1

save_files()
