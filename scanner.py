class Scanner:
    KEYWORDS = ['if', 'else', 'void', 'int', 'while', 'break', 'return']
    SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']

    def __init__(self, lines):
        self.lines = lines
        self.line_number = 0
        self.index = 0
        self.inside_comment = False
        self.comment_start_line = None
        self.current_line = ''
        self.errors = []
        # self.symbol_table = []
        # self.symbol_table.extend(self.KEYWORDS)

    def is_letter(self, ch): return ch.isalpha()
    def is_digit(self, ch): return ch.isdigit()
    def is_alnum(self, ch): return ch.isalnum()
    def is_whitespace(self, ch): return ch in ' \n\r\t\v\f'

    # def add_to_symbol_table(self, token):
    #     if token not in self.symbol_table:
    #         self.symbol_table.append(token)

    def get_next_token(self):
        while self.line_number < len(self.lines):
            line = self.lines[self.line_number]
            if self.index >= len(line):
                self.line_number += 1
                self.index = 0
                continue

            ch = line[self.index]

            # Skip whitespace
            if self.is_whitespace(ch):
                self.index += 1
                continue

            # Comment start
            if ch == '/' and self.index + 1 < len(line) and line[self.index + 1] == '*':
                self.inside_comment = True
                self.comment_start_line = self.line_number + 1
                self.index += 2
                while self.line_number < len(self.lines):
                    line = self.lines[self.line_number]
                    while self.index < len(line):
                        if line[self.index] == '*' and self.index + 1 < len(line) and line[self.index + 1] == '/':
                            self.inside_comment = False
                            self.index += 2
                            break
                        self.index += 1
                    if not self.inside_comment:
                        break
                    self.line_number += 1
                    self.index = 0
                continue

            # Unmatched comment end
            if ch == '*' and self.index + 1 < len(line) and line[self.index + 1] == '/':
                self.errors.append((self.line_number + 1, '*/', 'Unmatched comment'))
                self.index += 2
                continue

            # == or =
            if ch == '=':
                if self.index + 1 < len(line) and line[self.index + 1] == '=':
                    self.index += 2
                    return ('SYMBOL', '==')
                elif self.index + 1 < len(line) and (not self.is_alnum(line[self.index + 1]) and not self.is_whitespace(line[self.index + 1])):
                    self.errors.append((self.line_number, ch + line[self.index + 1], 'Invalid input'))
                    self.index += 2
                    continue
                else:
                    self.index += 1
                    return ('SYMBOL', '=')

            # Single-character symbols
            if ch in self.SYMBOLS:
                if self.index + 1 < len(line):
                    next_ch = line[self.index + 1]
                    if ch == "*" or ch == "/":
                        if not self.is_whitespace(next_ch) and next_ch not in self.SYMBOLS and not self.is_letter(next_ch) and not self.is_digit(next_ch) and next_ch != '=':
                            self.errors.append((self.line_number, ch + next_ch, 'Invalid input'))
                            return None, self.index + 2
                self.index += 1        
                return ('SYMBOL', ch)
            # Numbers
            if self.is_digit(ch):
                start = self.index
                while self.index < len(line) and self.is_digit(line[self.index]):
                    self.index += 1
                if self.index < len(line) and (self.is_letter(line[self.index]) or (not self.is_whitespace(line[self.index]) and line[self.index] not in self.SYMBOLS + ["="] )):
                    self.index += 1
                    self.errors.append((self.line_number, line[start:self.index], 'Invalid number'))
                    continue
                return ('NUM', line[start:self.index])

            # Identifiers and keywords
            if self.is_letter(ch):
                start = self.index
                while self.index < len(line) and self.is_alnum(line[self.index]):
                    self.index += 1
                if self.index < len(line) and not self.is_whitespace(line[self.index]) and line[self.index] not in self.SYMBOLS + ['=']:
                    invalid_start = start
                    self.index += 1
                    self.errors.append((self.line_number, line[invalid_start:self.index], 'Invalid input'))
                    continue
                word = line[start:self.index]
                if word in self.KEYWORDS:
                    return ('KEYWORD', word)
                # self.add_to_symbol_table(word)
                return ('ID', word)

            # Invalid input
            self.errors.append((self.line_number + 1, ch, 'Invalid input'))
            self.index += 1

        # End of input
        return ('$', '$')
    