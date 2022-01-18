
from ast import keyword


class JackTokenizer:
    def __init__(self, input_file_name): #TODO
        # TODO: handle multiline comments, remove whitespace, iterate over parts.
        output_file_name = input_file_name[:-5]+'T.xml'
        self.lines = []
        self.tokens_list = [] # [(token_type,token),...] e.g. [('symbol','{'),...]
        self.current_token = None
        self.current_token_idx = -1
        # Get lines from file, remove comments, whitespace:
        self.lines = self.__get_stripped_lines__(input_file_name)
        # Check for empty file:
        if len(self.lines) < 1:
            raise ValueError('JACK file is empty')
        # Split lines into tokens here
        self.__tokenize__()
        self.__generate_output_xml_file__(output_file_name)

    def has_more_tokens(self) -> bool:
        return len(self.tokens_list) > self.current_token_idx + 1

    def advance(self):
        self.current_token_idx += 1
        self.current_token = self.tokens_list[self.current_token_idx][1]

    def token_type(self) -> str:
        return self.tokens_list[self.current_token_idx][0]

    def keyword(self) -> str:
        return self.current_token

    def symbol(self) -> str:
        return self.current_token

    def identifier(self) -> str:
        return self.current_token

    def int_val(self) -> int: #TODO
        current_int = int(self.current_token)
        return current_int

    def string_val(self) -> str: #TODO
        return self.current_token

    def __tokenize__(self):
        for line in self.lines:
            char_list = []
            for char in line:
                char_list.append(char)
            idx = 0
            current_word = []
            while idx < len(char_list):
                char = char_list[idx]
                match char:
                    # if end of a word, add that to the tokens list first
                    case '"':
                        if current_word:
                            self.tokens_list.append(self.__tokenize_word__(current_word))
                            current_word = []
                        closing_idx = char_list.index('"',idx+1)
                        # Don't include quotes in token:
                        StringConstant = ''.join(char_list[idx+1:closing_idx])
                        self.tokens_list.append(('stringConstant', StringConstant))
                        idx = closing_idx
                    case ('{'|'}'|'('|')'|'['|']'|'.'|
                            ','|';'|'+'|'-'|'*'|'/'|'&'|
                           '|'|'<'|'>'|'='|'~'):
                        if current_word:
                            self.tokens_list.append(self.__tokenize_word__(current_word))
                            current_word = []
                        match char:
                            case '<':
                                symbol = '&lt;'
                            case '>':
                                symbol = '&gt;'
                            case '&':
                                symbol = '&amp;'
                            case _:
                                symbol = char
                        self.tokens_list.append(('symbol', symbol))
                    case ' ':
                        if current_word:
                            self.tokens_list.append(self.__tokenize_word__(current_word))
                            current_word = []
                    case _:
                        current_word.append(char)
                idx += 1
            if current_word:
                            self.tokens_list.append(self.__tokenize_word__(current_word))
                            current_word = []

    def __tokenize_word__(self, word):
        # print(f'tokenizing:{word}')
        word = ''.join(word)
        # returns (token_type,token_value) of word,  for INT_CONST, KEYWORD, IDENTIFIER
        keywords = {'class', 'constructor', 'function', 'method', 'field', 'static',
                    'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                    'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}
        is_keyword = word in keywords
        is_integer = word.isnumeric()
        if is_keyword:
            token = ('keyword', word)
        elif is_integer:
            token = ('integerConstant', int(word))
        else:
            token = ('identifier', word)
        # if no match, there's been a problem:
        if not token:
            print(f'Invalid word in __tokenize_word__: {word}')
            return
        return token

    def __get_stripped_lines__(self, input_file_name):
        lines = []
        with open(input_file_name, 'r') as file:
            in_multiline_comment = False
            for line in file:
                # comment types: //, /** */, or /* */
                if in_multiline_comment:
                    #print(f'in multiline comment line:{line}')
                    close_in_this_line = '*/' in line
                    #print(f'close in this line: {close_in_this_line}')
                    if close_in_this_line:
                        in_multiline_comment = False
                        begin_after_comment_idx = line.index('*/') + 2
                        if begin_after_comment_idx < len(line):
                            stripped_line = line[begin_after_comment_idx:].strip()
                elif '/**' in line or '/*' in line:
                    if '/**' in line:
                        begin_open_comment_idx = line.index('/**')
                        end_open_comment_idx = begin_open_comment_idx + 2
                    else:
                        begin_open_comment_idx = line.index('/*')
                        end_open_comment_idx = begin_open_comment_idx + 1
                    stripped_line = line[:begin_open_comment_idx].strip()
                    begin_comment_idx = end_open_comment_idx + 1
                    in_multiline_comment = True
                    close_in_this_line = '*/' in line[begin_comment_idx:]
                    if close_in_this_line:
                        in_multiline_comment = False
                        begin_after_comment_idx = line.index('*/',begin_comment_idx) + 2
                        if begin_after_comment_idx < len(line):
                            stripped_line = stripped_line + line[begin_after_comment_idx:]
                            stripped_line = stripped_line.strip()
                elif '//' in line:
                    comment_index = line.find('//')
                    stripped_line = line[:comment_index].strip()
                else:
                    stripped_line = line.strip()

                if len(stripped_line) > 0:
                    lines.append(stripped_line)
        return lines

    def __generate_output_xml_file__(self, output_file_name):
        with open(output_file_name,'w') as outfile:
            outlines = ['<tokens>']
            for (token_type,token_val) in self.tokens_list:
                outlines.append(f'<{token_type}> {token_val} </{token_type}>')
            outlines.append('</tokens>')
            outfile.write('\n'.join(outlines))


# test = JackTokenizer('/Users/marshall/Desktop/nand2tetris2021/TECS/CompilationEngine/Main.jack')