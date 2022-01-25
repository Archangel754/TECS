# Implements the symbol table module for the TECS assembler.

class AssemblerSymbolTable():
    def __init__(self, assembler_map_init = False):
        self.symbol_table = {}
        # Optionally initialize with standard values for HACK Assembler:
        if assembler_map_init == True:
            amap = {'SP':0,
                        'LCL':1,
                        'ARG':2,
                        'THIS':3,
                        'THAT':4,
                        'SCREEN':16384,
                        'KBD':24576
                        }
            for i in range(0,16):
                amap[('R'+str(i))] = i
            self.symbol_table.update(amap)

    def add_entry(self, symbol, address):
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        return (symbol in self.symbol_table)
    
    def get_address(self, symbol):
        return self.symbol_table[symbol] # this is an int

    def print_table(self):
        print(self.symbol_table)
