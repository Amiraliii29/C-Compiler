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
    
    import sys # For potential exit calls, though currently avoided

# Helper class for syntax recovery actions (alternative to integer codes)
class SyntaxRecoveryActions:
    PROCEED_AS_EXPECTED = "proceed_normal"
    APPLY_EMPTY_PRODUCTION = "proceed_epsilon"
    SKIP_TOKEN_AND_REASSESS = "skip_and_retry"
    SYNCHRONIZED_SKIP_RULE = "recovered_abort_current_rule"
    MALFORMED_ERROR_AND_SKIP = "malformed_error_and_skip" 

class SyntaxTreeConstructor:
    def __init__(self, token_source_object):
        self.attempt_empty_production_next = False 
        self.token_provider = token_source_object
        self.lookahead_token = None
        self.syntax_error_list = []
        self.derivation_log = []
        self.current_indentation_level = 0
        
        self.prediction_rules = {
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
        self.synchronization_rules = {
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

    def begin_syntax_analysis(self):
        self.lookahead_token = self.token_provider.get_next_token()
        self.attempt_parse_rule_with_recovery('Program', self.construct_Program)
        
        self.generate_derivation_output("parse_tree.txt") 
        self.generate_error_report("syntax_errors.txt") 

    def require_token(self, expected_kind, lexeme_value=None):
        token_kind, current_lexeme = self.lookahead_token
        match_successful = False
        if token_kind == expected_kind and (lexeme_value is None or current_lexeme == lexeme_value):
            self.log_syntax_node(f"({token_kind}, {current_lexeme})") 
            self.lookahead_token = self.token_provider.get_next_token()
            match_successful = True
        else:
            missing_token_desc = lexeme_value if lexeme_value else expected_kind
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, missing {missing_token_desc}" 
            )
        return match_successful

    def log_syntax_node(self, node_label):
        self.derivation_log.append("\t" * self.current_indentation_level + str(node_label)) 

    def generate_derivation_output(self, filename="parse_tree.txt"): 
        try:
            with open(filename, "w") as outfile:
                for entry in self.derivation_log:
                    outfile.write(entry + "\n")
        except IOError:
            print(f"Warning: Could not write derivation log to {filename}")

    def generate_error_report(self, filename="syntax_errors.txt"): 
        try:
            with open(filename, "w") as outfile:
                if not self.syntax_error_list:
                    outfile.write("There is no syntax error.\n") 
                else:
                    for issue in self.syntax_error_list:
                        outfile.write(issue + "\n")
        except IOError:
            print(f"Warning: Could not write error report to {filename}")
            
    def _format_token_for_illegal_error(self , token_kind , token_lexeme):
        if token_kind in {'NUM', 'ID'}:
            return token_kind
        return token_lexeme

    def determine_recovery_action(self, rule_identifier_string):
        self.attempt_empty_production_next = False 

        token_kind, token_lexeme = self.lookahead_token
        symbol_for_set_lookup = token_lexeme if token_kind not in {'ID', 'NUM', '$'} else token_kind
        
        if symbol_for_set_lookup in self.prediction_rules.get(rule_identifier_string, set()) and \
           symbol_for_set_lookup != 'epsilon': 
            return SyntaxRecoveryActions.PROCEED_AS_EXPECTED

        if "epsilon" in self.prediction_rules.get(rule_identifier_string, set()) and \
           symbol_for_set_lookup in self.synchronization_rules.get(rule_identifier_string, set()):
            self.attempt_empty_production_next = True 
            return SyntaxRecoveryActions.APPLY_EMPTY_PRODUCTION

        if token_kind == '$': 
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, Unexpected EOF"
            )
            self.generate_derivation_output()
            self.generate_error_report()
            exit()
            return SyntaxRecoveryActions.SYNCHRONIZED_SKIP_RULE 

        err_token_display_original_format = self._format_token_for_illegal_error(token_kind, token_lexeme)
        
        if symbol_for_set_lookup not in self.synchronization_rules.get(rule_identifier_string, set()):
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, illegal {err_token_display_original_format}"
            )
            return SyntaxRecoveryActions.SKIP_TOKEN_AND_REASSESS
        
        if symbol_for_set_lookup in self.synchronization_rules.get(rule_identifier_string, set()):
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, missing {rule_identifier_string}"
            )
            return SyntaxRecoveryActions.SYNCHRONIZED_SKIP_RULE
        
        self.syntax_error_list.append(
             f"#{self.token_provider.line_number + 1} : syntax error, general issue with token {err_token_display_original_format} for rule {rule_identifier_string}"
        )
        return SyntaxRecoveryActions.SKIP_TOKEN_AND_REASSESS

    def attempt_parse_rule_with_recovery(self, rule_name_key, parsing_method_ref):
        action = self.determine_recovery_action(rule_name_key)
        
        retry_attempts = 0 
        max_retries = 20 

        while action == SyntaxRecoveryActions.SKIP_TOKEN_AND_REASSESS and retry_attempts < max_retries :
            if self.lookahead_token[0] == '$': 
                if not any("Unexpected EOF" in err for err in self.syntax_error_list[-3:]) : 
                    self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, Unexpected EOF during recovery of {rule_name_key}.")
                return 
            self.lookahead_token = self.token_provider.get_next_token()
            action = self.determine_recovery_action(rule_name_key)
            retry_attempts += 1
        
        if retry_attempts >= max_retries and action == SyntaxRecoveryActions.SKIP_TOKEN_AND_REASSESS:
             err_token_display_original_format = self._format_token_for_illegal_error(self.lookahead_token[0], self.lookahead_token[1])
             self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, max recovery attempts for {rule_name_key} at token {err_token_display_original_format}.")
             return

        if action == SyntaxRecoveryActions.PROCEED_AS_EXPECTED:
            parsing_method_ref(use_empty_production=False)
        elif action == SyntaxRecoveryActions.APPLY_EMPTY_PRODUCTION:
            parsing_method_ref(use_empty_production=True)
        elif action == SyntaxRecoveryActions.SYNCHRONIZED_SKIP_RULE:
            pass 

    def _is_token_in_rule_predict_set(self, rule_key):
        token_kind, token_lexeme = self.lookahead_token
        symbol_for_set_lookup = token_lexeme if token_kind not in {'ID', 'NUM', '$'} else token_kind
        return symbol_for_set_lookup in (self.prediction_rules.get(rule_key, set()) - {'epsilon'})

    def _can_rule_be_empty_and_synced(self, rule_key):
        token_kind, token_lexeme = self.lookahead_token
        symbol_for_set_lookup = token_lexeme if token_kind not in {'ID', 'NUM', '$'} else token_kind
        
        is_epsilon_in_predict = "epsilon" in self.prediction_rules.get(rule_key, set())
        is_token_in_sync = symbol_for_set_lookup in self.synchronization_rules.get(rule_key, set())
        
        if is_epsilon_in_predict and is_token_in_sync:
            return True
        return False

    # --- Grammar Rule Processing Methods (Node names are original rule names) ---

    def construct_Program(self, use_empty_production):
        self.log_syntax_node("Program") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("DeclarationList", self.construct_DeclarationList)
        
        if self.lookahead_token[0] == '$':
            self.log_syntax_node("$") 
            self.lookahead_token = self.token_provider.get_next_token() 
        # elif not any("Unexpected EOF" in err for err in self.syntax_error_list[-1:]): 
        #      self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing $")
        self.current_indentation_level -= 1

    def construct_DeclarationList(self, use_empty_production):
        self.log_syntax_node("DeclarationList") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else:
            self.attempt_parse_rule_with_recovery("Declaration", self.construct_Declaration)
            self.attempt_parse_rule_with_recovery("DeclarationList", self.construct_DeclarationList)
        self.current_indentation_level -= 1

    def construct_Declaration(self, use_empty_production):
        self.log_syntax_node("Declaration") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("DeclarationInitial", self.construct_DeclarationInitial)
        self.attempt_parse_rule_with_recovery("DeclarationPrime", self.construct_DeclarationPrime)
        self.current_indentation_level -= 1

    def construct_DeclarationInitial(self, use_empty_production):
        self.log_syntax_node("DeclarationInitial") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("TypeSpecifier", self.construct_TypeSpecifier)
        self.require_token('ID')
        self.current_indentation_level -= 1

    def construct_DeclarationPrime(self, use_empty_production):
        self.log_syntax_node("DeclarationPrime") 
        self.current_indentation_level += 1
        # FIRST(FunDeclarationPrime) = {'('}
        # FIRST(VarDeclarationPrime) = {';', '['}
        # DeclarationPrime itself is not nullable by its FIRST set in prediction_rules
        token_kind, token_lexeme = self.lookahead_token
        if token_lexeme == '(' and token_kind == 'SYMBOL':
             self.attempt_parse_rule_with_recovery("FunDeclarationPrime", self.construct_FunDeclarationPrime)
        elif (token_lexeme == ';' or token_lexeme == '[') and token_kind == 'SYMBOL':
             self.attempt_parse_rule_with_recovery("VarDeclarationPrime", self.construct_VarDeclarationPrime)
        else:
            if not (use_empty_production or self.attempt_empty_production_next):
                self.syntax_error_list.append(
                    f"#{self.token_provider.line_number + 1} : syntax error, missing DeclarationPrime" 
                )
        self.current_indentation_level -= 1

    def construct_VarDeclarationPrime(self, use_empty_production):
        self.log_syntax_node("VarDeclarationPrime") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == ';' and self.lookahead_token[0] == 'SYMBOL':
            self.require_token('SYMBOL', ';')
        elif self.lookahead_token[1] == '[' and self.lookahead_token[0] == 'SYMBOL':
            self.require_token('SYMBOL', '[')
            self.require_token('NUM')
            self.require_token('SYMBOL', ']')
            self.require_token('SYMBOL', ';')
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing VarDeclarationPrime")
            if not self.require_token('SYMBOL', ';'): 
                 pass
        self.current_indentation_level -= 1

    def construct_FunDeclarationPrime(self, use_empty_production):
        self.log_syntax_node("FunDeclarationPrime") 
        self.current_indentation_level += 1
        self.require_token('SYMBOL', '(')
        self.attempt_parse_rule_with_recovery("Params", self.construct_Params)
        self.require_token('SYMBOL', ')')
        self.attempt_parse_rule_with_recovery("CompoundStmt", self.construct_CompoundStmt)
        self.current_indentation_level -= 1

    def construct_TypeSpecifier(self, use_empty_production):
        self.log_syntax_node("TypeSpecifier") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == 'int' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'int')
        elif self.lookahead_token[1] == 'void' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'void')
        else:
            # Error logged by require_token
            self.require_token('KEYWORD', 'int') # Default attempt if error
        self.current_indentation_level -= 1

    def construct_Params(self, use_empty_production):
        self.log_syntax_node("Params") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == 'int' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'int')
            self.require_token('ID')
            self.attempt_parse_rule_with_recovery("ParamPrime", self.construct_ParamPrime)
            self.attempt_parse_rule_with_recovery("ParamList", self.construct_ParamList)
        elif self.lookahead_token[1] == 'void' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'void')
        else:
             pass 
        self.current_indentation_level -= 1

    def construct_ParamList(self, use_empty_production):
        self.log_syntax_node("ParamList") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else:
            self.require_token('SYMBOL', ',')
            self.attempt_parse_rule_with_recovery("Param", self.construct_Param)
            self.attempt_parse_rule_with_recovery("ParamList", self.construct_ParamList)
        self.current_indentation_level -= 1

    def construct_Param(self, use_empty_production):
        self.log_syntax_node("Param") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("DeclarationInitial", self.construct_DeclarationInitial)
        self.attempt_parse_rule_with_recovery("ParamPrime", self.construct_ParamPrime)
        self.current_indentation_level -= 1

    def construct_ParamPrime(self, use_empty_production):
        self.log_syntax_node("ParamPrime") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "[")
            self.require_token("SYMBOL", "]") 
        self.current_indentation_level -= 1

    def construct_CompoundStmt(self, use_empty_production):
        self.log_syntax_node("CompoundStmt") 
        self.current_indentation_level += 1
        self.require_token('SYMBOL', '{')
        self.attempt_parse_rule_with_recovery("DeclarationList", self.construct_DeclarationList)
        self.attempt_parse_rule_with_recovery("StatementList", self.construct_StatementList)
        self.require_token('SYMBOL', '}')
        self.current_indentation_level -= 1

    def construct_StatementList(self, use_empty_production):
        self.log_syntax_node("StatementList") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else:
            self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
            self.attempt_parse_rule_with_recovery("StatementList", self.construct_StatementList)
        self.current_indentation_level -= 1

    def construct_Statement(self, use_empty_production):
        self.log_syntax_node("Statement") 
        self.current_indentation_level += 1
        token_kind, token_lexeme = self.lookahead_token
        
        # Check specific keywords first
        if token_lexeme == '{': 
            self.attempt_parse_rule_with_recovery("CompoundStmt", self.construct_CompoundStmt)
        elif token_lexeme == 'if': 
            self.attempt_parse_rule_with_recovery("SelectionStmt", self.construct_SelectionStmt)
        elif token_lexeme == 'while': 
            self.attempt_parse_rule_with_recovery("IterationStmt", self.construct_IterationStmt)
        elif token_lexeme == 'return': 
            self.attempt_parse_rule_with_recovery("ReturnStmt", self.construct_ReturnStmt)
        # Check if it can be an ExpressionStmt (which includes Expression, break;, ;)
        elif self._is_token_in_rule_predict_set("ExpressionStmt") or \
             (token_lexeme == ';' and token_kind == 'SYMBOL') or \
             (token_lexeme == 'break' and token_kind == 'KEYWORD'):
            self.attempt_parse_rule_with_recovery("ExpressionStmt", self.construct_ExpressionStmt)
        else:
            if not (use_empty_production or self.attempt_empty_production_next): # Statement itself is not epsilon
                 self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Statement")
        self.current_indentation_level -= 1

    def construct_ExpressionStmt(self, use_empty_production):
        self.log_syntax_node("ExpressionStmt")
        self.current_indentation_level += 1
        token_kind, token_lexeme = self.lookahead_token

        # ExpressionStmt -> Expression ; | break ; | ;
        # If 'epsilon' is in FIRST(ExpressionStmt), it corresponds to the ';' production if current token allows.
        if token_lexeme == ';' and token_kind == 'SYMBOL': # Empty statement production ;
            self.require_token("SYMBOL", ";")
        elif token_lexeme == 'break' and token_kind == 'KEYWORD': # break ;
            self.require_token("KEYWORD", "break")
            self.require_token("SYMBOL", ";")
        elif self._is_token_in_rule_predict_set("Expression"): # Expression ;
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", ";")
        # The 'use_empty_production' or 'attempt_empty_production_next' is for when ExpressionStmt as a whole
        # is treated as epsilon, usually because its only content (like Expression) could be epsilon,
        # and the following ';' is handled.
        # The original FIRST set for ExpressionStmt has 'epsilon'. This means if `determine_recovery_action`
        # chose APPLY_EMPTY_PRODUCTION for ExpressionStmt, this path is taken.
        # This implies that the structure leading to this allows a completely empty statement.
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing ExpressionStmt")
            self.require_token("SYMBOL", ";") # Attempt to sync
        self.current_indentation_level -= 1

    def construct_SelectionStmt(self, use_empty_production):
        self.log_syntax_node("SelectionStmt") 
        self.current_indentation_level += 1
        self.require_token("KEYWORD", "if")
        self.require_token("SYMBOL", "(")
        self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        self.require_token("SYMBOL", ")")
        self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
        
        if self.lookahead_token[1] == 'else' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token("KEYWORD", "else")
            self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing else")
            self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
        self.current_indentation_level -= 1

    def construct_IterationStmt(self, use_empty_production):
        self.log_syntax_node("IterationStmt") 
        self.current_indentation_level += 1
        self.require_token("KEYWORD", "while")
        self.require_token("SYMBOL", "(")
        self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        self.require_token("SYMBOL", ")")
        self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
        self.current_indentation_level -= 1

    def construct_ReturnStmt(self, use_empty_production):
        self.log_syntax_node("ReturnStmt") 
        self.current_indentation_level += 1
        self.require_token('KEYWORD', 'return')
        self.attempt_parse_rule_with_recovery("ReturnStmtPrime", self.construct_ReturnStmtPrime)
        self.current_indentation_level -= 1

    def construct_ReturnStmtPrime(self, use_empty_production):
        self.log_syntax_node("ReturnStmtPrime") 
        self.current_indentation_level += 1
        # ReturnStmtPrime -> Expression ; | ;
        if self.lookahead_token[1] == ';' and self.lookahead_token[0] == 'SYMBOL':
            self.require_token('SYMBOL', ';')    
        elif self._is_token_in_rule_predict_set("Expression"): 
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token('SYMBOL', ';')
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing ReturnStmtPrime")
            self.require_token('SYMBOL', ';') 
        self.current_indentation_level -= 1

    def construct_Expression(self, use_empty_production):
        self.log_syntax_node("Expression") 
        self.current_indentation_level += 1
        # Expression -> SimpleExpressionZegond | ID B 
        if self._is_token_in_rule_predict_set("SimpleExpressionZegond"):
            self.attempt_parse_rule_with_recovery("SimpleExpressionZegond", self.construct_SimpleExpressionZegond)
        elif self.lookahead_token[0] == "ID":
            self.require_token("ID")
            self.attempt_parse_rule_with_recovery("B", self.construct_B)
        else:
            # Expression cannot be epsilon by its FIRST set definition here.
            # If this 'else' is reached, it means determine_recovery_action for 'Expression' failed to guide properly
            # or the token is genuinely not part of an Expression.
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Expression")
        self.current_indentation_level -= 1

    def construct_B(self, use_empty_production):
        self.log_syntax_node("B") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == "=" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "=")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        elif self.lookahead_token[1] == "[" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "[")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", "]")
            self.attempt_parse_rule_with_recovery("H", self.construct_H)
        # Check for SimpleExpressionPrime (which can also be epsilon, handled by _can_rule_be_empty_and_synced)
        elif self._is_token_in_rule_predict_set("SimpleExpressionPrime") or \
             self._can_rule_be_empty_and_synced("SimpleExpressionPrime"): 
            self.attempt_parse_rule_with_recovery("SimpleExpressionPrime", self.construct_SimpleExpressionPrime)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing B")
        self.current_indentation_level -= 1

    def construct_H(self, use_empty_production):
        self.log_syntax_node("H") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == "=" and self.lookahead_token[0] == 'SYMBOL': 
            self.require_token("SYMBOL", "=")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        elif self._is_token_in_rule_predict_set("G") or \
             ("epsilon" in self.prediction_rules.get("G",{})) and self._is_token_in_rule_predict_set("D") or \
             ("epsilon" in self.prediction_rules.get("G",{})) and ("epsilon" in self.prediction_rules.get("D",{})) and self._is_token_in_rule_predict_set("C") or \
             self._can_rule_be_empty_and_synced("G"): 
            self.attempt_parse_rule_with_recovery("G", self.construct_G)
            self.attempt_parse_rule_with_recovery("D", self.construct_D)
            self.attempt_parse_rule_with_recovery("C", self.construct_C)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing H")
        self.current_indentation_level -= 1

    def construct_SimpleExpressionZegond(self, use_empty_production):
        self.log_syntax_node("SimpleExpressionZegond") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("AdditiveExpressionZegond", self.construct_AdditiveExpressionZegond)
        self.attempt_parse_rule_with_recovery("C", self.construct_C)
        self.current_indentation_level -= 1

    def construct_SimpleExpressionPrime(self, use_empty_production):
        self.log_syntax_node("SimpleExpressionPrime") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("AdditiveExpressionPrime", self.construct_AdditiveExpressionPrime)
        self.attempt_parse_rule_with_recovery("C", self.construct_C)
        self.current_indentation_level -= 1

    def construct_C(self, use_empty_production):
        self.log_syntax_node("C") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.attempt_parse_rule_with_recovery("Relop", self.construct_Relop)
            self.attempt_parse_rule_with_recovery("AdditiveExpression", self.construct_AdditiveExpression)
        self.current_indentation_level -= 1

    def construct_Relop(self, use_empty_production):
        self.log_syntax_node("Relop") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == "<" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "<")
        elif self.lookahead_token[1] == "==" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "==")
        else:
            # Error logged by require_token if none match.
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Relop")
        self.current_indentation_level -= 1

    def construct_AdditiveExpression(self, use_empty_production):
        self.log_syntax_node("AdditiveExpression") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("Term", self.construct_Term)
        self.attempt_parse_rule_with_recovery("D", self.construct_D)
        self.current_indentation_level -= 1

    def construct_AdditiveExpressionPrime(self, use_empty_production):
        self.log_syntax_node("AdditiveExpressionPrime") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("TermPrime", self.construct_TermPrime)
        self.attempt_parse_rule_with_recovery("D", self.construct_D)
        self.current_indentation_level -= 1

    def construct_AdditiveExpressionZegond(self, use_empty_production):
        self.log_syntax_node("AdditiveExpressionZegond") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("TermZegond", self.construct_TermZegond)
        self.attempt_parse_rule_with_recovery("D", self.construct_D)
        self.current_indentation_level -= 1

    def construct_D(self, use_empty_production):
        self.log_syntax_node("D") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.attempt_parse_rule_with_recovery("Addop", self.construct_Addop)
            self.attempt_parse_rule_with_recovery("Term", self.construct_Term)
            self.attempt_parse_rule_with_recovery("D", self.construct_D) 
        self.current_indentation_level -= 1

    def construct_Addop(self, use_empty_production):
        self.log_syntax_node("Addop") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == '+' and self.lookahead_token[0] == 'SYMBOL':
             self.require_token('SYMBOL', '+')
        elif self.lookahead_token[1] == '-' and self.lookahead_token[0] == 'SYMBOL':
             self.require_token('SYMBOL', '-')
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Addop")
        self.current_indentation_level -= 1

    def construct_Term(self, use_empty_production):
        self.log_syntax_node("Term") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("SignedFactor", self.construct_SignedFactor)
        self.attempt_parse_rule_with_recovery("G", self.construct_G)
        self.current_indentation_level -= 1

    def construct_TermPrime(self, use_empty_production):
        self.log_syntax_node("TermPrime") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("SignedFactorPrime", self.construct_SignedFactorPrime)
        self.attempt_parse_rule_with_recovery("G", self.construct_G)
        self.current_indentation_level -= 1

    def construct_TermZegond(self, use_empty_production):
        self.log_syntax_node("TermZegond") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("SignedFactorZegond", self.construct_SignedFactorZegond)
        self.attempt_parse_rule_with_recovery("G", self.construct_G)
        self.current_indentation_level -= 1

    def construct_G(self, use_empty_production):
        self.log_syntax_node("G") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "*")
            self.attempt_parse_rule_with_recovery("SignedFactor", self.construct_SignedFactor)
            self.attempt_parse_rule_with_recovery("G", self.construct_G) 
        self.current_indentation_level -= 1

    def construct_SignedFactor(self, use_empty_production):
        self.log_syntax_node("SignedFactor") 
        self.current_indentation_level += 1
        if (self.lookahead_token[1] == '+' or self.lookahead_token[1] == '-') and \
           self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", self.lookahead_token[1]) 
            self.attempt_parse_rule_with_recovery("Factor", self.construct_Factor)
        elif self._is_token_in_rule_predict_set("Factor"): 
            self.attempt_parse_rule_with_recovery("Factor", self.construct_Factor)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing SignedFactor")
        self.current_indentation_level -= 1

    def construct_SignedFactorPrime(self, use_empty_production):
        self.log_syntax_node("SignedFactorPrime") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("FactorPrime", self.construct_FactorPrime)
        self.current_indentation_level -= 1

    def construct_SignedFactorZegond(self, use_empty_production):
        self.log_syntax_node("SignedFactorZegond") 
        self.current_indentation_level += 1
        if (self.lookahead_token[1] == '+' or self.lookahead_token[1] == '-') and \
           self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", self.lookahead_token[1])
            self.attempt_parse_rule_with_recovery("FactorZegond", self.construct_FactorZegond) 
        elif self._is_token_in_rule_predict_set("FactorZegond"): 
            self.attempt_parse_rule_with_recovery("FactorZegond", self.construct_FactorZegond)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing SignedFactorZegond")
        self.current_indentation_level -= 1

    def construct_Factor(self, use_empty_production):
        self.log_syntax_node("Factor") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == "(" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", ")") 
        elif self.lookahead_token[0] == "ID":
            self.require_token("ID")
            self.attempt_parse_rule_with_recovery("VarCallPrime", self.construct_VarCallPrime)
        elif self.lookahead_token[0] == "NUM":
            self.require_token("NUM")
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Factor")
        self.current_indentation_level -= 1

    def construct_VarCallPrime(self, use_empty_production):
        self.log_syntax_node("VarCallPrime") 
        self.current_indentation_level += 1

        token_kind, token_lexeme = self.lookahead_token

        if token_lexeme == '(' and token_kind == 'SYMBOL':
            # Path: VarCallPrime -> ( Args )
            # This corresponds to the original: if self.current_token[1] == "(":
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Args", self.construct_Args)
            self.require_token("SYMBOL", ")")
        elif self._is_token_in_rule_predict_set("VarPrime") or \
             self._can_rule_be_empty_and_synced("VarPrime"):
            # Path: VarCallPrime -> VarPrime
            # This covers VarPrime starting with '[' or VarPrime being epsilon.
            # Original: elif self.check_in_first("VarPrime"): self.VarPrime()
            #           else: if self.check_epsilon("VarPrime"): self.VarPrime()
            self.attempt_parse_rule_with_recovery("VarPrime", self.construct_VarPrime)
        else:
            # Fallback: This case should ideally be handled by the recovery mechanism
            # for VarCallPrime before calling this function if the token doesn't fit any production.
            # The original code had a default to trying to match '(', which would then error.
            # If we reach here, it implies PROCEED_AS_EXPECTED was returned by determine_recovery_action,
            # but no production path was matched. This usually means an issue with prediction sets or logic.
            # For safety, and to mimic the original's fallback error:
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, missing VarCallPrime"
            )
            # Original fallback implies it expected '(':
            # self.require_token("SYMBOL", "(") # This would log a "missing (" error
            # self.attempt_parse_rule_with_recovery("Args", self.construct_Args)
            # self.require_token("SYMBOL", ")")
            # However, a simple error log is safer if the state is truly unexpected.
            
        self.current_indentation_level -= 1


    def construct_VarPrime(self, use_empty_production): 
        self.log_syntax_node("VarPrime") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "[")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", "]")
        self.current_indentation_level -= 1

    def construct_FactorPrime(self, use_empty_production): 
        self.log_syntax_node("FactorPrime") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Args", self.construct_Args)
            self.require_token("SYMBOL", ")")
        self.current_indentation_level -= 1

    def construct_FactorZegond(self, use_empty_production):
        self.log_syntax_node("FactorZegond") 
        self.current_indentation_level += 1
        if self.lookahead_token[1] == "(" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", ")")
        elif self.lookahead_token[0] == "NUM":
            self.require_token("NUM")
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing FactorZegond")
        self.current_indentation_level -= 1

    def construct_Args(self, use_empty_production):
        self.log_syntax_node("Args") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.attempt_parse_rule_with_recovery("ArgList", self.construct_ArgList)
        self.current_indentation_level -= 1

    def construct_ArgList(self, use_empty_production):
        self.log_syntax_node("ArgList") 
        self.current_indentation_level += 1
        self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        self.attempt_parse_rule_with_recovery("ArgListPrime", self.construct_ArgListPrime)
        self.current_indentation_level -= 1
        
    def construct_ArgListPrime(self, use_empty_production):
        self.log_syntax_node("ArgListPrime") 
        self.current_indentation_level += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", ",")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.attempt_parse_rule_with_recovery("ArgListPrime", self.construct_ArgListPrime)
        self.current_indentation_level -= 1

def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    scanner = Scanner(lines)
    parser = SyntaxTreeConstructor(scanner)
    parser.begin_syntax_analysis()



if __name__ == "__main__":
    main()