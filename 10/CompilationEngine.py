from JackTokenizer import *

XML_EXTENSION = 'xml'
DOT = '.'
BACK_SLASH = '\\'
ADD = 'add'
SUBSTRACT = 'sub'
NEG = 'neg'
EQUALIZER = 'eq'
GREATERTHAN = 'gt'
LOWERTHAN = 'lt'
AND = 'and'
OR = 'or'
NOT = 'not'

SYMBOL = 'symbol'
CLASS_VAR_DEC = {STATIC, FIELD}
SUBROUTINE_DEC = {CONSTRUCTOR, FUNCTION, METHOD}
STATEMENTS_TOKENS = {LET, IF, WHILE, DO, RETURN}


class CompilationEngine:
    return_label_counter = 0

    def __init__(self, file_name, more_than_one_file, tokenizer):
        self.output_file = open(file_name + DOT + XML_EXTENSION, "w")
        self.file_name = file_name.split(BACK_SLASH)[-1]
        self.indent_evel = 0
        self.tokenizer = JackTokenizer('bla')

        if more_than_one_file:
            pass

    def get_indent_string(self):
        if self.indent_evel == 0:
            return ""
        return " " * self.indent_evel

    def __write_line(self, line):
        self.output_file.write(self.get_indent_string() + line + '\n')

    def __write_tag(self, tag):
        self.__write_line("<{}>".format(tag))

    def __write_complete_tag_and_token(self):
        tag = self.tokenizer.token_type().name.lower()
        token = self.tokenizer.current_token
        if self.tokenizer.token_type == TokenType.INT_CONST:
            tag = 'integarConstant'
        if self.tokenizer.token_type == TokenType.STRING_CONST:
            tag = 'stringConstant'
            token = self.tokenizer.string_val()
        self.__write_line(self.get_indent_string() +
                          "<{}>{}</{}>".format(tag, token, tag))

    def compile_class(self):
        self.__write_tag(CLASS)
        self.indent_evel += 1
        self.__process(CLASS)
        while (self.tokenizer.has_more_tokens()):
            if self.tokenizer.current_token in CLASS_VAR_DEC:
                self.__write_tag('classVarDec')
                self.indent_evel += 1
                self.compile_var_def()
                self.indent_evel -= 1
                self.__write_tag('/classVarDec')
            elif (self.tokenizer.token_type in SUBROUTINE_DEC):
                self.compile_subroutine__dec()
            else:
                self.__process(self.tokenizer.current_token)
        self.__write_tag('/' + CLASS)

    def compile_subroutine__dec(self):
        self.__write_tag(SUBROUTINE_DEC)
        self.indent_evel += 1
        self.__process(self.tokenizer.current_token)
        while self.tokenizer.current_token != '}':
            if self.tokenizer.current_token == '(':
                self.__process(self.tokenizer.current_token)
                self.compile_parameters_list()
            elif self.tokenizer.current_token == '{':
                self.__process(self.tokenizer.current_token)
                self.compile_subroutine_body()
            else:
                self.__process(self.tokenizer.current_token)
        self.__write_complete_tag_and_token()
        self.indent_evel -= 1
        self.__write_tag('/' + SUBROUTINE_DEC)
        self.tokenizer.advance()

    def compile_parameters_list(self):
        self.__write_tag('parameterList')
        self.indent_evel += 1
        while (self.tokenizer.current_token != ')'):
            self.__process(self.tokenizer.current_token)
        self.__write_complete_tag_and_token()
        self.indent_evel -= 1
        self.__write_tag('/parameterList')
        self.tokenizer.advance()

    def compile_subroutine_body(self):
        self.__write_tag('subroutineBody')
        self.indent_evel += 1
        self.__process(self.tokenizer.current_token)
        while self.tokenizer.current_token != '}':
            if self.tokenizer.current_token in STATEMENTS_TOKENS:
                self.compile_statements()
            elif self.tokenizer.current_token == VAR:
                self.__write_tag('varDec')
                self.indent_evel += 1
                self.compile_var_def()
                self.indent_evel -= 1
                self.__write_tag('/varDec')
            else:
                self.__process(self.tokenizer.current_token)
        self.__write_complete_tag_and_token()
        self.indent_evel -= 1
        self.__write_tag('/subroutineBody')
        self.tokenizer.advance()

    def compile_var_def(self):
        self.__process(self.tokenizer.current_token)
        while (self.tokenizer.current_token != ';'):
            self.__process(self.tokenizer.current_token)
        self.__write_complete_tag_and_token()
        self.tokenizer.advance()

    def compile_statements(self):
        self.__write_tag('statements')
        self.indent_evel += 1
        while (self.tokenizer.current_token != '}'):
            if self.tokenizer.current_token == LET:
                self.compile_let()
            elif self.tokenizer.current_token == IF:
                self.compile_if()
            elif self.tokenizer.current_token == WHILE:
                self.compile_while()
            elif self.tokenizer.current_token == DO:
                self.compile_do()
            else:
                self.compile_return()
        self.__write_complete_tag_and_token()
        self.indent_evel -= 1
        self.__write_tag('/statements')
        self.tokenizer.advance()

    def compile_let(self):
        self.__write_tag('letStatement')
        self.indent_evel += 1
        self.__process(LET)
        self.__process(self.tokenizer.current_token)
        self.__process(EQUAL)
        self.compile_expression
        self.__process(SEMICOLON)
        self.indent_evel -= 1
        self.__write_tag('\ifStatement')

    def compile_if(self):
        self.__write_tag('ifStatement')
        self.indent_evel += 1
        self.__process(IF)
        self.__process('(')
        self.compile_expression()
        self.__process(')')
        self.__process('{')
        self.compile_statements()
        self.__process('}')
        self.indent_evel -= 1
        self.__write_tag('\ifStatement')

    def __process(self, token):
        if self.tokenizer.current_token == token:
            self.__printXMLToken()
        else:
            print('syntax error')
        self.tokenizer.advance()

    def __printXMLToken(self):
        self.__write_complete_tag_and_token()

    def compile_while(self):
        self.__write_tag('whileStatement')
        self.indent_evel += 1
        self.__process(WHILE)
        self.__process('(')
        self.compile_expression()
        self.__process(')')
        self.__process('{')
        self.compile_statements()
        self.__process('}')
        self.indent_evel -= 1
        self.__write_tag('\whileStatement')

    def compile_do(self):
        self.__write_tag('doStatement')
        self.indent_evel += 1
        self.__process(SEMICOLON)
        self.indent_evel -= 1
        self.__write_tag('\doStatement')

    def compile_return(self):
        self.__write_tag('returnStatement')
        self.indent_evel += 1
        self.__process(RETURN)
        while (self.tokenizer.current_token != ';')
        compile_expression()
        self.__process(SEMICOLON)
        self.indent_evel -= 1
        self.__write_tag('\returnStatement')

    def compile_expression(self):
        pass

    def compile_expression_list(self):
        pass

    def close(self):
        self.output_file.close()
