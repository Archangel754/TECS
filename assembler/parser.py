### Contains the parser module for the assembler for the Hack Computer TECS ###

class Parser():
    # takes a asm file name when initialized. returns object with attributes
    # relating to current command and can be stepped through the asm file.
    def __init__(self,input_file_name):
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
        #check for empty file
        if len(self.lines) < 1:
            raise ValueError('assembly file is empty')
        print(self.lines)
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
            raise ValueError('Tried to force parser advance beyond last command in file.')
        self.current_command = self.lines[self.current_index]
        
    def command_type(self):
        # checks command type of current command.
        # First symbol will be one of '(','@',other
        first_char = self.current_command[0]
        if first_char == '(':
            return 'L_COMMAND'
        elif first_char == '@':
            return 'A_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        # returns 'Xxx' for @Xxx or (Xxx) command
        if self.current_command[0] == '(':
            return self.current_command.rstrip()[1:-1]
        elif self.current_command[0] == '@':
            return self.current_command.rstrip()[1:]
        else:
            raise ValueError('inappropriate call of parser.symbol')

    def dest(self):
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        else:
            raise ValueError('inappropriate call of parser.dest')
        
    def comp(self):
        if '=' in self.current_command:
            return self.current_command.split('=')[1]
        elif ';' in self.current_command:
            return self.current_command.split(';')[0]
        else:
            raise ValueError('inappropriate call of parser.comp')

    def jump(self):
        if ';' in self.current_command:
            return self.current_command.split(';')[1]
        elif '=' in self.current_command:
            return 'null'
        
        else:
            raise ValueError('inappropriate call of parser.jump')
