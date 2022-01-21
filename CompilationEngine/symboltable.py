
class SymbolTable:
    """Provides access to class and subroutine scope symbol tables."""
    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # example: table = {symbolname:{'type':'int',kind:'static','index':0}}
        self.class_table = {}
        self.subroutine_table = {}
        self.__class_next_index__ = {'static':0,'field':0}
        self.__subroutine_next_index__ = {'arg':0,'var':0}

    def start_subroutine(self):
        """Start a new subroutine scope(reset subroutine symbol table)."""
        self.subroutine_table = {}
        self.__subroutine_next_index__ = {'arg':0,'var':0}

    def define(self, name, type, kind):
        """Define a new identifier, assign it running index."""
        # static, field identifiers -> class scope
        # arg, var identifiers -> subroutine scope
        match kind:
            case ('static' | 'field'):
                index = self.__class_next_index__[kind]
                self.class_table[name] = {'type':type,'kind':kind,'index':index}
                self.__class_next_index__[kind] += 1
            case ('arg' | 'var'):
                index = self.__subroutine_next_index__[kind]
                self.subroutine_table[name] = {'type':type,'kind':kind,'index':index}
                self.__subroutine_next_index__[kind] += 1

    def var_count(self, kind) -> int:
        """Return number of variabled of kind already defined in current scope."""
        match kind:
            case ('static' | 'field'):
                table = self.class_table
            case ('arg' | 'var'):
                table = self.subroutine_table
        count = 0
        for symbol_name in table:
            if table[symbol_name]['kind'] == kind:
                count += 1
        return count

    def kind_of(self, name) -> str:
        """Return kind of named identifier in current scope. If not defined, return NONE."""
        if name in self.subroutine_table:
            return self.subroutine_table[name]['kind']
        elif name in self.class_table:
            return self.class_table[name]['kind']
        else:
            return "NONE"

    def type_of(self, name) -> str:
        """Return type of named identifier in the current scope."""
        if name in self.subroutine_table:
            return self.subroutine_table[name]['type']
        elif name in self.class_table:
            return self.class_table[name]['type']
        else:
            raise ValueError('Symbol table.type_of: symbol not in scope. Use kind_of to check in table.')

    def index_of(self, name) -> int:
        """Return index assigned to named identifier."""
        if name in self.subroutine_table:
            return self.subroutine_table[name]['index']
        elif name in self.class_table:
            return self.class_table[name]['index']
        else:
            raise ValueError('Symbol table.index_of: symbol not in scope. Use kind_of to check in table.')