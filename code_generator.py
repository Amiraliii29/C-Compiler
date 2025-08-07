class CodeGen:
    def __init__(self):
        self.semantic_stack = []
        self.output = []  
        self.temp_counter = 0
        self.label_counter = 0
        self.index = 0

        self.saved_type = None
        self.current_scope = 'global'  # Default scope

        # Our real symbol table: [(name, type, address, scope)]
        self.symbol_table = []

    def get_temp(self):
        temp = f"T{self.temp_counter}"
        self.temp_counter += 1
        return temp

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
        self.push(lexeme)    

    def define_variable(self, lookahead=None):
        var_id = self.pop()
        # self.void_check(var_id)

        address = self.get_temp()
        self.insert_code('ASSIGN', '#0', address)

        self.symbol_table.append((var_id, self.saved_type, address, self.current_scope))
    

    def define_array(self, lookahead=None):
        array_size = int(self.pop())
        array_id = self.pop()
        # self.void_check(array_id)

        address = self.get_temp()
        self.insert_code('ASSIGN', f'#{array_size}', address)

        self.symbol_table.append((array_id, f'{self.saved_type}[]', address, self.current_scope))


    def void_check(self, name):
        if self.saved_type == 'void':
            print(f"[Semantic Error] Cannot declare variable '{name}' of type void")
