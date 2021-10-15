
class VMCodeWriter():
    """ Takes a .asm file name when initialized.
    Returns object which provides functions for writing 
    assembly commands to file from vm code. """
    def __init__(self,output_file_name):
        # initialize the stack?
        # SP is SP special symbol in assembly so '@SP'
        # then implement logic to increment or decrement SP
        self.lines = []
        self.unique = 111
        self.output_file_name = output_file_name

    def set_file_name(self,current_vm_file_name):
        self.current_vm_file_name = current_vm_file_name
        # will this add a label for each .vm file in assembly code later?

    def write_arithmetic(self,command: str):
        """ Take the top one/two things off of the stack,
        place them in A,D,M as appropriate. Perform the 
        selected operation. Then move result from D
        onto the top of the stack. """
        match command:
            #
            case 'add':
                self._getxandy() #A is x and D is y
                self.lines.append('D=A+D')
            case 'sub':
                self._getxandy() #A is x and D is y
                self.lines.append('D=A-D')
            case 'neg':
                self._gety() #y removed from stack and place in D
                self.lines.append('D=-D')
            case ('eq' | 'gt' | 'lt') as comparison: # all handled the same except first jump command
                comparators_dict = {'eq':'JEQ','gt':'JGT','lt':'JLT'}
                jump_command = comparators_dict[comparison]
                self._getxandy()
                command_string = ["D=A-D",
                                      f"@TRUE{str(self.unique)}",
                                      f"D;{jump_command}", # jump to (TRUE...) if x (== or < or >) y
                                      "D=0", # set D to false
                                      f"@CONTINUE{str(self.unique)}",
                                      "0;JMP", # goto continue to skip setting D to true
                                      f"(TRUE{str(self.unique)})",
                                      "D=-1",
                                      f"(CONTINUE{str(self.unique)})"]
                self.lines.extend(command_string)
                self.unique += 1
            case 'and':
                self._getxandy() #A is x and D is y
                self.lines.append('D=A&D')
            case 'or':
                self._getxandy() #A is x and D is y
                self.lines.append('D=A|D')
            case 'not':
                self._gety() #y removed from stack and place in D
                self.lines.append('D=!D')
        # push answer from any case to stack:
        self._writeDtostack()

    def write_push_pop(self,command: str, segment: str, index: int):
        # implement push constant x:
        match command:
            case 'push':
                match segment:
                    case 'constant':
                        # index is the number to push onto the stack
                        # (this string of commands has been tested in assembler)
                        command_string = ["@" + str(index),
                                              "D=A",
                                              "@SP",
                                              "A=M // A now points to top of stack",
                                              "M=D",
                                              "// now inc stack pointer:",
                                              "@SP",
                                              "M=M+1"]
        self.lines.extend(command_string)

    def close(self):
        # write self.lines to self.outfilename.
        with open(self.output_file_name,'w') as outfile:
            outfile.write('\n'.join(self.lines))
        
    def _writeDtostack(self):
        command_string = ["//place result(D) into top of stack:",
                              "@SP",
                              "A=M",
                              "M=D",
                              "//inc stack pointer:",
                              "@SP",
                              "M=M+1"]
        self.lines.extend(command_string)
                              
    def _getxandy(self):
        """ Uses SP to get x and y from stack and place
        them in A and D respectively. """
        command_string = ["//get y put y in D:",
                              "@SP",
                              "A = M",
                              "A=A-1",
                              "D = M",
                              "// dec SP twice:",
                              "@SP",
                              "M = M-1",
                              "M = M-1",
                              "// get x, put x in A:",
                              "A = M",
                              "A = M "]
        self.lines.extend(command_string)

    def _gety(self):
        """ Uses SP to y from stack and place
        it in D. """
        command_string = ["//get y put y in D:",
                              "@SP",
                              "A = M",
                              "A=A-1",
                              "D = M",
                              "// dec SP once:",
                              "@SP",
                              "M = M-1",]
        self.lines.extend(command_string)



""" Replaced code from match:
            case 'eq':
                self._getxandy()
                command_string = ["D=A-D",
                                      f"@TRUE{str(self.unique)}",
                                      "D;JEQ", # jump to (TRUE...) if x == y
                                      # f"(FALSE{str(self.unique)})", not needed
                                      "D=0", # set D to false
                                      f"@CONTINUE{str(self.unique)}",
                                      "0;JMP", # goto continue to skip setting D to true
                                      f"(TRUE{str(self.unique)})",
                                      "D=-1",
                                      f"(CONTINUE{str(self.unique)})"]
                self.lines.extend(command_string)
                self.unique += 1
                self._writeDtostack()

            case 'gt':
                self._getxandy()
                command_string = ["D=A-D",
                                      f"@TRUE{str(self.unique)}",
                                      "D;JGT", # jump to (TRUE...) if x > y
                                      # f"(FALSE{str(self.unique)})", not needed
                                      "D=0", # set D to false
                                      f"@CONTINUE{str(self.unique)}",
                                      "0;JMP", # goto continue to skip setting D to true
                                      f"(TRUE{str(self.unique)})",
                                      "D=-1",
                                      f"(CONTINUE{str(self.unique)})"]
                self.lines.extend(command_string)
                self.unique += 1
                self._writeDtostack()
            case 'lt':
                self._getxandy()
                command_string = ["D=A-D",
                                      f"@TRUE{str(self.unique)}",
                                      "D;JLT", # jump to (TRUE...) if x < y
                                      # f"(FALSE{str(self.unique)})", not needed
                                      "D=0", # set D to false
                                      f"@CONTINUE{str(self.unique)}", 
                                      "0;JMP", # goto continue to skip setting D to true
                                      f"(TRUE{str(self.unique)})",
                                      "D=-1",
                                      f"(CONTINUE{str(self.unique)})"]
                self.lines.extend(command_string)
                self.unique += 1
                self._writeDtostack()

"""
