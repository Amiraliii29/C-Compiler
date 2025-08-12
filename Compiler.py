# Mehrshad Dehghani  401105912
# Amirali Sheikhi   401106158

# class Scanner:
#     KEYWORDS = ['if', 'else', 'void', 'int', 'while', 'break', 'return']
#     SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']

#     def __init__(self, lines):
#         self.lines = lines
#         self.line_number = 0
#         self.index = 0
#         self.inside_comment = False
#         self.comment_start_line = None
#         self.current_line = ''
#         self.errors = []

#     def is_letter(self, ch): return ch.isalpha()
#     def is_digit(self, ch): return ch.isdigit()
#     def is_alnum(self, ch): return ch.isalnum()
#     def is_whitespace(self, ch): return ch in ' \n\r\t\v\f'

#     def get_next_token(self):
#         while self.line_number < len(self.lines):
#             line = self.lines[self.line_number]
#             if self.index >= len(line):
#                 self.line_number += 1
#                 self.index = 0
#                 continue

#             ch = line[self.index]

#             # Skip whitespace
#             if self.is_whitespace(ch):
#                 self.index += 1
#                 continue

#             # Comment start
#             if ch == '/' and self.index + 1 < len(line) and line[self.index + 1] == '*':
#                 self.inside_comment = True
#                 self.comment_start_line = self.line_number + 1
#                 self.index += 2
#                 while self.line_number < len(self.lines):
#                     line = self.lines[self.line_number]
#                     while self.index < len(line):
#                         if line[self.index] == '*' and self.index + 1 < len(line) and line[self.index + 1] == '/':
#                             self.inside_comment = False
#                             self.index += 2
#                             break
#                         self.index += 1
#                     if not self.inside_comment:
#                         break
#                     self.line_number += 1
#                     self.index = 0
#                 continue

#             # Unmatched comment end
#             if ch == '*' and self.index + 1 < len(line) and line[self.index + 1] == '/':
#                 self.errors.append((self.line_number + 1, '*/', 'Unmatched comment'))
#                 self.index += 2
#                 continue

#             # == or =
#             if ch == '=':
#                 if self.index + 1 < len(line) and line[self.index + 1] == '=':
#                     self.index += 2
#                     return ('SYMBOL', '==')
#                 elif self.index + 1 < len(line) and (not self.is_alnum(line[self.index + 1]) and not self.is_whitespace(line[self.index + 1])):
#                     self.errors.append((self.line_number, ch + line[self.index + 1], 'Invalid input'))
#                     self.index += 2
#                     continue
#                 else:
#                     self.index += 1
#                     return ('SYMBOL', '=')

#             # Single-character symbols
#             if ch in self.SYMBOLS:
#                 if self.index + 1 < len(line):
#                     next_ch = line[self.index + 1]
#                     if ch == "*" or ch == "/":
#                         if not self.is_whitespace(next_ch) and next_ch not in self.SYMBOLS and not self.is_letter(next_ch) and not self.is_digit(next_ch) and next_ch != '=':
#                             self.errors.append((self.line_number, ch + next_ch, 'Invalid input'))
#                             return None, self.index + 2
#                 self.index += 1        
#                 return ('SYMBOL', ch)
#             # Numbers
#             if self.is_digit(ch):
#                 start = self.index
#                 while self.index < len(line) and self.is_digit(line[self.index]):
#                     self.index += 1
#                 if self.index < len(line) and (self.is_letter(line[self.index]) or (not self.is_whitespace(line[self.index]) and line[self.index] not in self.SYMBOLS + ["="] )):
#                     self.index += 1
#                     self.errors.append((self.line_number, line[start:self.index], 'Invalid number'))
#                     continue
#                 return ('NUM', line[start:self.index])

#             # Identifiers and keywords
#             if self.is_letter(ch):
#                 start = self.index
#                 while self.index < len(line) and self.is_alnum(line[self.index]):
#                     self.index += 1
#                 if self.index < len(line) and not self.is_whitespace(line[self.index]) and line[self.index] not in self.SYMBOLS + ['=']:
#                     invalid_start = start
#                     self.index += 1
#                     self.errors.append((self.line_number, line[invalid_start:self.index], 'Invalid input'))
#                     continue
#                 word = line[start:self.index]
#                 if word in self.KEYWORDS:
#                     return ('KEYWORD', word)
#                 return ('ID', word)

#             # Invalid input
#             self.errors.append((self.line_number + 1, ch, 'Invalid input'))
#             self.index += 1

#         # End of input
#         return ('$', '$')

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
                    return ('SYMBOL', '==' , self.line_number + 1 )
                elif self.index + 1 < len(line) and (not self.is_alnum(line[self.index + 1]) and not self.is_whitespace(line[self.index + 1])):
                    self.errors.append((self.line_number, ch + line[self.index + 1], 'Invalid input'))
                    self.index += 2
                    continue
                else:
                    self.index += 1
                    return ('SYMBOL', '=' , self.line_number + 1)

            # Single-character symbols
            if ch in self.SYMBOLS:
                if self.index + 1 < len(line):
                    next_ch = line[self.index + 1]
                    if ch == "*" or ch == "/":
                        if not self.is_whitespace(next_ch) and next_ch not in self.SYMBOLS and not self.is_letter(next_ch) and not self.is_digit(next_ch) and next_ch != '=':
                            self.errors.append((self.line_number, ch + next_ch, 'Invalid input'))
                            return None, self.index + 2
                self.index += 1        
                return ('SYMBOL', ch , self.line_number + 1)
            # Numbers
            if self.is_digit(ch):
                start = self.index
                while self.index < len(line) and self.is_digit(line[self.index]):
                    self.index += 1
                if self.index < len(line) and (self.is_letter(line[self.index]) or (not self.is_whitespace(line[self.index]) and line[self.index] not in self.SYMBOLS + ["="] )):
                    self.index += 1
                    self.errors.append((self.line_number, line[start:self.index], 'Invalid number'))
                    continue
                return ('NUM', line[start:self.index] , self.line_number + 1)

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
                    return ('KEYWORD', word , self.line_number + 1)
                # self.add_to_symbol_table(word)
                return ('ID', word , self.line_number + 1)

            # Invalid input
            self.errors.append((self.line_number + 1, ch, 'Invalid input'))
            self.index += 1

        # End of input
        return ('$', '$' , self.line_number + 1)
    
class CodeGen:
    def __init__(self):
        self.semantic_stack = list()
        self.return_stack = list()
        self.break_stack = list()
        self.output = dict()
        self.temp_address = 500
        self.index = 0
        self.operations_symbols = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}

        self.saved_type = 'void'
        self.current_scope = 0  # Default scope

        self.semantic_errors = []

        # Our real symbol table: [(name, type, address, scope)]
        self.symbol_table = [] 

        # Pre-populate the symbol table with the built-in 'output' function.
        # Structure: (name, type, [return_value, params, return_address, entry_point], scope)
        # We can use placeholder values for addresses since it's a special case.
        output_params = [('x', 'int', 'p_addr_0', 1)] # A dummy parameter list
        self.symbol_table.append(('output', 'function', ['r_val_out', output_params, 'r_addr_out', 'builtin'], 0))

    def get_temp(self, count=1):
        address = str(self.temp_address)
        for _ in range(count):
            self.insert_code('ASSIGN', '#0', str(self.temp_address))
            self.temp_address += 4
        return address

        # In class CodeGen, inside code_generator.py

    def get_type_by_address(self, address):
        # Handle immediate values, which are always 'int'
        if isinstance(address, str) and address.startswith('#'):
            return 'int'
        
        # Find the variable in the symbol table by its address
        for record in self.symbol_table:
            # Check if the record is a variable/param and the address matches
            if isinstance(record, tuple) and len(record) == 4 and record[2] == address:
                return record[1]  # Return the type ('int' or 'int*')
        return None # Return None if not found
    
    def search_in_symbol_table(self, item, scope_num=0):
        # Search from latest to oldest (most recent declaration first)
        for record in self.symbol_table[::-1]:
            name, typ, address, scope = record
            if item == name and scope <= scope_num:
                return address  # or return record if you want full info
        return False
    
    def find_address(self, item):
        if item == 'output':
            return item
        for record in self.symbol_table[::-1]:
            if item == record[0]:
                return record[2]  # Return the address
        return None  # Or raise an error if needed

    
    def insert_code(self, a1, a2, a3='', a4=''):
        self.output[self.index] = f'({a1}, {a2}, {a3}, {a4})'
        self.index += 1

    def push(self, value):
        self.semantic_stack.append(value)

    def pop(self):
        return self.semantic_stack.pop()

    def top(self):
        return self.semantic_stack[-1] if self.semantic_stack else None

    def emit(self, code_line):
        self.output.append(code_line)

    def get_output(self):
        return "\n".join(self.output)
    
    def get_id_type(self, lexeme):
        self.saved_type = lexeme # always int or void

    def push_id(self, lexeme):
        self.push(lexeme)

    def push_num(self, lexeme):
        self.push(f'#{lexeme}')    

    def define_variable(self, lookahead=None):
        var_id = self.pop()
        self.void_check(var_id)

        address = self.get_temp()
        self.insert_code('ASSIGN', '#0', address)

        self.symbol_table.append((var_id, 'int', address, self.current_scope))
    

    def define_array(self, lookahead=None):
        array_size = int(self.pop()[1:])
        array_id = self.pop()
        self.void_check(array_id)

        address = self.get_temp()
        array_space = self.get_temp(array_size)

        self.insert_code('ASSIGN', f'#{array_space}', address)

        self.symbol_table.append((array_id, 'int*', address, self.current_scope))

    def scope_check(self, lookahead):
        if self.search_in_symbol_table(lookahead[1], self.current_scope) or lookahead[1] == 'output':
            return
        self.semantic_errors.append(f'#{lookahead[2]} : Semantic Error! \'{lookahead[1]}\' is not defined.')

    def void_check(self, var_id):
        # self.saved_type is now a 3-element tuple, e.g., ('KEYWORD', 'void', 5)
        if self.saved_type[1] == 'void':
            # FIX: Use the saved line number from saved_type[2]
            self.semantic_errors.append(f'#{self.saved_type[2]} : Semantic Error! Illegal type of void for \'{var_id}\'.')

    def break_check(self, lookahead):
        if len(self.break_stack) > 0 and ['>>>' in self.break_stack]:
            return
        self.semantic_errors.append(
            f'#{lookahead[2]} : Semantic Error! No \'while\' found for \'break\'.')

    def type_mismatch_check(self, lookahead, operand_1, operand_2):
        # print(operand_1,operand_2)

        if operand_2 is None or operand_1 is None:
            return
        operand_2_type = 'int'
        operand_1_type = 'int'
        if not operand_1.startswith('#'):
            for s in self.symbol_table:
                if s[2] == operand_1:
                    operand_1_type = s[1]
                    break
        if not operand_2.startswith('#'):
            for s in self.symbol_table:
                if s[2] == operand_2:
                    operand_2_type = s[1]
                    break

        if operand_2_type != operand_1_type:
            operand_1_type = 'array' if operand_1_type == 'int*' else operand_1_type
            operand_2_type = 'array' if operand_2_type == 'int*' else operand_2_type
            self.semantic_errors.append(
                f'#{lookahead[2]} : Semantic Error! Type mismatch in operands, Got {operand_2_type} instead of {operand_1_type}.')    

    def parameter_type_matching(self, lookahead, var, arg, num):
        if arg.startswith('#'):
            if var[1] != 'int':
                var_type = 'array' if var[1] == 'int*' else var[1]
                self.semantic_errors.append(
                    f'#{lookahead[2]} : Semantic Error! Mismatch in type of argument {num} of \'{self.get_func_name(var)}\'. Expected \'{var_type}\' but got \'int\' instead.')
        else:
            for rec in self.symbol_table:
                if rec[2] == arg and rec[1] != var[1]:
                    type = 'array' if rec[1] == 'int*' else rec[1]
                    var_type = 'array' if var[1] == 'int*' else var[1]
                    self.semantic_errors.append(
                        f'#{lookahead[2]} : Semantic Error! Mismatch in type of argument {num} of \'{self.get_func_name(var)}\'. Expected \'{var_type}\' but got \'{type}\' instead.')

    def get_func_name(self, var):
        for rec in self.symbol_table:
            if rec[1] == 'function':
                for arg in rec[2][1]:
                    if arg[2] == var[2]:
                        return rec[0]
    def parameter_num_matching(self, lookahead, args, attributes):
        func_name = ''
        for i in self.symbol_table:
            if i[2] == attributes:
                func_name = i[0]
        func_args = []
        for i in attributes:
            if isinstance(i, list):
                func_args = i
        if len(func_args) != len(args):
            self.semantic_errors.append(
                f'#{lookahead[2]} : Semantic Error! Mismatch in numbers of arguments of \'{func_name}\'.')
                            
    def start_params(self, lookahead):
        """marks the symbol table so that the args are recognized later.
        It also saves a place for jumping over for non-main functions.
        """
        func_attr = self.semantic_stack.pop()
        self.semantic_stack.append(self.index)  # to jump over for non-main functions
        self.index += 1
        self.semantic_stack.append(func_attr)
        # mark the table before adding args
        self.symbol_table.append('>>')

    def create_record(self, lookahead):
        """adds the function and its attributes to the symbol table"""
        return_address = self.get_temp()
        current_index = self.index  # where we jump to on call
        return_value = self.get_temp()
        self.semantic_stack.append(return_value)
        self.semantic_stack.append(return_address)
        func_id = self.semantic_stack[-3]
        args_start_idx = self.symbol_table.index('>>')
        func_args = self.symbol_table[args_start_idx + 1:]
        self.symbol_table.pop(args_start_idx)
        self.symbol_table \
            .append((func_id, 'function', [return_value, func_args, return_address, current_index], self.current_scope))

    # Manage returns
    def new_return(self, lookahead):
        """indicates new function so that every report between this and #end_return
        sets the return value and jumps to the address set by the caller
        """
        self.return_stack.append('>>>')

    def end_return(self, lookahead):
            """called at the end of the function, fills the gaps created by returns"""
            latest_func = len(self.return_stack) - self.return_stack[::-1].index('>>>') - 1
            return_value = self.semantic_stack[-2]
            return_address = self.semantic_stack[-1]
            for item in self.return_stack[latest_func + 1:]:
                self.output[item[0]] = f'(ASSIGN, {item[1]}, {return_value}, )'
                self.output[item[0] + 1] = f'(JP, @{return_address}, , )'
            self.return_stack = self.return_stack[:latest_func]

    def finish_function(self, lookahead):
            """in create_record we saved an instruction for now,
            so that non-main functions are jumped over.
            Also, we need to clean up the mess we've made in SS.
            """
            self.semantic_stack.pop(), self.semantic_stack.pop(), self.semantic_stack.pop()
            # all this shit only to exclude main from being jumped over
            for item in self.symbol_table[::-1]:
                if item[1] == 'function':
                    if item[0] == 'main':
                        self.output[self.semantic_stack.pop()] = f'(ASSIGN, #0, {self.get_temp()}, )'
                        return
                    break
            self.output[self.semantic_stack.pop()] = f'(JP, {self.index}, , )'

    def return_anyway(self, lookahead):
        """places a jump at the end of function. just in case it hasn't already"""
        if self.semantic_stack[-3] != 'main':
            return_address = self.semantic_stack[-1]
            self.insert_code('JP', f'@{return_address}')
    
    def define_array_argument(self, lookahead):
        temp = self.symbol_table[-1]
        del self.symbol_table[-1]
        self.symbol_table.append((temp[0], 'int*', temp[2], temp[3]))

    def push_scope(self, lookahead):
        self.current_scope += 1

    def pop_scope(self, lookahead):
        for record in self.symbol_table[::-1]:
            if record[3] == self.current_scope:
                del self.symbol_table[-1]
        self.current_scope -= 1    

    def clean_up(self, lookahead):
        self.semantic_stack.pop()    

    def break_loop(self, lookahead):
        """saves i to be later filled with a jump to after the scope"""
        self.break_check(lookahead)
        self.break_stack.append(self.index)
        self.index += 1    

    def save(self, lookahead):
        self.semantic_stack.append(self.index)
        self.index += 1

    def jpf_save(self, lookahead):
        dest = self.semantic_stack.pop()
        src = self.semantic_stack.pop()
        self.output[dest] = f'(JPF, {src}, {self.index + 1}, )'
        self.semantic_stack.append(self.index)
        self.index += 1

    def jump(self, lookahead):
        dest = int(self.semantic_stack.pop())
        self.output[dest] = f'(JP, {self.index}, , )'   

    def label(self, lookahead):
        self.semantic_stack.append(self.index)     

    def new_break(self, lookahead):
        """makes sure that break-stmt breaks the deepest breakable scope"""
        self.break_stack.append('>>>')

    def while_jumps(self, lookahead):
        self.output[int(self.semantic_stack[-1])] = f'(JPF, {self.semantic_stack[-2]}, {self.index + 1}, )'
        self.output[self.index] = f'(JP, {self.semantic_stack[-3]}, , )'
        self.index += 1
        self.semantic_stack.pop(), self.semantic_stack.pop(), self.semantic_stack.pop()    

    def end_break(self, lookahead):
        """fills PB[saved i] with a jump to current i and ends the scope"""
        latest_block = len(self.break_stack) - self.break_stack[::-1].index('>>>') - 1
        for item in self.break_stack[latest_block + 1:]:
            self.output[item] = f'(JP, {self.index}, , )'
        self.break_stack = self.break_stack[:latest_block]  

    def save_return(self, lookahead):
        """called by each return. Saves two instructions:
        one for assigning the return value,
        and one for jumping to the caller
        """
        self.return_stack.append((self.index, self.semantic_stack[-1]))
        self.semantic_stack.pop()
        self.index += 2     

    def push_index(self, lookahead):
        self.semantic_stack.append(f'#{self.index}')   

    def push_id_address(self, lookahead):
        self.scope_check(lookahead)
        self.semantic_stack.append(self.find_address(lookahead[1]))    


    def assign_operation(self, lookahead):
        # --- FIX STARTS HERE ---
        rhs_addr = self.semantic_stack[-1]
        lhs_addr = self.semantic_stack[-2]

        rhs_type = self.get_type_by_address(rhs_addr)
        lhs_type = self.get_type_by_address(lhs_addr)

        # Proceed if both types could be determined
        if rhs_type and lhs_type and rhs_type != lhs_type:
            # Format types for a user-friendly error message
            # 'int*' becomes 'array'
            expected_type = 'array' if lhs_type == 'int*' else lhs_type
            mismatched_type = 'array' if rhs_type == 'int*' else rhs_type
            
            # Report the error: "Got [mismatched type] instead of [expected type]"
            self.semantic_errors.append(
                f'#{lookahead[2]} : Semantic Error! Type mismatch in operands, Got {expected_type} instead of {mismatched_type}.')
        # --- FIX ENDS HERE ---

        # Generate code and pop from stack regardless of the error
        self.insert_code('ASSIGN', self.semantic_stack[-1], self.semantic_stack[-2])
        self.semantic_stack.pop()

    def array_index(self, lookahead):
        idx, array_address = self.semantic_stack.pop(), self.semantic_stack.pop()

        temp, result = self.get_temp(), self.get_temp()
        self.insert_code('MULT', '#4', idx, temp)
        self.insert_code('ASSIGN', f'{array_address}', result)
        self.insert_code('ADD', result, temp, result)

        self.semantic_stack.append(f'@{result}')    

    def push_operator(self, lookahead):
        self.semantic_stack.append(lookahead[1])

    def save_operation(self, lookahead):
        operand_2 = self.semantic_stack.pop()
        operator = self.semantic_stack.pop()
        operand_1 = self.semantic_stack.pop()

        self.type_mismatch_check(lookahead, operand_1, operand_2)

        address = self.get_temp()
        self.insert_code(self.operations_symbols[operator], operand_1, operand_2, address)

        self.semantic_stack.append(address)   

    def multiply(self, lookahead):
        result_address = self.get_temp()

        self.insert_code('MULT', self.semantic_stack[-1], self.semantic_stack[-2], result_address)
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.append(result_address)   

    def negate_factor(self, lookahead):
        result = self.get_temp()
        factor_value = self.semantic_stack.pop()
        self.insert_code('SUB', '#0', factor_value, result)
        self.semantic_stack.append(result)     

    def implicit_output(self, lookahead):
        if self.semantic_stack[-2] == 'output':
            self.insert_code('PRINT', self.semantic_stack.pop())     

    def call_function(self, lookahead): ## need to check
        """Does the following:
            1. assigns inputs to args.
            2. sets where the func must return to.
            3. jumps to the beginning of the function.
            4. saves the result (if any) to a temp and pops
               everything about the function and pushes the temp.
        """
        if self.semantic_stack[-1] != 'output':
            args, attributes = [], []
            for item in self.semantic_stack[::-1]:
                if isinstance(item, list):
                    attributes = item
                    break
                args = [item] + args
            self.parameter_num_matching(lookahead, args, attributes)
            # assign each arg
            # print(f"DEBUG: attributes = {attributes}")
            # print(f"DEBUG: args = {args}")
            for var, arg in zip(attributes[1], args):
                self.parameter_type_matching(lookahead, var, arg, attributes[1].index(var) + 1)
                self.insert_code('ASSIGN', arg, var[2])
                self.semantic_stack.pop()  # pop each arg
            for i in range(len(args) - len(attributes[1])):
                self.semantic_stack.pop()
            self.semantic_stack.pop()  # pop func attributes
            # set return address
            self.insert_code('ASSIGN', f'#{self.index + 2}', attributes[2])
            # jump
            self.insert_code('JP', attributes[-1])
            # save result to temp
            result = self.get_temp()
            self.insert_code('ASSIGN', attributes[0], result)
            self.semantic_stack.append(result)          

class SyntaxRecoveryActions:
    PROCEED_AS_EXPECTED = "proceed_normal"
    APPLY_EMPTY_PRODUCTION = "proceed_epsilon"
    SKIP_TOKEN_AND_REASSESS = "skip_and_retry"
    SYNCHRONIZED_SKIP_RULE = "recovered_abort_current_rule"
    MALFORMED_ERROR_AND_SKIP = "malformed_error_and_skip"

class Parser:
    def __init__(self, token_source_object):
        self.attempt_empty_production_next = False 
        self.token_provider = token_source_object
        self.code_gen = CodeGen()
        self.lookahead_token = None
        self.syntax_error_list = []
        self.parse_tree = []
        self.depth = 0

        
        self.firsts = {
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
        self.follows = {
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
        self.generate_intermediate_code("output.txt")
        self.generate_semantic_errors("semantic_errors.txt")


    def require_token(self, expected_kind, lexeme_value=None):
        token_kind, current_lexeme , _ = self.lookahead_token
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
        self.parse_tree.append("\t" * self.depth + str(node_label)) 

    def generate_derivation_output(self, filename="parse_tree.txt"): 
        try:
            with open(filename, "w") as outfile:
                for entry in self.parse_tree:
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

    def generate_semantic_errors(self, filename="semantic_errors.txt"): 
            try:
                with open(filename, "w") as outfile:
                    if not self.code_gen.semantic_errors:
                        outfile.write("There is no syntax error.\n") 
                    else:
                        for issue in self.code_gen.semantic_errors:
                            outfile.write(issue + "\n")
            except IOError:
                print(f"Warning: Could not write error report to {filename}")    

    # In class Parser

    def generate_intermediate_code(self, filename="output.txt"):
            try:
                with open(filename, "w") as outfile:
                    # --- FIX STARTS HERE ---
                    code_listing = self.code_gen.output
                    if not code_listing:
                        outfile.write("The output code has not been generated.\n")
                    else:
                        # Iterate through the sorted line numbers to ensure correct order
                        for line_num in sorted(code_listing.keys()):
                            instruction = code_listing[line_num]
                            outfile.write(f"{line_num}\t{instruction}\n")
                    # --- FIX ENDS HERE ---
            except IOError:
                print(f"Warning: Could not write error report to {filename}")                    
                
    def _format_token_for_illegal_error(self , token_kind , token_lexeme):
        if token_kind in {'NUM', 'ID'}:
            return token_kind
        return token_lexeme

    def determine_recovery_action(self, rule_identifier_string):
        self.attempt_empty_production_next = False 

        token_kind, token_lexeme , _ = self.lookahead_token
        symbol_for_set_lookup = token_lexeme if token_kind not in {'ID', 'NUM', '$'} else token_kind
        
        if symbol_for_set_lookup in self.firsts.get(rule_identifier_string, set()) and \
            symbol_for_set_lookup != 'epsilon': 
            return SyntaxRecoveryActions.PROCEED_AS_EXPECTED

        if "epsilon" in self.firsts.get(rule_identifier_string, set()) and \
            symbol_for_set_lookup in self.follows.get(rule_identifier_string, set()):
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
        
        if symbol_for_set_lookup not in self.follows.get(rule_identifier_string, set()):
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, illegal {err_token_display_original_format}"
            )
            return SyntaxRecoveryActions.SKIP_TOKEN_AND_REASSESS
        
        if symbol_for_set_lookup in self.follows.get(rule_identifier_string, set()):
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
        token_kind, token_lexeme , _ = self.lookahead_token
        symbol_for_set_lookup = token_lexeme if token_kind not in {'ID', 'NUM', '$'} else token_kind
        return symbol_for_set_lookup in (self.firsts.get(rule_key, set()) - {'epsilon'})

    def _can_rule_be_empty_and_synced(self, rule_key):
        token_kind, token_lexeme , _ = self.lookahead_token
        symbol_for_set_lookup = token_lexeme if token_kind not in {'ID', 'NUM', '$'} else token_kind
        
        is_epsilon_in_predict = "epsilon" in self.firsts.get(rule_key, set())
        is_token_in_sync = symbol_for_set_lookup in self.follows.get(rule_key, set())
        
        if is_epsilon_in_predict and is_token_in_sync:
            return True
        return False


    def construct_Program(self, use_empty_production):
        self.log_syntax_node("Program") 
        self.depth += 1

        self.attempt_parse_rule_with_recovery("DeclarationList", self.construct_DeclarationList)
        
        if self.lookahead_token[0] == '$':
            self.log_syntax_node("$") 
            self.lookahead_token = self.token_provider.get_next_token() 

        self.depth -= 1

    def construct_DeclarationList(self, use_empty_production):
        self.log_syntax_node("DeclarationList") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else:
            self.attempt_parse_rule_with_recovery("Declaration", self.construct_Declaration)
            self.attempt_parse_rule_with_recovery("DeclarationList", self.construct_DeclarationList)
        self.depth -= 1

    def construct_Declaration(self, use_empty_production):
        self.log_syntax_node("Declaration") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("DeclarationInitial", self.construct_DeclarationInitial)
        self.attempt_parse_rule_with_recovery("DeclarationPrime", self.construct_DeclarationPrime)
        self.depth -= 1

    def construct_DeclarationInitial(self, use_empty_production):
        self.log_syntax_node("DeclarationInitial") 
        self.depth += 1

        # ACTION: #get_id_type
        self.code_gen.get_id_type(self.lookahead_token)
        self.attempt_parse_rule_with_recovery("TypeSpecifier", self.construct_TypeSpecifier)

        # ACTION: #push_id
        if self.lookahead_token[0] == "ID":
            self.code_gen.push_id(self.lookahead_token[1])

        self.require_token('ID')
        self.depth -= 1

    def construct_DeclarationPrime(self, use_empty_production):
        self.log_syntax_node("DeclarationPrime") 
        self.depth += 1
        token_kind, token_lexeme , _ = self.lookahead_token
        if token_lexeme == '(' and token_kind == 'SYMBOL':
                self.attempt_parse_rule_with_recovery("FunDeclarationPrime", self.construct_FunDeclarationPrime)
        elif (token_lexeme == ';' or token_lexeme == '[') and token_kind == 'SYMBOL':
                self.attempt_parse_rule_with_recovery("VarDeclarationPrime", self.construct_VarDeclarationPrime)
        else:
            if not (use_empty_production or self.attempt_empty_production_next):
                self.syntax_error_list.append(
                    f"#{self.token_provider.line_number + 1} : syntax error, missing DeclarationPrime" 
                )
        self.depth -= 1

    def construct_VarDeclarationPrime(self, use_empty_production):
        self.log_syntax_node("VarDeclarationPrime") 
        self.depth += 1
        if self.lookahead_token[1] == ';' and self.lookahead_token[0] == 'SYMBOL':
            self.require_token('SYMBOL', ';')
            # ACTION: #define_variable
            self.code_gen.define_variable()
        elif self.lookahead_token[1] == '[' and self.lookahead_token[0] == 'SYMBOL':
            self.require_token('SYMBOL', '[')
            # ACTION: #push_num
            if self.lookahead_token[0] == "NUM":
                self.code_gen.push_num(self.lookahead_token[1])
            self.require_token('NUM')
            self.require_token('SYMBOL', ']')
            self.require_token('SYMBOL', ';')

            # ACTION: #define_array
            self.code_gen.define_array()
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing VarDeclarationPrime")
            if not self.require_token('SYMBOL', ';'): 
                 pass
        self.depth -= 1

    def construct_FunDeclarationPrime(self, use_empty_production):
        self.log_syntax_node("FunDeclarationPrime") 
        self.depth += 1
        # Action 
        self.code_gen.start_params(self.lookahead_token)  
        self.require_token('SYMBOL', '(')
        self.attempt_parse_rule_with_recovery("Params", self.construct_Params)
        self.require_token('SYMBOL', ')')

        self.code_gen.create_record(self.lookahead_token)    # #create_record
        self.code_gen.new_return(self.lookahead_token)       # #new_return

        self.attempt_parse_rule_with_recovery("CompoundStmt", self.construct_CompoundStmt)

        self.code_gen.end_return(self.lookahead_token)       # #end_return
        self.code_gen.return_anyway(self.lookahead_token)    # #return_anyway
        self.code_gen.finish_function(self.lookahead_token)  # #finish_function

        self.depth -= 1

    def construct_TypeSpecifier(self, use_empty_production):
        self.log_syntax_node("TypeSpecifier") 
        self.depth += 1
        if self.lookahead_token[1] == 'int' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'int')
        elif self.lookahead_token[1] == 'void' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'void')
        else:
            # Error logged by require_token
            self.require_token('KEYWORD', 'int') # Default attempt if error
        self.depth -= 1

    def construct_Params(self, use_empty_production):
        self.log_syntax_node("Params") 
        self.depth += 1
        if self.lookahead_token[1] == 'int' and self.lookahead_token[0] == 'KEYWORD':
            # get_id_type
            self.code_gen.get_id_type(self.lookahead_token)
            self.require_token('KEYWORD', 'int')
            if self.lookahead_token[0] == 'ID':
                # push_id
                self.code_gen.push_id(self.lookahead_token[1])
            self.require_token('ID')
            # define_variable
            self.code_gen.define_variable(self.lookahead_token)    

            self.attempt_parse_rule_with_recovery("ParamPrime", self.construct_ParamPrime)
            self.attempt_parse_rule_with_recovery("ParamList", self.construct_ParamList)
        elif self.lookahead_token[1] == 'void' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token('KEYWORD', 'void')
        else:
             pass 
        self.depth -= 1

    def construct_ParamList(self, use_empty_production):
        self.log_syntax_node("ParamList") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else:
            self.require_token('SYMBOL', ',')
            self.attempt_parse_rule_with_recovery("Param", self.construct_Param)
            # define_variable (after Param)
            self.code_gen.define_variable(self.lookahead_token)

            self.attempt_parse_rule_with_recovery("ParamList", self.construct_ParamList)
        self.depth -= 1

    def construct_Param(self, use_empty_production):
        self.log_syntax_node("Param") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("DeclarationInitial", self.construct_DeclarationInitial)
        self.attempt_parse_rule_with_recovery("ParamPrime", self.construct_ParamPrime)
        self.depth -= 1

    def construct_ParamPrime(self, use_empty_production):
        self.log_syntax_node("ParamPrime") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.code_gen.define_array_argument(self.lookahead_token)
            self.require_token("SYMBOL", "[")
            self.require_token("SYMBOL", "]") 
            # self.code_gen.define_array_argument(self.lookahead_token)
        self.depth -= 1

    def construct_CompoundStmt(self, use_empty_production):
        self.log_syntax_node("CompoundStmt") 
        self.depth += 1
        # Push a new scope
        self.code_gen.push_scope(self.lookahead_token)
        self.require_token('SYMBOL', '{')
        self.attempt_parse_rule_with_recovery("DeclarationList", self.construct_DeclarationList)
        self.attempt_parse_rule_with_recovery("StatementList", self.construct_StatementList)
        self.require_token('SYMBOL', '}')

        # Pop the current scope
        self.code_gen.pop_scope(self.lookahead_token)

        self.depth -= 1

    def construct_StatementList(self, use_empty_production):
        self.log_syntax_node("StatementList") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else:
            self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
            self.attempt_parse_rule_with_recovery("StatementList", self.construct_StatementList)
        self.depth -= 1

    def construct_Statement(self, use_empty_production):
        self.log_syntax_node("Statement") 
        self.depth += 1
        token_kind, token_lexeme , _ = self.lookahead_token
        
        # Check specific keywords first
        if token_lexeme == '{': 
            self.attempt_parse_rule_with_recovery("CompoundStmt", self.construct_CompoundStmt)
        elif token_lexeme == 'if': 
            self.attempt_parse_rule_with_recovery("SelectionStmt", self.construct_SelectionStmt)
        elif token_lexeme == 'while': 
            self.attempt_parse_rule_with_recovery("IterationStmt", self.construct_IterationStmt)
        elif token_lexeme == 'return': 
            self.attempt_parse_rule_with_recovery("ReturnStmt", self.construct_ReturnStmt)
        # Check if it can be an ExpressionStmt (which includes Expression, break;, 😉
        elif self._is_token_in_rule_predict_set("ExpressionStmt") or \
             (token_lexeme == ';' and token_kind == 'SYMBOL') or \
             (token_lexeme == 'break' and token_kind == 'KEYWORD'):
            self.attempt_parse_rule_with_recovery("ExpressionStmt", self.construct_ExpressionStmt)
        else:
            if not (use_empty_production or self.attempt_empty_production_next): # Statement itself is not epsilon
                 self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Statement")
        self.depth -= 1

    def construct_ExpressionStmt(self, use_empty_production):
        self.log_syntax_node("ExpressionStmt")
        self.depth += 1
        token_kind, token_lexeme , _ = self.lookahead_token

        if token_lexeme == ';' and token_kind == 'SYMBOL': # Empty statement production ;
            self.require_token("SYMBOL", ";")
        elif token_lexeme == 'break' and token_kind == 'KEYWORD': # break ;
            break_token = self.lookahead_token  # 1. Save the token for 'break'
            self.require_token("KEYWORD", "break")
            self.require_token("SYMBOL", ";")
            
            # 2. Pass the saved break_token to the action, not the new lookahead
            self.code_gen.break_loop(break_token)
        elif self._is_token_in_rule_predict_set("Expression"): # Expression ;
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", ";")
            # ACTION: #clean_up
            self.code_gen.clean_up(self.lookahead_token)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing ExpressionStmt")
            self.require_token("SYMBOL", ";") 
        self.depth -= 1    

    def construct_SelectionStmt(self, use_empty_production):
        self.log_syntax_node("SelectionStmt") 
        self.depth += 1
        self.require_token("KEYWORD", "if")
        self.require_token("SYMBOL", "(")
        self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        self.require_token("SYMBOL", ")")

        # ACTION: #save
        self.code_gen.save(self.lookahead_token)

        self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
        
        if self.lookahead_token[1] == 'else' and self.lookahead_token[0] == 'KEYWORD':
            self.require_token("KEYWORD", "else")
            # ACTION: #jpf_save
            self.code_gen.jpf_save(self.lookahead_token)

            self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)

            # ACTION: #jump
            self.code_gen.jump(self.lookahead_token)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing else")
            # ACTION: #jpf_save
            self.code_gen.jpf_save(self.lookahead_token)

            self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)

            # ACTION: #jump
            self.code_gen.jump(self.lookahead_token)

        self.depth -= 1

    def construct_IterationStmt(self, use_empty_production):
        self.log_syntax_node("IterationStmt") 
        self.depth += 1
        self.require_token("KEYWORD", "while")
        # ACTION: #label
        self.code_gen.label(self.lookahead_token)

        self.require_token("SYMBOL", "(")
        self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        self.require_token("SYMBOL", ")")
        # ACTION: #new_break
        self.code_gen.new_break(self.lookahead_token)

        # ACTION: #save
        self.code_gen.save(self.lookahead_token)

        self.attempt_parse_rule_with_recovery("Statement", self.construct_Statement)
        # ACTION: #while_jumps
        self.code_gen.while_jumps(self.lookahead_token)

        # ACTION: #end_break
        self.code_gen.end_break(self.lookahead_token)

        self.depth -= 1

    def construct_ReturnStmt(self, use_empty_production):
        self.log_syntax_node("ReturnStmt") 
        self.depth += 1
        self.require_token('KEYWORD', 'return')
        self.attempt_parse_rule_with_recovery("ReturnStmtPrime", self.construct_ReturnStmtPrime)
        self.code_gen.save_return(self.lookahead_token)  # perform semantic action
        
        self.depth -= 1

    def construct_ReturnStmtPrime(self, use_empty_production):
        self.log_syntax_node("ReturnStmtPrime") 
        self.depth += 1
        # ReturnStmtPrime -> Expression ; | ;
        if self.lookahead_token[1] == ';' and self.lookahead_token[0] == 'SYMBOL':
            self.code_gen.push_index(self.lookahead_token)  # Semantic action: #push_index
            self.require_token('SYMBOL', ';')    
        elif self._is_token_in_rule_predict_set("Expression"): 
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token('SYMBOL', ';')
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing ReturnStmtPrime")
            self.require_token('SYMBOL', ';') 
        self.depth -= 1

    def construct_Expression(self, use_empty_production):
        self.log_syntax_node("Expression") 
        self.depth += 1
        # Expression -> SimpleExpressionZegond | ID B 
        if self._is_token_in_rule_predict_set("SimpleExpressionZegond"):
            self.attempt_parse_rule_with_recovery("SimpleExpressionZegond", self.construct_SimpleExpressionZegond)
        elif self.lookahead_token[0] == "ID":
            # --- FIX STARTS HERE ---
            id_token = self.lookahead_token  # 1. Save the current ID token
            self.require_token("ID")         # 2. Consume it (advances lookahead)
            self.code_gen.push_id_address(id_token) # 3. Call the action with the SAVED token
            # --- FIX ENDS HERE ---
            self.attempt_parse_rule_with_recovery("B", self.construct_B)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Expression")
        self.depth -= 1

    def construct_B(self, use_empty_production):
        self.log_syntax_node("B") 
        self.depth += 1
        if self.lookahead_token[1] == "=" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "=")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.code_gen.assign_operation(self.lookahead_token)  # Semantic action: #assign_operation
        elif self.lookahead_token[1] == "[" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "[")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", "]")
            self.code_gen.array_index(self.lookahead_token)  # Semantic action: #array_index
            self.attempt_parse_rule_with_recovery("H", self.construct_H)
        elif self._is_token_in_rule_predict_set("SimpleExpressionPrime") or \
             self._can_rule_be_empty_and_synced("SimpleExpressionPrime"): 
            self.attempt_parse_rule_with_recovery("SimpleExpressionPrime", self.construct_SimpleExpressionPrime)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing B")
        self.depth -= 1

    def construct_H(self, use_empty_production):
        self.log_syntax_node("H") 
        self.depth += 1
        if self.lookahead_token[1] == "=" and self.lookahead_token[0] == 'SYMBOL': 
            self.require_token("SYMBOL", "=")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.code_gen.assign_operation(self.lookahead_token)  # Semantic action: #assign_operation
        elif self._is_token_in_rule_predict_set("G") or \
             ("epsilon" in self.firsts.get("G",{})) and self._is_token_in_rule_predict_set("D") or \
             ("epsilon" in self.firsts.get("G",{})) and ("epsilon" in self.firsts.get("D",{})) and self._is_token_in_rule_predict_set("C") or \
             self._can_rule_be_empty_and_synced("G"): 
            self.attempt_parse_rule_with_recovery("G", self.construct_G)
            self.attempt_parse_rule_with_recovery("D", self.construct_D)
            self.attempt_parse_rule_with_recovery("C", self.construct_C)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing H")
        self.depth -= 1

    def construct_SimpleExpressionZegond(self, use_empty_production):
        self.log_syntax_node("SimpleExpressionZegond") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("AdditiveExpressionZegond", self.construct_AdditiveExpressionZegond)
        self.attempt_parse_rule_with_recovery("C", self.construct_C)
        self.depth -= 1

    def construct_SimpleExpressionPrime(self, use_empty_production):
        self.log_syntax_node("SimpleExpressionPrime") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("AdditiveExpressionPrime", self.construct_AdditiveExpressionPrime)
        self.attempt_parse_rule_with_recovery("C", self.construct_C)
        self.depth -= 1

    def construct_C(self, use_empty_production):
        self.log_syntax_node("C") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.code_gen.push_operator(self.lookahead_token)  # Semantic action: #push_operator
            self.attempt_parse_rule_with_recovery("Relop", self.construct_Relop)
            self.attempt_parse_rule_with_recovery("AdditiveExpression", self.construct_AdditiveExpression)
            self.code_gen.save_operation(self.lookahead_token)  # Semantic action: #save_operation

        self.depth -= 1

    def construct_Relop(self, use_empty_production):
        self.log_syntax_node("Relop") 
        self.depth += 1
        if self.lookahead_token[1] == "<" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "<")
        elif self.lookahead_token[1] == "==" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "==")
        else:
            # Error logged by require_token if none match.
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Relop")
        self.depth -= 1   

    def construct_AdditiveExpression(self, use_empty_production):
        self.log_syntax_node("AdditiveExpression") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("Term", self.construct_Term)
        self.attempt_parse_rule_with_recovery("D", self.construct_D)
        self.depth -= 1

    def construct_AdditiveExpressionPrime(self, use_empty_production):
        self.log_syntax_node("AdditiveExpressionPrime") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("TermPrime", self.construct_TermPrime)
        self.attempt_parse_rule_with_recovery("D", self.construct_D)
        self.depth -= 1

    def construct_AdditiveExpressionZegond(self, use_empty_production):
        self.log_syntax_node("AdditiveExpressionZegond") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("TermZegond", self.construct_TermZegond)
        self.attempt_parse_rule_with_recovery("D", self.construct_D)
        self.depth -= 1

    def construct_D(self, use_empty_production):
        self.log_syntax_node("D") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.code_gen.push_operator(self.lookahead_token)  # Semantic action: #push_operator
            self.attempt_parse_rule_with_recovery("Addop", self.construct_Addop)
            self.attempt_parse_rule_with_recovery("Term", self.construct_Term)
            self.code_gen.save_operation(self.lookahead_token)  # Semantic action: #save_operation
            self.attempt_parse_rule_with_recovery("D", self.construct_D) 
        self.depth -= 1

    def construct_Addop(self, use_empty_production):
        self.log_syntax_node("Addop") 
        self.depth += 1
        if self.lookahead_token[1] == '+' and self.lookahead_token[0] == 'SYMBOL':
             self.require_token('SYMBOL', '+')
        elif self.lookahead_token[1] == '-' and self.lookahead_token[0] == 'SYMBOL':
             self.require_token('SYMBOL', '-')
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Addop")
        self.depth -= 1

    def construct_Term(self, use_empty_production):
        self.log_syntax_node("Term") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("SignedFactor", self.construct_SignedFactor)
        self.attempt_parse_rule_with_recovery("G", self.construct_G)
        self.depth -= 1

    def construct_TermPrime(self, use_empty_production):
        self.log_syntax_node("TermPrime") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("SignedFactorPrime", self.construct_SignedFactorPrime)
        self.attempt_parse_rule_with_recovery("G", self.construct_G)
        self.depth -= 1

    def construct_TermZegond(self, use_empty_production):
        self.log_syntax_node("TermZegond") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("SignedFactorZegond", self.construct_SignedFactorZegond)
        self.attempt_parse_rule_with_recovery("G", self.construct_G)
        self.depth -= 1

    def construct_G(self, use_empty_production):
        self.log_syntax_node("G") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "*")
            self.attempt_parse_rule_with_recovery("SignedFactor", self.construct_SignedFactor)
            self.code_gen.multiply(self.lookahead_token)
            self.attempt_parse_rule_with_recovery("G", self.construct_G) 
        self.depth -= 1   

    def construct_SignedFactor(self, use_empty_production):
        self.log_syntax_node("SignedFactor") 
        self.depth += 1
        if (self.lookahead_token[1] == '+' or self.lookahead_token[1] == '-') and \
            self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", self.lookahead_token[1]) 
            self.attempt_parse_rule_with_recovery("Factor", self.construct_Factor)
            if self.lookahead_token[1] == '-':
                self.code_gen.negate_factor(self.lookahead_token)
        elif self._is_token_in_rule_predict_set("Factor"): 
            self.attempt_parse_rule_with_recovery("Factor", self.construct_Factor)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing SignedFactor")
        self.depth -= 1

    def construct_SignedFactorPrime(self, use_empty_production):
        self.log_syntax_node("SignedFactorPrime") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("FactorPrime", self.construct_FactorPrime)
        self.depth -= 1

    def construct_SignedFactorZegond(self, use_empty_production):
        self.log_syntax_node("SignedFactorZegond") 
        self.depth += 1
        if (self.lookahead_token[1] == '+' or self.lookahead_token[1] == '-') and \
           self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", self.lookahead_token[1])
            self.attempt_parse_rule_with_recovery("FactorZegond", self.construct_FactorZegond) # TODO IS IT OK??? 
            if self.lookahead_token[1] == '-':
                self.code_gen.negate_factor(self.lookahead_token)
        elif self._is_token_in_rule_predict_set("FactorZegond"): 
            self.attempt_parse_rule_with_recovery("FactorZegond", self.construct_FactorZegond)
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing SignedFactorZegond")
        self.depth -= 1

    def construct_Factor(self, use_empty_production):
        self.log_syntax_node("Factor") 
        self.depth += 1
        if self.lookahead_token[1] == "(" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", ")") 
        elif self.lookahead_token[0] == "ID":
            id_token = self.lookahead_token
            self.require_token("ID")
            self.code_gen.push_id_address(id_token)
            self.attempt_parse_rule_with_recovery("VarCallPrime", self.construct_VarCallPrime)
        elif self.lookahead_token[0] == "NUM":
            num_token = self.lookahead_token
            self.require_token("NUM")
            self.code_gen.push_num(num_token[1])
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing Factor")
        self.depth -= 1

    def construct_VarCallPrime(self, use_empty_production):
        self.log_syntax_node("VarCallPrime") 
        self.depth += 1

        token_kind, token_lexeme , _ = self.lookahead_token

        if token_lexeme == '(' and token_kind == 'SYMBOL':
            # Path: VarCallPrime -> ( Args )
            # This corresponds to the original: if self.current_token[1] == "(":
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Args", self.construct_Args)
            self.code_gen.implicit_output(self.lookahead_token)
            self.require_token("SYMBOL", ")")
            self.code_gen.call_function(self.lookahead_token)
        elif self._is_token_in_rule_predict_set("VarPrime") or \
             self._can_rule_be_empty_and_synced("VarPrime"):

            self.attempt_parse_rule_with_recovery("VarPrime", self.construct_VarPrime)
        else:
            self.syntax_error_list.append(
                f"#{self.token_provider.line_number + 1} : syntax error, missing VarCallPrime"
            )

        self.depth -= 1


    def construct_VarPrime(self, use_empty_production): 
        self.log_syntax_node("VarPrime") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "[")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", "]")
            self.code_gen.array_index(self.lookahead_token)
        self.depth -= 1    

    def construct_FactorPrime(self, use_empty_production): 
        self.log_syntax_node("FactorPrime") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Args", self.construct_Args)
            self.code_gen.implicit_output(self.lookahead_token)
            self.require_token("SYMBOL", ")")
            self.code_gen.call_function(self.lookahead_token)
        self.depth -= 1

    def construct_FactorZegond(self, use_empty_production):
        self.log_syntax_node("FactorZegond") 
        self.depth += 1
        if self.lookahead_token[1] == "(" and self.lookahead_token[0] == 'SYMBOL':
            self.require_token("SYMBOL", "(")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.require_token("SYMBOL", ")")
        elif self.lookahead_token[0] == "NUM":
            self.code_gen.push_num(self.lookahead_token[1])
            self.require_token("NUM")
        else:
            self.syntax_error_list.append(f"#{self.token_provider.line_number + 1} : syntax error, missing FactorZegond")
        self.depth -= 1

    def construct_Args(self, use_empty_production):
        self.log_syntax_node("Args") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.attempt_parse_rule_with_recovery("ArgList", self.construct_ArgList)
        self.depth -= 1

    def construct_ArgList(self, use_empty_production):
        self.log_syntax_node("ArgList") 
        self.depth += 1
        self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
        self.attempt_parse_rule_with_recovery("ArgListPrime", self.construct_ArgListPrime)
        self.depth -= 1
        
    def construct_ArgListPrime(self, use_empty_production):
        self.log_syntax_node("ArgListPrime") 
        self.depth += 1
        if use_empty_production or self.attempt_empty_production_next:
            self.log_syntax_node("epsilon") 
            self.attempt_empty_production_next = False
        else: 
            self.require_token("SYMBOL", ",")
            self.attempt_parse_rule_with_recovery("Expression", self.construct_Expression)
            self.attempt_parse_rule_with_recovery("ArgListPrime", self.construct_ArgListPrime)
        self.depth -= 1

def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    scanner = Scanner(lines)
    parser = Parser(scanner)
    parser.begin_syntax_analysis()



if __name__ == "__main__":
    main()