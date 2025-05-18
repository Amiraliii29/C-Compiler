# Parser + Scanner combined in one Python module

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

    def is_letter(self, ch): return ch.isalpha()
    def is_digit(self, ch): return ch.isdigit()
    def is_alnum(self, ch): return ch.isalnum()
    def is_whitespace(self, ch): return ch in ' \n\r\t\v\f'

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
                else:
                    self.index += 1
                    return ('SYMBOL', '=')

            # Single-character symbols
            if ch in self.SYMBOLS:
                self.index += 1
                return ('SYMBOL', ch)

            # Numbers
            if self.is_digit(ch):
                start = self.index
                while self.index < len(line) and self.is_digit(line[self.index]):
                    self.index += 1
                return ('NUM', line[start:self.index])

            # Identifiers and keywords
            if self.is_letter(ch):
                start = self.index
                while self.index < len(line) and self.is_alnum(line[self.index]):
                    self.index += 1
                word = line[start:self.index]
                if word in self.KEYWORDS:
                    return ('KEYWORD', word)
                else:
                    return ('ID', word)

            # Invalid input
            self.errors.append((self.line_number + 1, ch, 'Invalid input'))
            self.index += 1

        # End of input
        return ('$', '$')

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = self.scanner.get_next_token()
        self.errors = []
        self.output = []  # parse tree lines
        self.stack = []
        self.indent_level = 0

        # Example grammar rules and productions (You provide full)
        # format: non_terminal: [list of possible productions]
        # each production is list of grammar symbols (terminals or non-terminals)
        self.grammar = {
            'Program': [['DeclarationList']],
            'DeclarationList': [['Declaration', 'DeclarationList'], []],  # epsilon
            'Declaration': [['KEYWORD', 'ID', 'DeclarationPrime']],
            # Add all 47 rules here
        }

        # FIRST and FOLLOW sets placeholders (you add real sets)
        self.FIRST = {
            'Program': {'int', 'void'},
            'DeclarationList': {'int', 'void', ''},  # epsilon represented by empty string
            'Declaration': {'int', 'void'},
            'DeclarationPrime': {';', '(', '[', '{'},
            # ...
        }

        self.FOLLOW = {
            'Program': {'$'},
            'DeclarationList': {'$'},
            'Declaration': {'int', 'void', '$'},
            'DeclarationPrime': {'int', 'void', '$'},
            # ...
        }

    def write_node(self, node):
        self.output.append('\t' * self.indent_level + node)

    def advance(self):
        self.current_token = self.scanner.get_next_token()

    def panic_recovery(self, non_terminal):
        # Skip tokens until token in FOLLOW(non_terminal) or EOF ($)
        follow_set = self.FOLLOW.get(non_terminal, set())
        while self.current_token[1] not in follow_set and self.current_token[0] != '$':
            self.errors.append(f"#{self.scanner.line_number+1} : syntax error, unexpected token {self.current_token[1]} in {non_terminal}, skipping")
            self.advance()

    def parse(self):
        self.stack = ['Program']
        self.indent_level = 0
        self.write_node('Program')
        self.indent_level += 1

        while self.stack:
            top = self.stack.pop()
            if top in self.grammar:  # non-terminal
                # Decide which production to use based on FIRST sets and current token
                # Here we simplify and pick first production whose FIRST set contains current token
                # You need to replace this logic with your real FIRST set logic and table
                productions = self.grammar[top]

                prod_to_use = None
                for prod in productions:
                    # Compute FIRST(prod)
                    first_sym = prod[0] if prod else ''  # epsilon if empty production
                    if first_sym == '':
                        # epsilon production always possible
                        prod_to_use = prod
                        break
                    # If first_sym terminal or non-terminal, check if current token matches
                    # For simplicity, check if current token matches first_sym (terminal)
                    if first_sym in [self.current_token[1], self.current_token[0]]:
                        prod_to_use = prod
                        break
                    # Also check if current_token in FIRST(first_sym) if first_sym non-terminal
                    if first_sym in self.FIRST and self.current_token[1] in self.FIRST[first_sym]:
                        prod_to_use = prod
                        break
                if prod_to_use is None:
                    # Panic mode error recovery
                    self.errors.append(f"#{self.scanner.line_number+1} : syntax error, unexpected token {self.current_token[1]} when parsing {top}")
                    self.panic_recovery(top)
                    continue

                # Output non-terminal node
                self.write_node(top)
                self.indent_level += 1

                # Push production RHS to stack in reverse order
                for symbol in reversed(prod_to_use):
                    if symbol != '':
                        self.stack.append(symbol)

            else:
                # terminal symbol expected
                typ, val = self.current_token
                if top == val or top == typ:
                    self.write_node(f"({typ}, {val})")
                    self.advance()
                else:
                    # Terminal mismatch error
                    self.errors.append(f"#{self.scanner.line_number+1} : syntax error, missing {top}")
                    self.write_node(f"({top})")  # pretend it's there

        self.indent_level -= 1

def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    scanner = Scanner(lines)
    parser = Parser(scanner)
    parser.parse()

    with open("parse_tree.txt", "w") as f:
        for line in parser.output:
            f.write(line + "\n")

    with open("syntax_errors.txt", "w") as f:
        if not parser.errors and not scanner.errors:
            f.write("There is no syntax error.\n")
        else:
            for err in scanner.errors:
                f.write(f"Scanner error at line {err[0]}: {err[2]} ('{err[1]}')\n")
            for err in parser.errors:
                f.write(err + "\n")

if __name__ == "__main__":
    main()
