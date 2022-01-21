
class CompilationEngine:
    def __init__(self, tokenizer, vmwriter, output_line_list):
        from symboltable import SymbolTable
        self.symbol_table = SymbolTable()
        self.tokenizer = tokenizer
        self.output_list = output_line_list
        self.vmwriter = vmwriter

    def compile_class(self):
        self.output_list.append('<class>')
        # class keyword
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # identifier (class name)
        self.class_name = self.tokenizer.current_token
        self.output_list.append(self.tokenizer.token_to_xml())
        xml_string = f'<IDuse> define class {self.class_name} </IDuse>'
        self.output_list.append(xml_string)
        self.tokenizer.advance()
        # '{'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        finished = False
        while not finished:
            if self.tokenizer.has_more_tokens() == False:
                finished = True
            match self.tokenizer.current_token:        
                case 'field' | 'static':
                    self.compile_class_var_dec()
                case ('constructor' | 'function' | 'method'):
                    self.compile_subroutine()
                case _: # should only happen for final '}'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    if self.tokenizer.has_more_tokens():
                        self.tokenizer.advance()
                    else:
                        finished = True
        self.output_list.append('</class>')

    def compile_class_var_dec(self):
        outlist = self.output_list
        outlist.append('<classVarDec>')
        var_kind, var_name, var_type = None, None, None
        if self.tokenizer.current_token != ';':
            # current token is var kind (static or field)
            var_kind = self.tokenizer.current_token
            var_type = self.tokenizer.look_ahead_token()
            # add kind to output:
            outlist.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            # type to output:
            outlist.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        while self.tokenizer.current_token != ';':
            outlist.append(self.tokenizer.token_to_xml())
            # symbol table entry:
            if self.tokenizer.current_token not in [',',';']:
                # token is name of variable to declare: add to table          
                var_name = self.tokenizer.current_token
                print(f'Adding {var_name,var_type,var_kind} to symbol table:')
                self.symbol_table.define(var_name,var_type,var_kind)
                var_index = self.symbol_table.index_of(var_name)
                xml_string = f'<STentry> define {var_kind} {var_type} {var_name} idx: {var_index} </STentry>'
                outlist.append(xml_string)
            # XML:
            self.tokenizer.advance()
        # add ';':
        outlist.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</classVarDec>')

    def compile_subroutine(self):
        outlist = self.output_list
        self.symbol_table.start_subroutine()
        outlist.append('<subroutineDec>')
        # compile subroutine type, return type
        for i in range(2):
            #if i == 2:
                # print(f'Compiling subroutine: {self.tokenizer.current_token}')
            outlist.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # compile name
        subroutine_name = self.tokenizer.current_token
        outlist.append(self.tokenizer.token_to_xml())
        xml_string = f'<IDuse> define subroutine {subroutine_name} </IDuse>'
        outlist.append(xml_string)
        self.tokenizer.advance()
        # compile '('
        outlist.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # compile parameter list
        self.compile_parameter_list()
        # ')'
        outlist.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()

        # compile subroutine body
        outlist.append('<subroutineBody>')
        # '{'
        outlist.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        while self.tokenizer.current_token != '}':
            # varDec*
            while self.tokenizer.current_token == 'var':
                self.compile_var_dec()
            # Write vm code for function definition
            number_of_arguments = self.symbol_table.var_count('arg')
            self.vmwriter.function(f'{self.class_name}.{subroutine_name}', number_of_arguments)
            # Statements:
            self.compile_statements()
        # }
        outlist.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</subroutineBody>')
        outlist.append('</subroutineDec>')

    def compile_parameter_list(self):
        outlist = self.output_list
        outlist.append('<parameterList>')
        var_kind = 'arg'
        var_name, var_type = None, None
        while self.tokenizer.current_token != ')':
            # symbol table entry:
            if self.tokenizer.current_token != ',':
                if var_type == None:
                    var_type = self.tokenizer.current_token
                else:
                    var_name = self.tokenizer.current_token
                    print(f'Adding {var_name,var_type,var_kind} to symbol table:')
                    self.symbol_table.define(var_name,var_type,var_kind)
                    var_index = self.symbol_table.index_of(var_name)
                    xml_string = f'<STentry> define {var_kind} {var_type} {var_name} idx: {var_index} </STentry>'
                    outlist.append(xml_string)
                    var_type, var_name = None, None

            # xml:
            outlist.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        outlist.append('</parameterList>')

    def compile_var_dec(self):
        outlist = self.output_list
        outlist.append('<varDec>')
        var_kind = 'var'
        var_type, var_name = None, None
        # var kind:
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # var type:
        var_type = self.tokenizer.current_token
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        while self.tokenizer.current_token != ';':
            # xml:
            self.output_list.append(self.tokenizer.token_to_xml())
            # symbol table entry:
            if self.tokenizer.current_token not in [',',';']:
                # token is name of variable to declare: add to table          
                var_name = self.tokenizer.current_token
                print(f'Adding {var_name,var_type,var_kind} to symbol table:')
                self.symbol_table.define(var_name,var_type,var_kind)
                var_index = self.symbol_table.index_of(var_name)
                xml_string = f'<STentry> define {var_kind} {var_type} {var_name} idx: {var_index} </STentry>'
                outlist.append(xml_string)
            self.tokenizer.advance()
        # one more for ';'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</varDec>')

    def compile_statements(self):
        outlist = self.output_list
        outlist.append('<statements>')
        while self.tokenizer.current_token != '}':
            match self.tokenizer.current_token:
                case 'let':
                    self.compile_let()
                case 'if':
                    self.compile_if()
                case 'while':
                    self.compile_while()
                case 'do':
                    self.compile_do()
                case 'return':
                    self.compile_return()
        outlist.append('</statements>')

    def compile_do(self):
        outlist = self.output_list
        outlist.append('<doStatement>')
        no_class_specified = True
        while self.tokenizer.current_token != ';':
            if self.tokenizer.current_token == '(':
                # (
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
                # expression
                nargs = self.compile_expression_list()
                # )
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
            else:
                token_type = self.tokenizer.token_type()
                self.output_list.append(self.tokenizer.token_to_xml()) 
                if token_type == 'identifier':
                    # check if variable in table
                    var_name = self.tokenizer.current_token
                    var_kind = self.symbol_table.kind_of(var_name)
                    if var_kind != 'NONE':
                        var_index = self.symbol_table.index_of(var_name)
                        var_type = self.symbol_table.type_of(var_name)
                        xml_string = f'<IDuse> use {var_kind} {var_type} {var_name} idx: {var_index} </IDuse>'
                        outlist.append(xml_string)
                        specified_class = var_name    
                        no_class_specified = False
                    # else check if next is . implies class
                    elif self.tokenizer.look_ahead_token() == '.':
                        if var_kind == 'NONE':
                            # otherwise var_name is a variable which is instance of some class
                            xml_string = f'<IDuse> use class {var_name} </IDuse>'
                            outlist.append(xml_string)
                            specified_class = var_name 
                            no_class_specified = False
                    # check if next is () implies subroutine
                    elif self.tokenizer.look_ahead_token() == '(':
                        subroutine_name = self.tokenizer.current_token
                        xml_string = f'<IDuse> use subroutine {subroutine_name} </IDuse>'
                        outlist.append(xml_string)
                self.tokenizer.advance()
        # add vm code for routine call:
        if no_class_specified:
            self.vmwriter.call(f'{self.class_name}.{subroutine_name}', nargs) 
        else:
            self.vmwriter.call(f'{specified_class}.{subroutine_name}', nargs)


        # one more for ';'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</doStatement>')

    def compile_let(self):
        outlist = self.output_list
        outlist.append('<letStatement>')
        # 'let'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # varName or varName[expression]:
        # varName
        var_name = self.tokenizer.current_token
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # do IDuse xml:
        var_kind = self.symbol_table.kind_of(var_name)
        if var_kind == 'NONE':
            raise SyntaxError(f'{var_name} invoked in let before declaration.')
        else:
            var_type = self.symbol_table.type_of(var_name)
            var_index = self.symbol_table.index_of(var_name)
            xml_string = f'<IDuse> use {var_kind} {var_type} {var_name} idx: {var_index} </IDuse>'
            outlist.append(xml_string)
        if self.tokenizer.current_token == '[':
            # '['
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            # expression
            self.compile_expression()
            # ']'
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # '='
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # expression:
        self.compile_expression()
        # ';'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</letStatement>')

    def compile_while(self):
        outlist = self.output_list
        outlist.append('<whileStatement>')
        # <while>, '('
        for _ in range(2):
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # expressions:
        self.compile_expression()
        # ')' , '{' :
        for _ in range(2):
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # statements:
        self.compile_statements()
        # '}'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</whileStatement>')

    def compile_return(self):
        outlist = self.output_list
        outlist.append('<returnStatement>')
        # 'return' keyword
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        if self.tokenizer.current_token == ';':
            is_void_function = True
        while self.tokenizer.current_token != ';':
            self.compile_expression()
        if is_void_function:
            # void functions must push 0 onto stack before returning
            # calls to void functions will throw away the value after return
            self.vmwriter.push('constant', 0)
        self.vmwriter.ret()
        # one more for ';'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</returnStatement>')

    def compile_if(self):
        outlist = self.output_list
        outlist.append('<ifStatement>')
        # 'if' , '('
        for _ in range(2):
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # expression:
        self.compile_expression()
        # ')', '{' 
        for _ in range(2):
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # statements:
        self.compile_statements()
        # one more for '}'
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        # handle if there is an else:
        if self.tokenizer.current_token == 'else':
            # else, {
            for _ in range(2):
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
            # statements
            self.compile_statements()
            # }
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        outlist.append('</ifStatement>')

    def compile_expression(self): 
        outlist = self.output_list
        outlist.append('<expression>')
        # nested expression
        if self.tokenizer.current_token == '(':
            outlist.append('<term>')
            # (
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            # inner expression
            self.compile_expression()
            # )
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            outlist.append('</term>')
        # single term
        else:
            self.compile_term()
        # if next is op, more term
        ops = {'+','-','*','/','&amp;','|','&lt;','&gt;','='}
        builtin_ops = {'+':'add','-':'neg','&amp;':'and','|':'or','&lt;':'lt','&gt;':'gt','=':'eq'}

        while self.tokenizer.current_token in ops:
            # op
            op = self.tokenizer.current_token
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            # term
            self.compile_term()
            # TODO VM cod for op?
            if op in builtin_ops:
                self.vmwriter.arithmetic(builtin_ops[op])
            elif op == '*':
                self.vmwriter.call('Math.multiply', 2)
            elif op == '/':
                self.vmwriter.call('Math.divide', 2)
        outlist.append('</expression>')

    def compile_term(self):
        outlist = self.output_list
        outlist.append('<term>')
        match self.tokenizer.token_type():
            case 'integerConstant':
                integer = self.tokenizer.current_token
                self.vmwriter.push('constant', integer)
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
            case ('stringConstant' | 'keyword'):
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
            case 'identifier':
                # handle varName | varName '[' expression ']' | subroutineName
                # identifier 'name':
                var_name = self.tokenizer.current_token
                var_kind = self.symbol_table.kind_of(var_name)
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
                if var_kind != 'NONE':
                    category = var_kind
                    var_index = self.symbol_table.index_of(var_name)
                    var_type = self.symbol_table.type_of(var_name)
                    xml_string = f'<IDuse> use {var_kind} {var_type} {var_name} idx: {var_index} </IDuse>'
                    outlist.append(xml_string)      
                # if next symbol is (, [, or ., then it's a subroutineCall
                # array or array
                if self.tokenizer.current_token == '[':
                    # '['
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                    # expression
                    self.compile_expression()
                    # ']'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                elif self.tokenizer.current_token == '(':
                    subroutine_name = self.tokenizer.current_token
                    xml_string = f'<IDuse> use subroutine {subroutine_name} </IDuse>'
                    outlist.append(xml_string)
                    # '('
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                    # expression
                    self.compile_expression_list()
                    # ')'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                    # TODO add vm code for subroutine. remember to add class name.subroutine
                elif self.tokenizer.current_token == '.':
                    # previous was class:
                    if var_kind == 'NONE':
                        # otherwise var_name is a variable which is instance of some class
                        xml_string = f'<IDuse> use class {var_name} </IDuse>'
                        outlist.append(xml_string)
                    # '.'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()  
                    # subroutine name
                    subroutine_name = self.tokenizer.current_token
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()  
                    xml_string = f'<IDuse> use subroutine {subroutine_name} </IDuse>'
                    outlist.append(xml_string)
                    # (
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()  
                    # expression list
                    nargs = self.compile_expression_list()
                    # ')'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                    self.vmwriter.call(f'{var_name}.{subroutine_name}', nargs)

            case 'symbol':
                match self.tokenizer.current_token:
                    # unaryOp and term
                    case ('-' | '~'):
                        # unaryOp
                        self.output_list.append(self.tokenizer.token_to_xml())
                        self.tokenizer.advance() 
                        # term
                        self.compile_term()
                            
                    # (expression)
                    case '(':
                        # '('
                        self.output_list.append(self.tokenizer.token_to_xml())
                        self.tokenizer.advance() 
                        # expression
                        self.compile_expression()
                        # ')'
                        self.output_list.append(self.tokenizer.token_to_xml())
                        self.tokenizer.advance() 
            case _:
                raise SyntaxError(f'Unknown term (compile_term): {self.tokenizer.token_type()}')
        outlist.append('</term>')

    def compile_expression_list(self):
        nargs = 0
        outlist = self.output_list
        outlist.append('<expressionList>')
        if self.tokenizer.current_token != ')':
            self.compile_expression()
            nargs += 1
        while self.tokenizer.current_token == ',':
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            self.compile_expression()
            nargs += 1
        outlist.append('</expressionList>')
        return nargs