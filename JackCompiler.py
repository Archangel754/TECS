#!/usr/bin/env python3.10

# Takes a folder of .jack files as command line argument and
# compiles it to .vm files in the same directory. VM files are then
# compiled into one .asm assembly file in same directory as folder.
# Assembly file is then compiled into one .hack machinde code file.
# .vm files for OS operations should be copied into folder containing
# .jack files before compilation so that they will be included in
# assembly.
# Tested on python 3.10.0

def jack_compiler_main(filename):
    """
    Compiles .jack file (filename) or files into .HACK machine code.
    If filename is folder, compiles all .jack files within. OS .vm files
    should be placed in the same directory so they are included in the 
    .asm file.
    """
    import sys
    from CompilationEngine.jackanalyzer import jack_analyzer_main
    from Assembler.assembler import assembler_main
    from VMtranslator.VMtranslator import VMtranslator_main
    sys.path.append('.')
    sys.path.insert(0,'./CompilationEngine')
    sys.path.insert(0,'./VMtranslator')
    sys.path.insert(0,'./Assembler')
    # Compile from .jack to .vm files:
    jack_analyzer_main(filename)
    # Compile from .vm files to one .asm assembly file:
    VMtranslator_main(filename)
    # Compile the single .asm file to .HACK machine code file:
    if filename[-1] == '/':
        filename = filename[:-1]
    asm_name = filename + '.asm'
    assembler_main(asm_name)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        raise ValueError('No input file given.')
    else:
        filearg = sys.argv[1]
    jack_compiler_main(filearg)
