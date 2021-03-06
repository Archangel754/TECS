#!/usr/bin/env python3.10

# Takes a .jack  file or folder of same as command line argument and
# converts it to .xml files in the same directory.
# Tested on python 3.10.0

def jack_analyzer_main(filename):
    """
    Compiles .jack file (filename) into .vm file.
    If filename is folder, compiles all .jack files within.
    """
    from jacktokenizer import JackTokenizer
    from compilationengine import CompilationEngine
    from vmwriter import VMWriter
    import os
    # Handle directory or .vm file:
    if os.path.isdir(filename):
        # Make jackfilelist a list of all .jack files in directory:
        jackfilelist = []
        # Walk the directory recursively and add only file names to vmfilelist:
        for (dirpath, dirnames,insidefilenames) in os.walk(filename):
            jackfilelist.extend(os.path.join(dirpath,insidefilename) for insidefilename in insidefilenames)
    else:
        jackfilelist = [filename]
    
    # Compile .jack files into .vm files:
    for jackfile in [jfile for jfile in jackfilelist if jfile[-5:] == '.jack']:
        print(f"Coding {jackfile}.")
        output_line_list = []
        tokenizer = JackTokenizer(jackfile)
        vmwriter = VMWriter()
        compilation_engine = CompilationEngine(tokenizer, vmwriter, output_line_list)

        # Generate output_line_list / compile jack code:
        if tokenizer.current_token == 'class':
            compilation_engine.compile_class()
        else:
            raise SyntaxError(f'File does not start with class: {tokenizer.current_token}')

        # Write output vm file:
        output_vm_file_name = jackfile[:-5] + '.vm'
        output_vm_list = vmwriter.get_output_list()
        with open(output_vm_file_name,'w') as outfile:
            outfile.write('\n'.join(output_vm_list))

        # Print vm code:
        # vmwriter.print_vm_code()

        # Write output xml file:
        # output_file_name = jackfile[:-5] + 'm.xml'
        # with open(output_file_name,'w') as outfile:
        #    outfile.write('\n'.join(output_line_list))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        raise ValueError('No input file given.')
    else:
        filearg = sys.argv[1]
    jack_analyzer_main(filearg)
