
class VMCodeWriter():
    """Write a .asm file line by line.
    
    Takes a .asm file name when initialized.
    Returns object which provides functions for writing 
    assembly commands to file from vm code."""
    
    def __init__(self,output_file_name):
        # initialize the stack?
        # SP is SP special symbol in assembly so '@SP'
        # then implement logic to increment or decrement SP
        self.lines = []
        self.unique = 111
        self.uniquefunctionreturn = 222 # necessary for recursion or labels won't be unique
        self.output_file_name = output_file_name
        self.current_function_name = ''

    def set_file_name(self,current_vm_file_name):
        """Set name of the current .vm file. Used internally by VM."""
        self.current_vm_file_name = current_vm_file_name
        # will this add a label for each .vm file in assembly code later?

    ###################################### VMII ######################################
    # The following functions implement Ch 8
    # function handling: if, goto, labels, and subroutine calling.
    def write_init(self):
        """Generate assembly for VM initialization(bootstrap code). 
        Must go at the beginning of .asm file."""
        command_list = ["@256",
                            "D=A",
                            "@SP",
                            "M=D"] #R0/SP is now 256
        self.lines.extend(command_list)
        
        # call sys.init with setup:
        self.write_call(function_name='Sys.init', num_args=0)
        # Answers were misaligned with tests. Spec and tests expect
        # Sys.init to be called like a regular funtion.
        # These values were expected on the stack since sys.init never
        # finishes running. Really though, these shouldn't be necessary since
        # sys.init never returns to anything. (instead of @Sys.init, 0;JMP)

        
        # do LCL, ARG, THIS, THAT need to be initialized here?
       # should follow same stack setup format as write_call()?

    def write_label(self,label):
        """Writes assembly for label command."""
        self.lines.append(f"({self.current_function_name}${label})")

    def write_goto(self,label):
        """Writes assembly for goto command."""
        self.lines.extend([f"@{self.current_function_name}${label}",
                               "0;JMP"])

    def write_if(self,label):
        """Writes assembly for if-goto command."""
        self._gety() # pops top item from stack and puts in D
        self.lines.extend([f"@{self.current_function_name}${label}",
                               "D;JNE"]) # jump only if D != 0

    def write_call(self,function_name: str,num_args: int):
        """Writes assembly for call command. Must handle
        setting up the stack and built-ins(LCL,ARG, etc.) 
        for each routine."""
        # push return-address (seperately because value in A not M):
        self.lines.extend([f"@returnaddressfrom.{function_name}{self.uniquefunctionreturn}","D=A"])
        self._writeDtostack()
        
        # push LCL, ARG, THIS, THAT:
        to_push = ["@LCL","@ARG","@THIS","@THAT"]
        for item in to_push:
            self.lines.extend([item,"D=M"])
            self._writeDtostack()
            
        # ARG = SP-num_args-5:
        arg_command_list = ["@SP",
                            "D=M",# value of SP in D
                            f"@{num_args+5}",
                            "D=D-A",
                            "@ARG",
                            "M=D"] # ARG now set to SP-(num_args+5)
        self.lines.extend(arg_command_list)
        
        # LCL = SP:
        lcl_command_list = ["@SP",
                                "D=M", # value of SP in D
                                "@LCL",
                                "M=D"] # LCL set to SP value
        self.lines.extend(lcl_command_list)
        
        # goto function_name:
        self.lines.append(f"@{function_name}")
        self.lines.append("0;JMP")
        
        # label for return address:
        self.lines.append(f"(returnaddressfrom.{function_name}{self.uniquefunctionreturn})")

        # increment unique pattern for next call
        # necessary for recursive calls.
        self.uniquefunctionreturn += 1
        
    def write_return(self):
        """Writes assembly for call command. Must handle
        restoring the stack and built-ins(LCL,ARG, etc.) 
        for the calling(outer) routine."""

        # set LCL address to temp var FRAME: 
        command_list = ["@LCL",
                            "D=M", # was D=A                                             **
                            "@FRAME",
                            "M=D"] # FRAME is set to address of LCL
        self.lines.extend(command_list)


        # RET = contents of FRAME-5
        # Setting RET as temp variable for return-address is necessary,
        # otherwise replacing ARG later will overwrite return-address
        # inside the calling function's frame.
        self.lines.extend(["@FRAME",
                               "A=M-1", #A = (FRAME-1)
                               "A=A-1", #A = (FRAME-2)
                               "A=A-1", #A = (FRAME-3)
                               "A=A-1", #A = (FRAME-4)
                               "A=A-1", #A = (FRAME-5)
                               "D=M", # D = contents of FRAME-5 = return address
                               "@RET", # variable RET
                               "M=D"]) # RET = return-address
        
        # pop y from stack and place at ARG M
        self._gety() # return value now in D
        self.lines.extend(["@ARG",
                               "A=M",     # added because set value at ARG not set ARG    **
                               "M=D"])

        # set SP to ARG + 1
        self.lines.extend(["@ARG",
                               "D=M+1", # was D=A+1 changed M is address of ARG, A is just 2   **
                               "@SP",
                               "M=D"])

        # set THAT to contents of (FRAME-1)
        self.lines.extend(["@FRAME",
                               "A=M-1", # A = (FRAME-1)
                               "D=M", # D = contents of FRAME-1
                               "@THAT",
                               "M=D" ]) #THAT = contents of FRAME-1

        # set THIS to contents of (FRAME-2)
        self.lines.extend(["@FRAME",
                               "A=M-1", #A = (FRAME-1)
                               "A=A-1", #A = (FRAME-2)
                               "D=M", # D = contents of FRAME-1
                               "@THIS",
                               "M=D" ]) #THIS = contents of FRAME-2

        # set ARG to contents of (FRAME-3)
        self.lines.extend(["@FRAME",
                               "A=M-1", #A = (FRAME-1)
                               "A=A-1", #A = (FRAME-2)
                               "A=A-1", #A = (FRAME-3)
                               "D=M", # D = contents of FRAME-3
                               "@ARG",
                               "M=D" ]) #ARG = contents of FRAME-3
                            
        # set LCL to contents of (FRAME-4)
        self.lines.extend(["@FRAME",
                               "A=M-1", #A = (FRAME-1)
                               "A=A-1", #A = (FRAME-2)
                               "A=A-1", #A = (FRAME-3)
                               "A=A-1", #A = (FRAME-4)
                               "D=M", # D = contents of FRAME-4
                               "@LCL",
                               "M=D" ]) #LCL = contents of FRAME-4

        # set A to contents of (FRAME-5) and jump to it (return address of calling function)
        self.lines.extend(["@RET",
                               "A=M", #A = contents of RET = return-address
                               "0;JMP"]) # jump to return address of calling function
        
    def write_function(self,function_name: str,num_locals: int):
        """Writes assembly for the beginning of a new function.
        Should include function label, etc.."""
        # save the name (used by write_label,write_if,write_goto):
        self.current_function_name = function_name 
        # Add label for beginning of function:
        self.lines.append(f"({function_name})")
        # Initialize num_locals number of variables to
        # stack with value of 0:
        for i in range(num_locals):
            self.write_push_pop('push','constant', 0)

    ##################################################################################

    def write_arithmetic(self,command: str):
        """Take the top one/two things off of the stack,
        place them in A,D,M as appropriate. Perform the 
        selected operation. Then move result from D
        onto the top of the stack."""
        # add a comment:
        self.lines.append(f"// write_arithmetic:{command}:")
        match command:
            # all cases should put result in D, which is pushed to stack after match statement.
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
        """Write assembly for push and pop commands."""
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
        """Writes generated lines to file.
        Call once when finished with other commands."""
        # write self.lines to self.outfilename.
        with open(self.output_file_name,'w') as outfile:
            outfile.write('\n'.join(self.lines))
        
    def _writeDtostack(self):
        """Write assembly for pushing contents
        of D register to stack."""
        command_string = ["//place result(D) into top of stack:",
                              "@SP",
                              "A=M",
                              "M=D",
                              "//inc stack pointer:",
                              "@SP",
                              "M=M+1"]
        self.lines.extend(command_string)
                              
    def _getxandy(self):
        """Use SP to get x and y from stack and place
        them in A and D respectively."""
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
        """Use SP to get y from stack and place
        it in D."""
        command_string = ["//get y put y in D:",
                              "@SP",
                              "A = M",
                              "A=A-1",
                              "D = M",
                              "// dec SP once:",
                              "@SP",
                              "M = M-1",]
        self.lines.extend(command_string)

    def write_comment(self, comment_str):
        """Place a comment in the output stream file."""
        self.lines.append(f"//{comment_str}")
