
class CompilationEngine:
    def __init__(self, tokenizer, output_line_list):
        self.tokenizer = tokenizer
        self.output_list = output_line_list

    def compile_class(self):
        self.output_list.append('<class>')
        for i in range(3): # class keyword, class identifier, '{'
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
        while self.tokenizer.current_token != ';':
            outlist.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        # add ';':
        outlist.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
        outlist.append('</classVarDec>')

    def compile_subroutine(self):
        outlist = self.output_list
        outlist.append('<subroutineDec>')
        # compile subroutine type, return type, name, '('
        for i in range(4):
            #if i == 2:
                # print(f'Compiling subroutine: {self.tokenizer.current_token}')
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
        while self.tokenizer.current_token != ')':
            outlist.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
        outlist.append('</parameterList>')

    def compile_var_dec(self):
        outlist = self.output_list
        outlist.append('<varDec>')
        while self.tokenizer.current_token != ';':
            self.output_list.append(self.tokenizer.token_to_xml())
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
        while self.tokenizer.current_token != ';':
            if self.tokenizer.current_token == '(':
                # (
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
                # expression
                self.compile_expression_list()
                # )
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
            else:
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
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
        self.output_list.append(self.tokenizer.token_to_xml())
        self.tokenizer.advance()
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
        while self.tokenizer.current_token != ';':
            self.compile_expression()
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
        while self.tokenizer.current_token in ops:
            # op
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            # term
            self.compile_term()
        outlist.append('</expression>')

    def compile_term(self):
        outlist = self.output_list
        outlist.append('<term>')
        match self.tokenizer.token_type():
            case ('integerConstant' | 'stringConstant' | 'keyword'):
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
            case 'identifier':
                # handle varName | varName '[' expression ']' | subroutineName
                # identifier:
                self.output_list.append(self.tokenizer.token_to_xml())
                self.tokenizer.advance()
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
                    # '('
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                    # expression
                    self.compile_expression_list()
                    # ')'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()
                elif self.tokenizer.current_token == '.':
                    # '.' , subroutine name , '('
                    for _ in range(3):
                        self.output_list.append(self.tokenizer.token_to_xml())
                        self.tokenizer.advance()  
                    # expression list
                    self.compile_expression_list()
                    # ')'
                    self.output_list.append(self.tokenizer.token_to_xml())
                    self.tokenizer.advance()

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
        outlist = self.output_list
        outlist.append('<expressionList>')
        if self.tokenizer.current_token != ')':
            self.compile_expression()
        while self.tokenizer.current_token == ',':
            self.output_list.append(self.tokenizer.token_to_xml())
            self.tokenizer.advance()
            self.compile_expression()
        outlist.append('</expressionList>')