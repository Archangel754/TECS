#!/usr/bin/python3

# Takes a .asm assembly file as command line argument and
# converts it to a .hack file in the same directory, which is
# written in machine language to run on the HACK Computer(TECS).
# Tested on both python 3.8.2 and 3.10.0

def assembler_main(filename):
    from parser import Parser
    from code import code
    
    # load parser object with assembly file
    asm = Parser(filename)

    # generate list of assembly commands:
    machine_code = []
    next_variable_loc = 16
    finished = False
    while finished == False:
        if asm.has_more_commands() == False:
            finished = True
        #print('is true')
        #print(asm.current_command)
        if asm.command_type() == 'A_COMMAND':
            
            # check if not a variable:
            if asm.symbol().isdecimal():
                machine_code.append ('0' + assembler_convert_to_15bit_bin(asm.symbol()))
            elif asm.sym_table.contains(asm.symbol()):
                # variable or label is alread in the table. set @ instr with value.
                loc_string = str(asm.sym_table.get_address(asm.symbol()))
                machine_code.append ('0' + assembler_convert_to_15bit_bin(loc_string))

            else:
                # variable hasn't been used. add it to table and set @ instr.
                asm.sym_table.add_entry(asm.symbol(),next_variable_loc)
                machine_code.append ('0' + assembler_convert_to_15bit_bin(str(next_variable_loc)))
                next_variable_loc += 1        
            
        elif asm.command_type() == 'C_COMMAND':
            command = []
            command.append('111')
            command.append(code(asm.comp(),'comp'))
            command.append(code(asm.dest(),'dest'))
            command.append(code(asm.jump(),'jump'))
            machine_code.append(''.join(command))
            
        elif asm.command_type() == 'L_COMMAND':
            raise ValueError('L commands should have been dealt with by parser.')
        
        if asm.has_more_commands() == True:
            asm.advance()

    # write the machine code to file with basename + .hack (overwrites)
    #print(machine_code)
    base_name = filename[:filename.find('.asm')]
    hack_name = base_name + '.hack'
    with open(hack_name,'w') as newfile:
        for code in machine_code:
            newfile.write(code)
            newfile.write('\n')

def assembler_convert_to_15bit_bin(number):
    # returns 15 bit binary string of input number which is a string
    binary_version = str(bin(int(number)))[2:]
    lead = '0' * (15 - len(binary_version))
    return lead + binary_version
    
if __name__ == '__main__':
    import sys
    filearg = sys.argv[1]
    assembler_main(filearg)
