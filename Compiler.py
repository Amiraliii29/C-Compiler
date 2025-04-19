KEYWORDS = ['if', 'else', 'void', 'int', 'while', 'break', 'return']
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']

symbol_table = []
symbol_table.extend(KEYWORDS)
tokens = []
lexical_errors = []

def add_to_symbol_table(token):
    if token not in symbol_table:
        symbol_table.append(token)

def is_letter(ch):
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'

def is_digit(ch):
    return '0' <= ch <= '9'

def is_alnum(ch):
    return is_letter(ch) or is_digit(ch)

def is_whitespace(ch):
    return ch in ' \n\r\t\v\f'

inside_comment = False
comment_start_line = None

def get_next_token(line, index, line_number):
    global inside_comment, comment_start_line

    if inside_comment:
        while index < len(line):
            if line[index] == '*' and index + 1 < len(line) and line[index + 1] == '/':
                inside_comment = False
                return None, index + 2
            index += 1
        return None, index  # continue comment in next line

    if index >= len(line):
        return None, index

    ch = line[index]

    if is_whitespace(ch):
        return None, index + 1

    # COMMENT START
    if not inside_comment and ch == '/' and index + 1 < len(line) and line[index + 1] == '*':
        inside_comment = True
        comment_start_line = line_number
        return None, index + 2

    # UNMATCHED COMMENT END
    if ch == '*' and index + 1 < len(line) and line[index + 1] == '/':
        lexical_errors.append((line_number, '*/', 'Unmatched comment'))
        return None, index + 2

    # SYMBOLS including ==
    if ch == '=':
        if index + 1 < len(line) and line[index + 1] == '=':
            return ('SYMBOL', '=='), index + 2
        return ('SYMBOL', '='), index + 1

    if ch in SYMBOLS:
        if index + 1 < len(line):
            next_ch = line[index + 1]
            if not is_whitespace(next_ch) and next_ch not in SYMBOLS and not is_letter(next_ch) and not is_digit(next_ch) and next_ch != '=':
                lexical_errors.append((line_number, ch + next_ch, 'Invalid input'))
                return None, index + 2
        return ('SYMBOL', ch), index + 1

    if is_digit(ch):
        start = index
        while index < len(line) and is_digit(line[index]):
            index += 1
        if index < len(line) and is_letter(line[index]):
            index += 1
            lexical_errors.append((line_number, line[start:index], 'Invalid number'))
            return None, index
        return ('NUM', line[start:index]), index

    if is_letter(ch):
        start = index
        while index < len(line) and is_alnum(line[index]):
            index += 1
        if index < len(line) and not is_whitespace(line[index]) and line[index] not in SYMBOLS + ['=']:
            invalid_start = start
            while index < len(line) and not is_whitespace(line[index]) and line[index] not in SYMBOLS + ['=']:
                index += 1
            lexical_errors.append((line_number, line[invalid_start:index], 'Invalid input'))
            return None, index
        word = line[start:index]
        if word in KEYWORDS:
            return ('KEYWORD', word), index
        add_to_symbol_table(word)
        return ('ID', word), index

    lexical_errors.append((line_number, ch, 'Invalid input'))
    return None, index + 1

def main():
    global tokens, lexical_errors, inside_comment, comment_start_line
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    for line_number, line in enumerate(lines, start=1):
        i = 0
        line_tokens = []
        while i < len(line):
            result, new_index = get_next_token(line, i, line_number)
            if result:
                line_tokens.append(result)
                if result[0] == 'KEYWORD':
                    add_to_symbol_table(result[1])
            i = new_index
        if line_tokens:
            tokens.append(f"{line_number}.\t" + ' '.join(f"({t[0]}, {t[1]})" for t in line_tokens))
    # Handle unclosed comment at EOF
    if inside_comment:
        comment_content = lines[comment_start_line - 1].split('/*', 1)[1]
        short_preview = comment_content[:5] + '...'
        lexical_errors.append((comment_start_line, f'/*{short_preview}', 'Unclosed comment'))


    with open('token.txt', 'w') as f:
        for line in tokens:
            f.write(line + '\n')

    with open('lexical_errors.txt', 'w') as f:
        if not lexical_errors:
            f.write("There is no lexical error.\n")
        else:
            current_line = -1
            buffer = []
            for ln, val, msg in lexical_errors:
                if ln != current_line:
                    if buffer:
                        f.write(f"{current_line}.\t" + ' '.join(buffer) + '\n')
                    buffer = [f"({val}, {msg})"]
                    current_line = ln
                else:
                    buffer.append(f"({val}, {msg})")
            if buffer:
                f.write(f"{current_line}.\t" + ' '.join(buffer) + '\n')

    with open('symbol_table.txt', 'w') as f:
        for i, sym in enumerate(symbol_table):
            f.write(f"{i+1}.\t{sym}\n")


if __name__ == "__main__":
    main()
