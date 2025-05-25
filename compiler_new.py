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
        self.current_token = None
        self.errors = []
        self.output = []
        self.depth = 0
        self.first_sets = {
            'Program': {'int', 'void', 'epsilon'},
            'DeclarationList': {'int', 'void', 'epsilon'},
            'Declaration': {'int', 'void'},
            'DeclarationInitial': {'int', 'void'},
            'DeclarationPrime': {';', '[', '('},
            'VarDeclarationPrime': {';', '['},
            'FunDeclarationPrime': {'('},
            'TypeSpecifier': {'int', 'void'},
            'Params': {'int', 'void'},
            'ParamList': {',', 'epsilon'},
            'Param': {'int', 'void'},
            'ParamPrime': {'[', 'epsilon'},
            'CompoundStmt': {'{'},
            'StatementList': {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'while', 'return', '+', '-', 'epsilon'},
            'Statement': {'ID', ';', 'NUM', '(', '{', 'break', 'if', 'while', 'return', '+', '-'},
            'ExpressionStmt': {'ID', ';', 'NUM', '(', 'break', '+', '-'},
            'SelectionStmt': {'if'},
            'IterationStmt': {'while'},
            'ReturnStmt': {'return'},
            'ReturnStmtPrime': {';', 'ID', 'NUM', '(', '+', '-'},
            'Expression': {'ID', 'NUM', '(', '+', '-'},
            'B': {'=', '[', '(', '<', '==', '+', '-', '*', 'epsilon'},
            'H': {'=', 'epsilon', '<', '==', '+', '-', '*'},
            'SimpleExpressionZegond': {'NUM', '(', '+', '-'},
            'SimpleExpressionPrime': {'(', 'epsilon', '<', '==', '+', '-', '*'},
            'C': {'<', '==', 'epsilon'},
            'Relop': {'<', '=='},
            'AdditiveExpression': {'ID', 'NUM', '(', '+', '-'},
            'AdditiveExpressionPrime': {'(', 'epsilon', '+', '-', '*'},
            'AdditiveExpressionZegond': {'NUM', '(', '+', '-'},
            'D': {'+', '-', 'epsilon'},
            'Addop': {'+', '-'},
            'Term': {'ID', 'NUM', '(', '+', '-'},
            'TermPrime': {'(', 'epsilon', '*'},
            'TermZegond': {'NUM', '(', '+', '-'},
            'G': {'*', 'epsilon'},
            'SignedFactor': {'+', '-', 'ID', 'NUM', '('},
            'SignedFactorPrime': {'(', 'epsilon'},
            'SignedFactorZegond': {'+', '-', 'NUM', '('},
            'Factor': {'(', 'ID', 'NUM'},
            'VarCallPrime': {'(', '[', 'epsilon'},
            'VarPrime': {'[', 'epsilon'},
            'FactorPrime': {'(', 'epsilon'},
            'FactorZegond': {'(', 'NUM'},
            'Args': {'ID', 'NUM', '(', '+', '-', 'epsilon'},
            'ArgList': {'ID', 'NUM', '(', '+', '-'},
            'ArgListPrime': {',', 'epsilon'}
        }
        self.follow_sets = {
            'Program': {'$'},
            'DeclarationList': {'}', 'NUM', 'while', '+', 'break', '-', '{', 'if', 'return', '(', 'ID', '$', ';'},
            'Declaration': {'}', 'NUM', 'while', '+', 'break', '-', '{', 'void', 'if', '(', 'return', 'ID', 'int', '$', ';'},
            'DeclarationInitial': {',', '[', '(', ';', ')'},
            'DeclarationPrime': {'}', 'NUM', 'while', '+', 'break', '-', '{', 'void', 'if', '(', 'return', 'ID', 'int', '$', ';'},
            'VarDeclarationPrime': {'}', 'NUM', 'while', '+', 'break', '-', '{', 'void', 'if', '(', 'return', 'ID', 'int', '$', ';'},
            'FunDeclarationPrime': {'}', 'NUM', 'while', '+', 'break', '-', '{', 'void', 'if', '(', 'return', 'ID', 'int', '$', ';'},
            'TypeSpecifier': {'ID'},
            'Params': {')'},
            'ParamList': {')'},
            'Param': {',', ')'},
            'ParamPrime': {',', ')'},
            'CompoundStmt': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'void', 'if', '(', 'return', 'ID', 'int', '$', ';'},
            'StatementList': {'}'},
            'Statement': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'if', 'return', '(', 'ID', ';'},
            'ExpressionStmt': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'if', 'return', '(', 'ID', ';'},
            'SelectionStmt': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'if', 'return', '(', 'ID', ';'},
            'IterationStmt': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'if', 'return', '(', 'ID', ';'},
            'ReturnStmt': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'if', 'return', '(', 'ID', ';'},
            'ReturnStmtPrime': {'}', 'NUM', 'while', 'else', 'break', '+', '-', '{', 'if', 'return', '(', 'ID', ';'},
            'Expression': {',', ';', ')', ']'},
            'B': {',', ';', ')', ']'},
            'H': {',', ';', ')', ']'},
            'SimpleExpressionZegond': {',', ';', ')', ']'},
            'SimpleExpressionPrime': {',', ';', ')', ']'},
            'C': {',', ';', ')', ']'},
            'Relop': {'NUM', '+', '-', '(', 'ID'},
            'AdditiveExpression': {',', ';', ')', ']'},
            'AdditiveExpressionPrime': {',', ']', '==', '<', ';', ')'},
            'AdditiveExpressionZegond': {',', ']', '==', '<', ';', ')'},
            'D': {',', ']', '==', '<', ';', ')'},
            'Addop': {'NUM', '+', '-', '(', 'ID'},
            'Term': {',', ']', '+', '-', '==', '<', ';', ')'},
            'TermPrime': {',', ']', '+', '-', '==', '<', ';', ')'},
            'TermZegond': {',', ']', '+', '-', '==', '<', ';', ')'},
            'G': {',', ']', '+', '-', '==', '<', ';', ')'},
            'SignedFactor': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'SignedFactorPrime': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'SignedFactorZegond': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'Factor': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'VarCallPrime': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'VarPrime': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'FactorPrime': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'FactorZegond': {',', ']', '+', '-', '*', '==', '<', ';', ')'},
            'Args': {')'},
            'ArgList': {')'},
            'ArgListPrime': {')'}
        }


    def advance(self):
        while self.current_token[0] == None:
            self.current_token = self.scanner.get_next_token()

    def write_node(self, node):
        self.output.append('\t' * self.depth + node)
    
    def save_parse_tree(self):
        with open("parse_tree.txt", "w") as f:
            for line in self.output:
                f.write(line + "\n")

    def save_errors(self):
        with open("syntax_errors.txt", "w") as f:
            if not self.errors:
                f.write("There is no syntax error.\n")
            else:
                for error in self.errors:
                    f.write(error + "\n")

    def syntax_error(self, message):
        self.errors.append(f"#{self.scanner.line_number + 1} : syntax error, {message}")

    def match(self, expected_value):
        if self.current_token[1] == expected_value:
            self.write_node(f"({self.current_token[0]}, {self.current_token[1]})")
            self.advance()
        elif expected_value == 'ID' and self.current_token[0] == expected_value:
            self.write_node(f"({self.current_token[0]}, {self.current_token[1]})")
            self.advance()
        elif expected_value == 'NUM' and self.current_token[0] == expected_value:
            self.write_node(f"({self.current_token[0]}, {self.current_token[1]})")
            self.advance()
        else:
            self.syntax_error(f"Expected '{expected_value}'")

    def panic_mode(self, non_terminal):
        self.epsilon_allowed = False
        token_type, token_lexeme = self.current_token

        if token_type == '$':
            if '$' not in self.follow_sets[non_terminal]:
                self.errors.append(f"#{self.scanner.current_line} : syntax error, Unexpected EOF")
                self.write_parse_tree()
                self.write_syntax_errors()
                exit()

        if token_type not in self.first_sets[non_terminal] and token_lexeme not in self.first_sets[non_terminal]:
            if "epsilon" in self.first_sets[non_terminal] and (token_type in self.follow_sets[non_terminal] or token_lexeme in self.follow_sets[non_terminal]):
                self.epsilon_allowed = True
            elif token_type not in self.follow_sets[non_terminal] and token_lexeme not in self.follow_sets[non_terminal]:
                illegal_symbol = token_type if token_type in {"NUM", "ID"} else token_lexeme
                self.errors.append(f"#{self.scanner.current_line + 1} : syntax error, illegal {illegal_symbol}")
                return 1
            elif token_type in self.follow_sets[non_terminal] or token_lexeme in self.follow_sets[non_terminal]:
                self.errors.append(f"#{self.scanner.line_number + 1} : syntax error, missing {non_terminal}")
                return 2

        return 0

    def parse(self):
        self.current_token = self.scanner.get_next_token()
        self.advance()
        self.Program()
        self.save_parse_tree()
        self.save_errors()

    def Program(self):
        self.write_node("Program")
        self.depth += 1

        res = self.panic_mode("Program")
        if res == 1:
            self.advance()
            self.Program()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        self.DeclarationList()

        self.depth -= 1

    def DeclarationList(self):
        self.write_node("DeclarationList")
        self.depth += 1

        first = self.first_sets["DeclarationList"]
        follow = self.follow_sets["DeclarationList"]
        token_type, token_lexeme = self.current_token

        if token_lexeme in {'int', 'void'}:
            self.Declaration()
            self.DeclarationList()
        elif "epsilon" in first and (token_lexeme in follow or token_type in follow):
            self.write_node("ε")  # epsilon production
        else:
            self.syntax_error("illegal DeclarationList")
            # Instead of passing follow set, pass the non-terminal name
            res = self.panic_mode("DeclarationList")
            if res == 1:  # Illegal token - skip it
                self.advance()
                self.DeclarationList()
            elif res == 2:  # Missing non-terminal - continue
                pass

        self.depth -= 1

    def Declaration(self):
        self.write_node("Declaration")
        self.depth += 1

        res = self.panic_mode("Declaration")
        if res == 1:
            self.advance()
            self.Declaration()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        self.DeclarationInitial()
        self.DeclarationPrime()
        self.depth -= 1

    def DeclarationInitial(self):
        self.write_node("DeclarationInitial")
        self.depth += 1

        res = self.panic_mode("DeclarationInitial")
        if res == 1:
            self.advance()
            self.DeclarationInitial()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        self.TypeSpecifier()
        self.match('ID')
        self.depth -= 1

    def DeclarationPrime(self):
        self.write_node("DeclarationPrime")
        self.depth += 1

        first = self.first_sets["DeclarationPrime"]
        follow = self.follow_sets["DeclarationPrime"]
        token_type, token_lexeme = self.current_token

        if token_lexeme in {'int', 'void'}:
            self.Declaration()
            self.DeclarationList()
        elif "epsilon" in first and (token_lexeme in follow or token_type in follow):
            self.write_node("ε")  # epsilon production
        else:
            self.syntax_error("illegal DeclarationList")
            # Instead of passing follow set, pass the non-terminal name
            res = self.panic_mode("DeclarationList")
            if res == 1:  # Illegal token - skip it
                self.advance()
                self.DeclarationList()
            elif res == 2:  # Missing non-terminal - continue
                pass

        self.depth -= 1

    def VarDeclarationPrime(self):
        self.write_node("VarDeclarationPrime")
        self.depth += 1

        res = self.panic_mode("VarDeclarationPrime")
        if res == 1:
            self.advance()
            self.VarDeclarationPrime()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        token_type, token_lexeme = self.current_token
        if token_lexeme == ';':
            self.match(';')
        elif token_lexeme == '[':
            self.match('[')
            self.match('NUM')
            self.match(']')
            self.match(';')
        else:
            self.syntax_error("illegal VarDeclarationPrime")
            res = self.panic_mode("VarDeclarationPrime")
            if res == 1:
                self.advance()
        self.depth -= 1


    def VarDeclarationPrime(self):
        self.write_node("VarDeclarationPrime")
        self.depth += 1

        res = self.panic_mode("VarDeclarationPrime")
        if res == 1:
            self.advance()
            self.VarDeclarationPrime()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        token_type, token_lexeme = self.current_token
        if token_lexeme == ';':
            self.match(';')
        elif token_lexeme == '[':
            self.match('[')
            self.match('NUM')
            self.match(']')
            self.match(';')
        else:
            self.syntax_error("illegal VarDeclarationPrime")
            self.panic_mode(self.follow_sets["VarDeclarationPrime"])

        self.depth -= 1

    def FunDeclarationPrime(self):
        self.write_node("FunDeclarationPrime")
        self.depth += 1

        res = self.panic_mode("FunDeclarationPrime")
        if res == 1:
            self.advance()
            self.FunDeclarationPrime()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        self.match('(')
        self.Params()
        self.match(')')
        self.CompoundStmt()

        self.depth -= 1

    def TypeSpecifier(self):
        self.write_node("TypeSpecifier")
        self.depth += 1

        res = self.panic_mode("TypeSpecifier")
        if res == 1:
            self.advance()
            self.TypeSpecifier()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        token_type, token_lexeme = self.current_token
        if token_lexeme == 'int':
            self.match('int')
        elif token_lexeme == 'void':
            self.match('void')
        else:
            self.syntax_error("illegal TypeSpecifier")
            self.panic_mode(self.follow_sets["TypeSpecifier"])

        self.depth -= 1

    def Params(self):
        self.write_node("Params")
        self.depth += 1

        res = self.panic_mode("Params")
        if res == 1:
            self.advance()
            self.Params()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        token_type, token_lexeme = self.current_token
        if token_lexeme == 'void':
            self.match('void')
            # Check for void with no parameters
            next_token = self.scanner.get_next_token()
            if next_token[1] == ')':
                pass  # just void, no parameters
            else:
                self.ParamList()
        elif token_lexeme == 'int':
            self.ParamList()
        else:
            self.syntax_error("illegal Params")
            self.panic_mode(self.follow_sets["Params"])

        self.depth -= 1

    def ParamList(self):
        self.write_node("ParamList")
        self.depth += 1

        res = self.panic_mode("ParamList")
        if res == 1:
            self.advance()
            self.ParamList()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        self.Param()
        token_type, token_lexeme = self.current_token
        if token_lexeme == ',':
            self.match(',')
            self.ParamList()

        self.depth -= 1

    def Param(self):
        self.write_node("Param")
        self.depth += 1

        res = self.panic_mode("Param")
        if res == 1:
            self.advance()
            self.Param()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        self.TypeSpecifier()
        self.match('ID')
        self.ParamPrime()

        self.depth -= 1

    def ParamPrime(self):
        self.write_node("ParamPrime")
        self.depth += 1

        res = self.panic_mode("ParamPrime")
        if res == 1:
            self.advance()
            self.ParamPrime()
            self.depth -= 1
            return
        elif res == 2:
            self.depth -= 1
            return

        token_type, token_lexeme = self.current_token
        if token_lexeme == '[':
            self.match('[')
            self.match(']')
        # epsilon production is handled by not doing anything

        self.depth -= 1