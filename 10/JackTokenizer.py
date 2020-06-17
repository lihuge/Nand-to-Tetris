from enum import Enum

COMMENT_SYMBOL = '//'
WHITE_SPACE = ' '
EMPTY_STRING = ''
EQUAL_SIGN = '='


CURLY_OPEN = '{'
CURLY_CLOSE = '}'
PARENTHESES_OPEN = '('
PARENTHESES_CLOSE = ')'
SQUARE_BRACKETS_OPEN = '['
SQUARE_BRACKETS_CLOSE = ']'
DOT = '.'
COMMA = ','
SEMICOLON = ';'
PLUS = '+'
MINUS = '-'
ASTERISK = '*'
SLASH = '/'
AMPERSAND = '&'
PIPELINE = '|'
GREATER_THAN = '>'
LESS_THAN = '<'
EQUAL = '='
TILDA = '~'

SYMBOLS_LIST = {CURLY_OPEN, CURLY_CLOSE, PARENTHESES_OPEN, PARENTHESES_CLOSE,
                SQUARE_BRACKETS_OPEN, SQUARE_BRACKETS_CLOSE, DOT, COMMA,
                SEMICOLON, PLUS, MINUS, ASTERISK, SLASH, AMPERSAND, PIPELINE,
                GREATER_THAN, LESS_THAN, EQUAL, TILDA}


CLASS = 'class'
METHOD = 'method'
FUNCTION = 'function'
CONSTRUCTOR = 'constructor'
INT = 'int'
BOOLEAN = 'boolean'
CHAR = 'char'
VOID = 'void'
VAR = 'var'
STATIC = 'static'
FIELD = 'field'
LET = 'let'
DO = 'do'
IF = 'if'
ELSE = 'else'
WHILE = 'while'
RETURN = 'return'
TRUE = 'true'
FALSE = 'false'
NULL = 'null'
THIS = 'this'

KEYWORDS_LIST = {CLASS, METHOD, FUNCTION,
                 CONSTRUCTOR, INT, BOOLEAN,
                 CHAR, VOID, VAR, STATIC,
                 FIELD, LET, DO, IF, ELSE,
                 WHILE, RETURN, TRUE, FALSE,
                 NULL, THIS}


class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5


class KeywordType(Enum):
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 11
    LET = 12
    DO = 13
    IF = 14
    ELSE = 15
    WHILE = 16
    RETURN = 17
    TRUE = 18
    FALSE = 19
    NULL = 20
    THIS = 21


class JackTokenizer:

    def __init__(self, file_name):
        self.next_word = 0
        self.words = []

        comment_zone = False
        with open(file_name) as jackFile:
            for line in jackFile:
                # cleaning up line
                line = line.strip().split(COMMENT_SYMBOL)[0].strip()
                new_line = ''
                if line:
                    for i in range(0, len(line) - 1, 2):
                        if line[i] == '/' and line[i+1] == '*':
                            comment_zone = True
                        elif line[i] == '*' and line[i+1] == '/':
                            comment_zone = False
                        else:
                            if comment_zone == False:
                                new_line += line[i] + line[i+1]
                    if len(line) % 2 != 0 and comment_zone == False:
                        new_line += line[-1]
                    if new_line != '':
                        new_line = new_line.replace(';', ' ; ')
                        new_line = new_line.replace(',', ' , ')
                        new_line = new_line.replace('(', ' ( ')
                        new_line = new_line.replace(')', ' ) ')
                        self.words.extend(new_line.split())
        print(KeywordType.WHILE.name)

    def has_more_tokens(self):
        if len(self.words) > self.next_word:
            return True
        else:
            return False

    def advance(self):
        self.current_token = self.words[self.next_word]
        self.next_word += 1

    def token_type(self):
        if self.current_token in KEYWORDS_LIST:
            return TokenType.KEYWORD
        elif self.current_token in SYMBOLS_LIST:
            return TokenType.SYMBOL
        elif self.current_token.is_int():
            return TokenType.INT_CONST
        elif self.current_token.startswith('"'):
            return TokenType.STRING_CONST
        else:
            return TokenType.IDENTIFIER

    def is_int(self, word):
        try:
            int(word)
            return True
        except ValueError:
            return False

    def keyword(self):
        if self.current_token == CLASS:
            return CLASS
        elif self.current_token == CONSTRUCTOR:
            return CONSTRUCTOR
        elif self.current_token == FUNCTION:
            return FUNCTION
        elif self.current_token == METHOD:
            return METHOD
        elif self.current_token == FIELD:
            return FIELD
        elif self.current_token == STATIC:
            return STATIC
        elif self.current_token == VAR:
            return VAR
        elif self.current_token == INT:
            return INT
        elif self.current_token == CHAR:
            return CHAR
        elif self.current_token == BOOLEAN:
            return BOOLEAN
        elif self.current_token == VOID:
            return VOID
        elif self.current_token == TRUE:
            return TRUE
        elif self.current_token == FALSE:
            return FALSE
        elif self.current_token == NULL:
            return NULL
        elif self.current_token == THIS:
            return THIS
        elif self.current_token == LET:
            return LET
        elif self.current_token == DO:
            return DO
        elif self.current_token == IF:
            return IF
        elif self.current_token == ELSE:
            return ELSE
        elif self.current_token == WHILE:
            return WHILE
        elif self.current_token == RETURN:
            return RETURN

    def symbol(self):
        return self.current_token[0]

    def identifier(self):
        return self.current_token

    def int_val(self):
        return int(self.current_token)

    def string_val(self):
        return self.current_token[1:-1]

    """def arg1(self):
        if self.token_type() == TokenType.SYMBOL:
            return self.current_token.strip()
        else:
            return self.current_token.split(WHITE_SPACE)[1].strip()

    def arg2(self):
        return self.current_token.split(WHITE_SPACE)[2].strip()"""
