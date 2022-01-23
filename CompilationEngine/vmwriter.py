
class VMWriter:
    def __init__(self) -> None:
        """Initialize a new object for writing vm commands into vm code."""
        self.output_list = []
        
    def push(self, segment, idx):
        """Writes a VM push command."""
        if segment == 'var':
            segment = 'local'
        if segment == 'arg':
            segment = 'argument'
        if segment == 'field':
            segment = 'this'
        self.output_list.append(f'push {segment} {idx}')

    def pop(self, segment,idx):
        """Writes a VM pop command."""
        if segment == 'var':
            segment = 'local'
        if segment == 'arg':
            segment = 'argument'
        if segment == 'field':
            segment = 'this'
        self.output_list.append(f'pop {segment} {idx}')

    def arithmetic(self, command):
        """Writes VM arithmetic command(add, sub, neg, eq, gt, lt, and, or, not)."""
        self.output_list.append(command)

    def label(self, label):
        """Writes a VM label command."""
        self.output_list.append(f'label {label}')

    def goto(self, label):
        """Writes a VM goto command."""
        self.output_list.append(f'goto {label}')

    def if_goto(self, label):
        """Writes a VM if_goto command."""
        self.output_list.append(f'if-goto {label}')

    def call(self, name, nArgs):
        """Writes a VM call command."""
        self.output_list.append(f'call {name} {nArgs}')

    def function(self, name, nLocals):
        """Writes a VM function command."""
        self.output_list.append(f'function {name} {nLocals}')

    def ret(self):
        """Writes a VM return command."""
        self.output_list.append('return')

    def print_vm_code(self):
        """Prints VM code for debugging."""
        for line in self.output_list:
            print(line)
    
    def get_output_list(self):
        """Returns the output list for writing to file."""
        return self.output_list