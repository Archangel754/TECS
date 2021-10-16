
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
        # add a comment:
        self.lines.append(f"// write_arithmetic:{command}:")
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
        # add a comment:
        self.lines.append(f"// write_push_pop:{command} {segment} {index}:")
        # implement push constant x:
        match command:
            case 'push':
                match segment:
                    case 'constant':
                        # index is the number to push onto the stack
                        # (this string of commands has been tested in assembler)
                        command_string = ["@" + str(index),
                                              "D=A", # value to push to stack is now in D
                                              ]
                    case ('local' | 'argument' | 'this' | 'that') as segment:
                        seg_dict = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}
                        command_string = [f"@{seg_dict[segment]}",
                                              "D=M", #D is the address of base of segment
                                              f"@{str(index)}",
                                              "A=D+A", #A is now address of segment(base+index)
                                              "D=M", # value to push to stack is now in D
                                              ]
                    case ('pointer' | 'temp') as segment:
                        seg_dict = {'pointer':3,'temp':5}
                        command_string = [f"@{str(seg_dict[segment]+index)}",
                                              "D=M" #D is the contents of address: pointer i or temp i
                                              ]
                    case 'static':
                        var_name = f'{self.current_vm_file_name}.{str(index)}'
                        command_string = [f"@{var_name}",
                                              "D=M" #value of static[index] to push to stack is now in D
                                              ]
                                              
                # now push D onto stack
                command_string.extend(["@SP",
                                           "A=M // A now points to top of stack",
                                           "M=D",
                                           "// now inc stack pointer:",
                                           "@SP",
                                           "M=M+1"])
            case 'pop':
                #print('found a pop',command,segment,index)
                match segment:
                    # get segment address
                    # get base + i address put in D
                    # pop something off stack into A
                    case ('local' | 'argument' | 'this' | 'that') as segment:
                        seg_dict = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}
                        command_string = [f"@{seg_dict[segment]}",
                                              "D=M", #D is the address of base of local
                                              f"@{str(index)}",
                                              "A=D+A", #A is now address of segment(base+index)
                                              "D=A",
                                              "@R13",
                                              "M=D", #Storing address temporarily in R13
                                              "//get something from stack:",
                                              "@SP",
                                              "A=M // A now points to top of stack",
                                              "A=A-1 // A points to topmost item on stack",
                                              "D=M", # D holds item popped from stack
                                              "@SP",
                                              "M=M-1", # decrement the stack pointer
                                              "@R13", 
                                              "A=M", # A is now address to pop stack to
                                              "M=D" # item popped from stack is put in segment[index]
                                              ]
                    case ('pointer' | 'temp') as segment:
                        seg_dict = {'pointer':3,'temp':5}
                        command_string = ["//get something from stack:",
                                              "@SP",
                                              "A=M // A now points to top of stack",
                                              "A=A-1 // A points to topmost item on stack",
                                              "D=M", # D holds item popped from stack
                                              "@SP",
                                              "M=M-1", # decrement the stack pointer
                                              f"@{str(seg_dict[segment]+index)}", # address to pop stack to
                                              "M=D" # item popped from stack is put in segment[index]
                                              ]
                    case 'static':
                        var_name = f'{self.current_vm_file_name}.{str(index)}'
                        command_string = ["//get something from stack:",
                                              "@SP",
                                              "A=M // A now points to top of stack",
                                              "A=A-1 // A points to topmost item on stack",
                                              "D=M", # D holds item popped from stack
                                              "@SP",
                                              "M=M-1", # decrement the stack pointer
                                              f"@{var_name}",
                                              "M=D" #value of static[index] set to value popped from stack
                                              ]
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


