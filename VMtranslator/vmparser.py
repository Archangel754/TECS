### Contains the VM parser module for the assembler for the Hack Computer TECS ###


# TODO:
# arg1
# arg2
# command type

class VMParser():
    # takes a .vm file name when initialized. returns object with attributes
    # relating to current command and can be stepped through the vm file.
    def __init__(self,input_file_name):
        #from symbol_table import AssemblerSymbolTable

        self.lines = []
        with open(input_file_name, 'r') as file:
            for line in file:
                if '//' in line:
                    comment_index = line.find('//')
                    stripped_line = line[:comment_index].strip()
                else:
                    stripped_line = line.strip()
                if len(stripped_line) > 0:
                    self.lines.append(stripped_line)
        #check for empty file:
        if len(self.lines) < 1:
            raise ValueError('VM file is empty')
        #print(self.lines)

        # Initialize a symbol table and do first pass of assembly to:
        # 1. add labels to symbol table
        # 2. remove labels from list of instructions
        # self.sym_table = AssemblerSymbolTable(assembler_map_init = True)
        # counter = 0
        # newlines = []
        # for line in self.lines:
        #     if line[0] == '(':
        #         #add label to symbol table and remove line
        #         self.sym_table.add_entry(line[1:-1],counter)
        #     else:
        #         newlines.append(line)
        #         counter += 1
        # self.lines = newlines

        #testing:
        #print('inputfile:',input_file_name)
        #print(self.lines)
        
        # Attributes:
        self.current_index = 0
        self.current_command = self.lines[self.current_index]
        self.max_index = len(self.lines) - 1
        

        
    def has_more_commands(self):
        if self.current_index < self.max_index:
            return True
        else:
            return False

    def advance(self):
        # advances to next command in list
        self.current_index += 1
        if self.current_index > self.max_index:
            raise ValueError('Tried to force vmparser advance beyond last command in file.')
        self.current_command = self.lines[self.current_index]
        
    def command_type(self) -> str:
#       """Returns command type of current command. First word of line is used."""
        command_type = {'add':'C_ARITHMETIC',
                            'sub':'C_ARITHMETIC',
                            'neg':'C_ARITHMETIC',
                            'eq':'C_ARITHMETIC',
                            'gt':'C_ARITHMETIC',
                            'lt':'C_ARITHMETIC',
                            'and':'C_ARITHMETIC',
                            'or':'C_ARITHMETIC',
                            'not':'C_ARITHMETIC',
                            'push':'C_PUSH',
                            'pop':'C_POP',
                            'label':'C_LABEL',
                            'goto':'C_GOTO',
                            'if-goto':'C_IF',
                            'function':'C_FUNCTION',
                            'return':'C_RETURN',
                            'call':'C_CALL',
            }
        command = self.current_command.split(' ')[0]
        return command_type[command]

    def arg1(self) -> str:
        if self.command_type() == 'C_ARITHMETIC':
            command = self.current_command.split(' ')[0]
        else:
            command = self.current_command.split(' ')[1]
        return command

    def arg2(self) -> int:
        arg2 = self.current_command.split(' ')[2]
        #print(self.current_command)
        #print(arg2)
        return int(arg2)
        
