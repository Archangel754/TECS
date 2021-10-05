#!/usr/bin/python3


def assembler_main(filename):
    from parser import Parser
    from code import code
    
    # load parser object with assembly file
    asm = Parser(filename)

    # generate list of assembly commands:
    machine_code = []
    while asm.has_more_commands() == True:
        #print('is true')
        #print(asm.current_command)
        if asm.command_type() == 'A_COMMAND':
            machine_code.append ('0' + assembler_convert_to_15bit_bin(asm.symbol()))
            
        elif asm.command_type() == 'C_COMMAND':
            command = []
            command.append('111')
            command.append(code(asm.comp(),'comp'))
            command.append(code(asm.dest(),'dest'))
            command.append(code(asm.jump(),'jump'))
            machine_code.append(''.join(command))
            
        elif asm.command_type() == 'L_COMMAND':
            pass
        asm.advance()

    # do the final line (because has more commands is false here):
    if asm.command_type() == 'A_COMMAND':
        machine_code.append ('0' + assembler_convert_to_15bit_bin(asm.symbol()))
            
    elif asm.command_type() == 'C_COMMAND':
        command = []
        command.append('111')
        command.append(code(asm.comp(),'comp'))
        command.append(code(asm.dest(),'dest'))
        command.append(code(asm.jump(),'jump'))
        machine_code.append(''.join(command))
            
    elif asm.command_type() == 'L_COMMAND':
        pass
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
