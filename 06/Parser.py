COMMENT_SYMBOL = '//'
LOOP_BEGINNING = '('
SYMBOL_BEGINNING = '@'
WHITE_SPACE = ' '
EMPTY_STRING = ''
EQUAL_SIGN = '='
SEMICOLON_SIGN = ';'

from enum import Enum
class Command_Type(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3


class Parser:
    def __init__(self, fileName):
        self.nextLine = 1
        self.linesArray = []
        with open(fileName) as asmFile:
            for line in asmFile:
                line = line.strip().split(COMMENT_SYMBOL)[0].replace(WHITE_SPACE, EMPTY_STRING)
                if (line):
                    self.linesArray.append(line)

    

    def hasMoreLines(self):
        if (len(self.linesArray) >= self.nextLine):
            return True
        else:
            return False

    def advance(self):
        self.currentInstruction = self.linesArray[self.nextLine-1]
        self.nextLine += 1

    def instructionType(self):
        if (self.currentInstruction.startswith(LOOP_BEGINNING)):
            return Command_Type.L_INSTRUCTION
        elif (self.currentInstruction.startswith(SYMBOL_BEGINNING)):
            return Command_Type.A_INSTRUCTION
        else:
            return Command_Type.C_INSTRUCTION

    def symbol(self):
        if self.currentInstruction.startswith(LOOP_BEGINNING):
            return self.currentInstruction[1:-1]
        else:
            return self.currentInstruction[1:]

    def dest(self):
        if ('=' in self.currentInstruction):
            return self.currentInstruction[:self.currentInstruction.find(EQUAL_SIGN)]
        else:
            return EMPTY_STRING
    
    def comp(self):
        startIndex = 0
        endIndex = len(self.currentInstruction)
        if (EQUAL_SIGN in self.currentInstruction):
            startIndex = self.currentInstruction.find(EQUAL_SIGN) + 1
        if (SEMICOLON_SIGN in self.currentInstruction):
            endIndex = self.currentInstruction.find(SEMICOLON_SIGN)
        return self.currentInstruction[startIndex:endIndex]

    def jump(self):
        if (SEMICOLON_SIGN in self.currentInstruction):
            return self.currentInstruction[self.currentInstruction.find(SEMICOLON_SIGN) + 1:]
        else:
            return EMPTY_STRING
    
    

    
            


