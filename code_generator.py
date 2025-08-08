


class CodeGen:
    def __init__(self):
        self.semantic_stack = []
        self.return_stack = []
        self.break_stack = []
        self.output = []  
        self.temp_address = 500
        self.label_counter = 0
        self.index = 0
        self.operations_symbols = {'+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}

        self.saved_type = None
        self.current_scope = 0  # Default scope

        self.semantic_errors = []

        # Our real symbol table: [(name, type, address, scope)]
        self.symbol_table = []

    def get_temp(self, count=1):
        address = str(self.temp_address)
        for _ in range(count):
            self.insert_code('ASSIGN', '#0', str(self.temp_address))
            self.temp_address += 4
        return address
    
    def search_in_symbol_table(self, item, scope_num=0):
        # Search from latest to oldest (most recent declaration first)
        for record in reversed(self.symbol_table):
            name, typ, address, scope = record
            if item == name and scope <= scope_num:
                return address  # or return record if you want full info
        return False
    
    def find_address(self, item):
        if item == 'output':
            return item
        for record in reversed(self.symbol_table):
            if item == record[0]:
                return record[2]  # Return the address
        return None  # Or raise an error if needed

    def get_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
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
        # self.void_check(var_id)

        address = self.get_temp()
        self.insert_code('ASSIGN', '#0', address)

        self.symbol_table.append((var_id, 'int', address, self.current_scope))
    

    def define_array(self, lookahead=None):
        array_size = int(self.pop())
        array_id = self.pop()
        # self.void_check(array_id)

        address = self.get_temp()
        self.insert_code('ASSIGN', f'#{array_size}', address)

        self.symbol_table.append((array_id, 'int*', address, self.current_scope))

    def scope_check(self, lookahead):
        if self.search_in_symbol_table(lookahead[1], self.current_scope) or lookahead[1] == 'output':
            return
        self.semantic_errors.append(f'#{lookahead[0]} : Semantic Error! \'{lookahead[1]}\' is not defined.')

    def void_check(self, var_id):
        if self.id_type[2] == 'void':
            self.semantic_errors.append(f'#{self.id_type[0]} : Semantic Error! Illegal type of void for \'{var_id}\'.')

    def break_check(self, lookahead):
        if len(self.break_stack) > 0 and ['>>>' in self.break_stack]:
            return
        self.semantic_errors.append(
            f'#{lookahead[0]} : Semantic Error! No \'while\' or \'for\' found for \'break\'.')

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
                f'#{lookahead[0]} : Semantic Error! Type mismatch in operands, Got {operand_2_type} instead of {operand_1_type}.')    

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