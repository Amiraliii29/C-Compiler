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
        print (self.current_token)
        self.errors = []
        self.output = []
        self.path_stack = []


    def advance(self):
        self.current_token = self.scanner.get_next_token()


    def write_node(self, depth, node, last):
        line = ""
        for i in range(depth - 1):
            line += "│   "
        if depth > 0:
            line += "└── " if last else "├── "
        line += node
        self.output.append(line)

    def match(self, expected_value, depth, last=True):
        if self.current_token[1] == expected_value:
            self.write_node(depth, f"({self.current_token[0]}, {self.current_token[1]})", last)
            self.advance()
        elif expected_value == 'ID' and self.current_token[0] == expected_value:
            self.write_node(depth, f"({self.current_token[0]}, {self.current_token[1]})", last)
            self.advance()
        elif expected_value == 'NUM' and self.current_token[0] == expected_value:
            self.write_node(depth, f"({self.current_token[0]}, {self.current_token[1]})", last)
            self.advance()
        else:
            self.syntax_error(depth, f"Expected '{expected_value}'", last)

    def syntax_error(self, depth, message, last=True):
        self.errors.append(f"#{self.scanner.line_number + 1} : syntax error, {message}")
        self.write_node(depth, "(error)", last)

    def Program(self, depth, last=True):
        self.write_node(depth, 'Program', False)
        self.DeclarationList(depth + 1, False)

    def DeclarationList(self, depth, last=True):
        self.write_node(depth, 'DeclarationList', last)
        if self.current_token[1] in ['int', 'void']:
            self.Declaration(depth + 1, last=False)
            self.DeclarationList(depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def Declaration(self, depth, last=True):
        self.write_node(depth, 'Declaration', last)
        self.DeclarationInitial(depth + 1, last=False)
        self.DeclarationPrime(depth + 1, last=True)

    def DeclarationInitial(self, depth, last=True):
        self.write_node(depth, 'DeclarationInitial', last)
        self.TypeSpecifier(depth + 1, last=False)
        self.match('ID', depth + 1, last=True)

    def DeclarationPrime(self, depth, last=True):
        self.write_node(depth, 'DeclarationPrime', last)
        if self.current_token[1] == '(':
            self.FunDeclarationPrime(depth + 1, last=True)
        elif self.current_token[1] in [';', '[']:
            self.VarDeclarationPrime(depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Expected ( or ; or [', last=True)

    def VarDeclarationPrime(self, depth, last=True):
        self.write_node(depth, 'VarDeclarationPrime', last)
        if self.current_token[1] == ';':
            self.match(';', depth + 1, last=True)
        elif self.current_token[1] == '[':
            self.match('[', depth + 1, last=False)
            self.match('NUM', depth + 1, last=False)
            self.match(']', depth + 1, last=False)
            self.match(';', depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Expected ; or [', last=True)

    def FunDeclarationPrime(self, depth, last=True):
        self.write_node(depth, 'FunDeclarationPrime', last)
        self.match('(', depth + 1, last=False)
        self.Params(depth + 1, last=False)
        self.match(')', depth + 1, last=False)
        self.CompoundStmt(depth + 1, last=True)

    def TypeSpecifier(self, depth, last=True):
        self.write_node(depth, 'TypeSpecifier', last)
        if self.current_token[1] in ['int', 'void']:
            self.match(self.current_token[1], depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Expected int or void', last=True)

    def Params(self, depth, last=True):
        self.write_node(depth, 'Params', last)
        if self.current_token[1] == 'int':
            self.match('int', depth + 1, last=False)
            self.match('ID', depth + 1, last=False)
            self.ParamPrime(depth + 1, last=False)
            self.ParamList(depth + 1, last=True)
        elif self.current_token[1] == 'void':
            self.match('void', depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Expected int or void', last=True)

    def ParamPrime(self, depth, last=True):
        self.write_node(depth, 'ParamPrime', last)
        if self.current_token[1] == '[':
            self.match('[', depth + 1, last=False)
            self.match(']', depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def ParamList(self, depth, last=True):
        self.write_node(depth, 'ParamList', last)
        if self.current_token[1] == ',':
            self.match(',', depth + 1, last=False)
            self.Param(depth + 1, last=False)
            self.ParamList(depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def Param(self, depth, last=True):
        self.write_node(depth, 'Param', last)
        self.DeclarationInitial(depth + 1, last=False)
        self.ParamPrime(depth + 1, last=True)

    def CompoundStmt(self, depth, last=True):
        self.write_node(depth, 'CompoundStmt', last)
        self.match('{', depth + 1, last=False)
        self.DeclarationList(depth + 1, last=False)
        self.StatementList(depth + 1, last=False)
        self.match('}', depth + 1, last=True)

    def StatementList(self, depth, last=True):
        self.write_node(depth, 'StatementList', last)
        if self.current_token[0] in {'NUM', 'ID'} or self.current_token[1] in ['if', 'while', 'return', 'break', '(', '{', ';']:
            self.Statement(depth + 1, last=False)
            self.StatementList(depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def Statement(self, depth, last=True):
        self.write_node(depth, 'Statement', last)
        if self.current_token[1] == '{':
            self.CompoundStmt(depth + 1, last=True)
        elif self.current_token[1] == 'if':
            self.SelectionStmt(depth + 1, last=True)
        elif self.current_token[1] == 'while':
            self.IterationStmt(depth + 1, last=True)
        elif self.current_token[1] == 'return':
            self.ReturnStmt(depth + 1, last=True)
        else:
            self.ExpressionStmt(depth + 1, last=True)

    def ExpressionStmt(self, depth, last=True):
        self.write_node(depth, 'ExpressionStmt', last)
        if self.current_token[1] == ';':
            self.match(';', depth + 1, last=True)
        elif self.current_token[1] == 'break':
            self.match('break', depth + 1, last=False)
            self.match(';', depth + 1, last=True)
        else:
            self.Expression(depth + 1, last=False)
            self.match(';', depth + 1, last=True)

    def SelectionStmt(self, depth, last=True):
        self.write_node(depth, 'SelectionStmt', last)
        self.match('if', depth + 1, last=False)
        self.match('(', depth + 1, last=False)
        self.Expression(depth + 1, last=False)
        self.match(')', depth + 1, last=False)
        self.Statement(depth + 1, last=False)
        self.match('else', depth + 1, last=False)
        self.Statement(depth + 1, last=True)

    def IterationStmt(self, depth, last=True):
        self.write_node(depth, 'IterationStmt', last)
        self.match('while', depth + 1, last=False)
        self.match('(', depth + 1, last=False)
        self.Expression(depth + 1, last=False)
        self.match(')', depth + 1, last=False)
        self.Statement(depth + 1, last=True)

    def ReturnStmt(self, depth, last=True):
        self.write_node(depth, 'ReturnStmt', last)
        self.match('return', depth + 1, last=False)
        self.ReturnStmtPrime(depth + 1, last=True)

    def ReturnStmtPrime(self, depth, last=True):
        self.write_node(depth, 'ReturnStmtPrime', last)
        if self.current_token[1] == ';':
            self.match(';', depth + 1, last=True)
        else:
            self.Expression(depth + 1, last=False)
            self.match(';', depth + 1, last=True)

    def Expression(self, depth, last=True):
        self.write_node(depth, 'Expression', last)
        if self.current_token[0] == 'ID':
            self.match('ID', depth + 1, last=False)
            self.B(depth + 1, last=True)
        else:
            self.SimpleExpressionZegond(depth + 1, last=True)

    def B(self, depth, last=True):
        self.write_node(depth, 'B', last)
        if self.current_token[1] == '=':
            self.match('=', depth + 1, last=False)
            self.Expression(depth + 1, last=True)
        elif self.current_token[1] == '[':
            self.match('[', depth + 1, last=False)
            self.Expression(depth + 1, last=False)
            self.match(']', depth + 1, last=False)
            self.H(depth + 1, last=True)
        else:
            self.SimpleExpressionPrime(depth + 1, last=True)

    def H(self, depth, last=True):
        self.write_node(depth, 'H', last)
        if self.current_token[1] == '=':
            self.match('=', depth + 1, last=False)
            self.Expression(depth + 1, last=True)
        else:
            self.G(depth + 1, last=False)
            self.D(depth + 1, last=False)
            self.C(depth + 1, last=True)

    def SimpleExpressionZegond(self, depth, last=True):
        self.write_node(depth, 'SimpleExpressionZegond', last)
        self.AdditiveExpressionZegond(depth + 1, last=False)
        self.C(depth + 1, last=True)

    def SimpleExpressionPrime(self, depth, last=True):
        self.write_node(depth, 'SimpleExpressionPrime', last)
        self.AdditiveExpressionPrime(depth + 1, last=False)
        self.C(depth + 1, last=True)

    def C(self, depth, last=True):
        self.write_node(depth, 'C', last)
        if self.current_token[1] in ['<', '==']:
            self.Relop(depth + 1, last=False)
            self.AdditiveExpression(depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def Relop(self, depth, last=True):
        self.write_node(depth, 'Relop', last)
        if self.current_token[1] in ['<', '==']:
            self.match(self.current_token[1], depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Expected relational operator', last=True)

    def AdditiveExpression(self, depth, last=True):
        self.write_node(depth, 'AdditiveExpression', last)
        self.Term(depth + 1, last=False)
        self.D(depth + 1, last=True)

    def AdditiveExpressionPrime(self, depth, last=True):
        self.write_node(depth, 'AdditiveExpressionPrime', last)
        self.TermPrime(depth + 1, last=False)
        self.D(depth + 1, last=True)

    def AdditiveExpressionZegond(self, depth, last=True):
        self.write_node(depth, 'AdditiveExpressionZegond', last)
        self.TermZegond(depth + 1, last=False)
        self.D(depth + 1, last=True)

    def D(self, depth, last=True):
        self.write_node(depth, 'D', last)
        if self.current_token[1] in ['+', '-']:
            self.Addop(depth + 1, last=False)
            self.Term(depth + 1, last=False)
            self.D(depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def Addop(self, depth, last=True):
        self.write_node(depth, 'Addop', last)
        if self.current_token[1] in ['+', '-']:
            self.match(self.current_token[1], depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Expected + or -', last=True)

    def Term(self, depth, last=True):
        self.write_node(depth, 'Term', last)
        self.SignedFactor(depth + 1, last=False)
        self.G(depth + 1, last=True)

    def TermPrime(self, depth, last=True):
        self.write_node(depth, 'TermPrime', last)
        self.SignedFactorPrime(depth + 1, last=False)
        self.G(depth + 1, last=True)

    def TermZegond(self, depth, last=True):
        self.write_node(depth, 'TermZegond', last)
        self.SignedFactorZegond(depth + 1, last=False)
        self.G(depth + 1, last=True)

    def G(self, depth, last=True):
        self.write_node(depth, 'G', last)
        if self.current_token[1] == '*':
            self.match('*', depth + 1, last=False)
            self.SignedFactor(depth + 1, last=False)
            self.G(depth + 1, last=True)
        else:
            self.write_node(depth + 1, 'epsilon', last=True)

    def SignedFactor(self, depth, last=True):
        self.write_node(depth, 'SignedFactor', last)
        if self.current_token[1] in ['+', '-']:
            self.match(self.current_token[1], depth + 1, last=False)
            self.Factor(depth + 1, last=True)
        else:
            self.Factor(depth + 1, last=True)

    def SignedFactorPrime(self, depth, last=True):
        self.write_node(depth, 'SignedFactorPrime', last)
        self.FactorPrime(depth + 1, last=True)

    def SignedFactorZegond(self, depth, last=True):
        self.write_node(depth, 'SignedFactorZegond', last)
        if self.current_token[1] in ['+', '-']:
            self.match(self.current_token[1], depth + 1, last=False)
            self.Factor(depth + 1, last=True)
        else:
            self.FactorZegond(depth + 1, last=True)

    def Factor(self, depth, last=True):
        self.write_node(depth, 'Factor', last)
        if self.current_token[1] == '(':
            self.match('(', depth + 1, last=False)
            self.Expression(depth + 1, last=False)
            self.match(')', depth + 1, last=True)
        elif self.current_token[0] == 'ID':
            self.match('ID', depth + 1, last=False)
            self.VarCallPrime(depth + 1, last=True)
        elif self.current_token[0] == 'NUM':
            self.match('NUM', depth + 1, last=True)
        else:
            self.syntax_error(depth + 1, 'Invalid factor', last=True)


    def VarCallPrime(self, depth , last=True):
        self.write_node(depth, 'VarCallPrime' , last)
        if self.current_token[1] == '(':
            self.match('(', depth + 1 , last=False)
            self.Args(depth + 1)
            self.match(')', depth + 1 , last=True)
        else:
            self.VarPrime(depth + 1 , last=True)

    def VarPrime(self, depth , last=True):
        self.write_node(depth, 'VarPrime' , last)
        if self.current_token[1] == '[':
            self.match('[', depth + 1 , last=False)
            self.Expression(depth + 1 , last=False)
            self.match(']', depth + 1 , last=True)
        else:
            self.write_node(depth + 1, 'EPSILON' , last=True)

    def FactorPrime(self, depth , last=True):
        self.write_node(depth, 'FactorPrime' , last)
        if self.current_token[1] == '(':
            self.match('(', depth + 1 , last=False)
            self.Args(depth + 1 , last=False)
            self.match(')', depth + 1 , last=True)
        else:
            self.write_node(depth + 1, 'EPSILON' , last=True)

    def FactorZegond(self, depth , last=True):
        self.write_node(depth, 'FactorZegond' , last)
        if self.current_token[1] == '(':
            self.match('(', depth + 1 , last=False)
            self.Expression(depth + 1 , last=False)
            self.match(')', depth + 1 , last=True)
        elif self.current_token[0] == 'NUM':
            self.match('NUM', depth + 1 , last=True)
        else:
            self.syntax_error(depth + 1, 'Invalid factor (Zegond)' , last=True)

    def Args(self, depth , last=True):
        self.write_node(depth, 'Args' , last)
        if self.current_token[0] in ['ID', 'NUM'] or self.current_token[1] in ['(', '+', '-']:
            self.ArgList(depth + 1 , last = True)
        else:
            self.write_node(depth + 1, 'EPSILON' , last=True)

    def ArgList(self, depth , last=True):
        self.write_node(depth, 'ArgList' , last)
        self.Expression(depth + 1 , last=False)
        self.ArgListPrime(depth + 1 , last=True)

    def ArgListPrime(self, depth , last=True):
        self.write_node(depth, 'ArgListPrime' , last)
        if self.current_token[1] == ',':
            self.match(',', depth + 1 , last=False)
            self.Expression(depth + 1 , last=False)
            self.ArgListPrime(depth + 1 , last=True)
        else:
            self.write_node(depth + 1, 'EPSILON' , last=True)

    def parse(self):
        self.Program(0 , last=True)
        self.write_node(1 , '$' , last=True)

        # Write output to files
        with open("parse_tree.txt", "w") as f:
            for line in self.output:
                f.write(line + "\n")

        with open("syntax_errors.txt", "w") as f:
            if not self.errors and not self.scanner.errors:
                f.write("There is no syntax error.\n")
            else:
                for err in self.scanner.errors:
                    f.write(f"Scanner error at line {err[0]}: {err[2]} ('{err[1]}')\n")
                for err in self.errors:
                    f.write(err + "\n")


def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    scanner = Scanner(lines)
    parser = Parser(scanner)
    parser.parse()



if __name__ == "__main__":
    main()