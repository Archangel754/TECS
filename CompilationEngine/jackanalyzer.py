#!/usr/bin/env python3.10

# Takes a .jack  file or folder of same as command line argument and
# converts it to .xml files in the same directory.
# Tested on python 3.10.0

def jack_analyzer_main(filename):
    from jacktokenizer import JackTokenizer
    from compilationengine import CompilationEngine
    from vmwriter import VMWriter
    import os
    #handle directory or .vm file
    if os.path.isdir(filename):
        if filename[-1] == '/':
            base_name = filename[:-1]
        else:
            base_name = filename
            filename += '/'
        
        # make jackfilelist a list of all .jack files in directory:
        jackfilelist = []
        # walk the directory recursively and add only file names to vmfilelist:
        for (dirpath, dirnames,insidefilenames) in os.walk(filename):
            jackfilelist.extend(os.path.join(dirpath,insidefilename) for insidefilename in insidefilenames)
        #base_name = filename # for output file name
        
    else:
        jackfilelist = [filename]
        base_name = filename[:filename.find('.jack')]
    
    for jackfile in [jfile for jfile in jackfilelist if jfile[-5:] == '.jack']:
        print(f"Coding {jackfile}.")
        output_line_list = []
        tokenizer = JackTokenizer(jackfile)
        vmwriter = VMWriter()
        #for item in tokenizer.tokens_list:
        #    print(item)
        compilation_engine = CompilationEngine(tokenizer, vmwriter, output_line_list)
        # generate output_line_list
        if tokenizer.current_token == 'class':
            compilation_engine.compile_class()
        else:
            raise SyntaxError(f'File does not start with class: {tokenizer.current_token}')
        # Generate output name
        stripped_file_name = os.path.basename(jackfile)[:-5] # get rid of folders,slashes,extensions
        output_file_name = stripped_file_name + 'm.xml'
        output_vm_file_name = jackfile[:-5] + '.vm'
        
        # print vm code
        # vmwriter.print_vm_code()

        # Write output xml file
        #with open(output_file_name,'w') as outfile:
        #    outfile.write('\n'.join(output_line_list))

        # Write output vm file
        output_vm_list = vmwriter.get_output_list()
        with open(output_vm_file_name,'w') as outfile:
            outfile.write('\n'.join(output_vm_list))



if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        raise ValueError('No input file given.')
    else:
        filearg = sys.argv[1]

    jack_analyzer_main(filearg)
