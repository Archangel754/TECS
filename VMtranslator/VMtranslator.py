#!/usr/bin/env python3.10

# Takes a .vm assembly file or folder of same as command line argument and
# converts it to a .asm file in the same directory, which is
# written in assembly to run on the HACK Computer(TECS).
# Will be tested on python 3.10.0
# first version will only work on one file

def VMtranslator_main(filename):
    from vmcodewriter import VMCodeWriter
    from vmparser import VMParser
    import os
    #handle directory or .vm file
    if os.path.isdir(filename):
        if filename[-1] == '/':
            base_name = filename[:-1]
        else:
            base_name = filename
            filename += '/'
        
        # make vmfilelist a list of all .vm files in directory:
        vmfilelist = []
        # walk the directory recursively and add only file names to vmfilelist:
        for (dirpath, dirnames,insidefilenames) in os.walk(filename):
            vmfilelist.extend(os.path.join(dirpath,insidefilename) for insidefilename in insidefilenames)
        #print(vmfilelist)
        #base_name = filename # for output file name
        #print('base_name: ',base_name)
        
    else:
        vmfilelist = [filename]
        base_name = filename[:filename.find('.vm')]

    
    # set output file name and initialize writer:
    asm_name = base_name + '.asm'
    writer = VMCodeWriter(asm_name)

    for vmfile in [vfile for vfile in vmfilelist if vfile[-3:] == '.vm']: # will change for multiple files
        parser = VMParser(vmfile) # change to loop over files
        writer.set_file_name(vmfile[:-3]) # doesn't really do anything yet.may add label later.
        finished = False
        while finished == False:
            if parser.has_more_commands() == False:
                finished = True
            # Deal with translating current command line:
            ctype = parser.command_type()
            match ctype:
                case 'C_ARITHMETIC':
                    writer.write_arithmetic(command = parser.current_command) # 'add', 'eq', etc.
                case 'C_PUSH':
                    writer.write_push_pop(command = 'push', segment = parser.arg1(), index = parser.arg2())
                case 'C_POP':
                    writer.write_push_pop(command = 'pop', segment = parser.arg1(), index = parser.arg2())
                # other cases to add here soon


            if parser.has_more_commands() == True:
                parser.advance()
    writer.close()





if __name__ == '__main__':
    import sys
    filearg = sys.argv[1]
    VMtranslator_main(filearg)
