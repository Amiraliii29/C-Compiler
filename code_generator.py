class CodeGen:
    def __init__(self):
        self.semantic_stack = []
        self.output = []  # Store code lines here if needed
        self.temp_counter = 0
        self.label_counter = 0
        self.index = 0

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

    

