COMMENT_SYMBOL = '//'
PUSH_BEGINNING = 'push'
POP_BEGINNING = 'pop'
ADD_BEGINNING = 'add'
SUBSTRACT_BEGINNING = 'sub'
NEG_BEGINNING = 'neg'
EQUALIZER_BEGINNING = 'eq'
GREATERTHAN_BEGINNING = 'gt'
LOWERTHAN_BEGINNING = 'lt'
AND_BEGINNING = 'and'
OR_BEGINNING = 'or'
NOT_BEGINNING = 'not'
LABEL_BEGINNING = 'label'
GOTO_BEGINNING = 'goto'
IFGOTO_BEGINNING = 'if-goto'
FUNCTION_BEGINNING = 'function'
CALL_BEGINNING = 'call'
RETURN_BEGINNING = 'return'
WHITE_SPACE = ' '
EMPTY_STRING = ''
EQUAL_SIGN = '='
SEMICOLON_SIGN = ';'
ARITHMETIC_LIST = {ADD_BEGINNING, SUBSTRACT_BEGINNING, NEG_BEGINNING,
                    EQUALIZER_BEGINNING, GREATERTHAN_BEGINNING, LOWERTHAN_BEGINNING,
                    AND_BEGINNING, OR_BEGINNING, NOT_BEGINNING}


from enum import Enum
class Command_Type(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class Parser:
    def __init__(self, fileName):
        self.nextLine = 0
        self.linesArray = []
        with open(fileName) as vmFile:
            for line in vmFile:
                # cleaning up line
                line = line.strip().split(COMMENT_SYMBOL)[0]
                if (line):
                    self.linesArray.append(line)

    def hasMoreLines(self):
        if (len(self.linesArray) > self.nextLine):
            return True
        else:
            return False

    def advance(self):
        self.currentCommand = self.linesArray[self.nextLine]
        self.nextLine += 1

    def instructionType(self):
        if (self.currentCommand.startswith(tuple(ARITHMETIC_LIST))):
            return Command_Type.C_ARITHMETIC
        elif (self.currentCommand.startswith(PUSH_BEGINNING)):
            return Command_Type.C_PUSH
        elif (self.currentCommand.startswith(POP_BEGINNING)):
            return Command_Type.C_POP
        elif (self.currentCommand.startswith(LABEL_BEGINNING)):
            return Command_Type.C_LABEL
        elif (self.currentCommand.startswith(GOTO_BEGINNING)):
            return Command_Type.C_GOTO
        elif (self.currentCommand.startswith(IFGOTO_BEGINNING)):
            return Command_Type.C_IF
        elif (self.currentCommand.startswith(FUNCTION_BEGINNING)):
            return Command_Type.C_FUNCTION
        elif (self.currentCommand.startswith(RETURN_BEGINNING)):
            return Command_Type.C_RETURN
        elif (self.currentCommand.startswith(CALL_BEGINNING)):
            return Command_Type.C_CALL

    def arg1(self):
        if (self.instructionType() == Command_Type.C_ARITHMETIC):
            return self.currentCommand
        else:
            return self.currentCommand.split(WHITE_SPACE)[1]

    # returns dest part
    def arg2(self):
        return self.currentCommand.split(WHITE_SPACE)[2]