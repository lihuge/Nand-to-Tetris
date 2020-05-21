from Parser import Command_Type

ASM_EXTENSION = 'asm'
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

SEGMENT_ARGUMENT = 'argument'
SEGMENT_LOCAL = 'local'
SEGMENT_STATIC = 'static'
SEGMENT_CONSTANT = 'constant'
SEGMENT_THIS = 'this'
SEGMENT_THAT = 'that'
SEGMENT_POINTER = 'pointer'
SEGMENT_TEMP = 'temp'

LOCAL_ADDRESS = 'LCL'
ARGUMENT_ADDRESS = 'ARG'
STATIC_ADDRESS = 16
THIS_ADDRESS = 'THIS'
THAT_ADDRESS = 'THAT'
TEMP_ADDRESS = 5
POINTER_ADDRESS = 3

COMPARISION_LOOP_SYMBOL =  'COMPARISION_LOOP_'
END_COMPARISION_LOOP_SYMBOL = 'END_COMPARISION_LOOP_'

SEGMENT_DICTIONARY = {'local': LOCAL_ADDRESS, 'argument': ARGUMENT_ADDRESS,
                     'this':THIS_ADDRESS, 'that':THAT_ADDRESS,
                     'temp':TEMP_ADDRESS, 'static':STATIC_ADDRESS, 'pointer':POINTER_ADDRESS}


class CodeWriter:
    def __init__(self, fileName):
            self.outputFile = open(fileName + DOT + ASM_EXTENSION, "w")
            self.fileName = fileName.split(BACK_SLASH)[-1]
            self.comparisionsCounter = 0

    def __writeLine(self, line):
        self.outputFile.write(line + '\n')

    def __dealWithArithmetic(self, command):
        if (command == ADD):
            self.__writeLine('M=D+M')
        elif (command == SUBSTRACT):
            self.__writeLine('M=M-D')
        elif (command == NEG):
            self.__writeLine('M=-M')
        elif (command in [EQUALIZER, GREATERTHAN, LOWERTHAN]):
            self.comparisionsCounter += 1
            self.__writeLine('D=M-D')
            self.__writeLine('@' + COMPARISION_LOOP_SYMBOL + str(self.comparisionsCounter))
            if (command == EQUALIZER):
                self.__writeLine('D;JEQ')
            elif (command == GREATERTHAN):
                self.__writeLine('D;JGT')
            else:
                self.__writeLine('D;JLT')
            self.__handleComparisionJumps()
        elif (command == AND):
            self.__writeLine('M=M&D')
        elif (command == OR):
            self.__writeLine('M=M|D')
        else:
            self.__writeLine('M=!M')


    def writeArithmetic(self, command):
        if (command not in [NEG, NOT]):
            self.__putStackTopToD()
        self.__putStackTopIntoA()
        self.__dealWithArithmetic(command)
        self.__incrementSP()

    # sets the address for the segment and the index for temp,pointer,static and constant cases
    def __setAddressForSegment(self, segment, index):
        if (segment in [SEGMENT_TEMP, SEGMENT_POINTER]):
            address = '@R' + str(SEGMENT_DICTIONARY[segment] + index)
        elif (segment == SEGMENT_STATIC):
            address = '@' + self.fileName + DOT + str(index)
        elif (segment != SEGMENT_CONSTANT):
            address = '@' + SEGMENT_DICTIONARY[segment]
        else:
            address = ''
        return address

    def writePushPop(self, command, segment, index):
        address = self.__setAddressForSegment(segment, index) 
        if (command == Command_Type.C_POP):
            if (segment in [SEGMENT_TEMP, SEGMENT_POINTER, SEGMENT_STATIC]):
                self.__putStackTopToD()
                self.__writeLine(address)
                self.__writeLine('M=D')
            else:
                self.__putIndexInD(index)
                self.__saveAddressWithIndexIntoTemp(address)
                self.__putStackTopToD()
                self.__putDInAddressOfTemp()
        elif (command == Command_Type.C_PUSH):
            if (segment in [SEGMENT_TEMP, SEGMENT_POINTER, SEGMENT_STATIC]):
                self.__writeLine(address)
                self.__writeLine('D=M')
            else:
                self.__putIndexInD(index)
                if (segment != SEGMENT_CONSTANT):
                    self.__writeLine(address)
                    self.__writeLine('A=M+D')
                    self.__writeLine('D=M')
            self.__putDIntoStackTop()
            self.__incrementSP()

    """ handling comparision situation where a new symbol need to be used to distinguish between
        the situation where the comparision return true and false, we do that by creating labels
        jumping between them """
    def __handleComparisionJumps(self):
        self.__writeLine('@SP')
        self.__writeLine('A=M')
        self.__writeLine('M=0')
        self.__writeLine('@' + END_COMPARISION_LOOP_SYMBOL + str(self.comparisionsCounter))
        self.__writeLine('0;JMP')
        self.__writeLine('(' + COMPARISION_LOOP_SYMBOL + str(self.comparisionsCounter) + ')')
        self.__writeLine('@SP')
        self.__writeLine('A=M')
        self.__writeLine('M=-1')
        self.__writeLine('(' + END_COMPARISION_LOOP_SYMBOL + str(self.comparisionsCounter) + ')')               

    def __incrementSP(self):
        self.__writeLine('@SP')
        self.__writeLine('M=M+1')
    
    def __decrementSP(self):
        self.__writeLine('@SP')
        self.__writeLine('M=M-1')  
       
    def __putIndexInD(self, index):
        self.__writeLine('@' + str(index))
        self.__writeLine('D=A')

    def __putDIntoStackTop(self):
        self.__writeLine('@SP')
        self.__writeLine('A=M')
        self.__writeLine('M=D')

    # dealing with a situation where we need to use a temp memory address in order to do operation on 2 variables
    def __saveAddressWithIndexIntoTemp(self, address):
        self.__writeLine(address)
        self.__writeLine('D=M+D')
        self.__writeLine('@R5')
        self.__writeLine('M=D')

    # taking the data out of temp memory address used before in order to complete the operation on 2 variables
    def __putDInAddressOfTemp(self):
        self.__writeLine('@R5')
        self.__writeLine('A=M')
        self.__writeLine('M=D')

    def __putStackTopToD(self):
        self.__putStackTopIntoA()
        self.__writeLine('D=M')

    def __putStackTopIntoA(self):
        self.__decrementSP()
        self.__writeLine('A=M')

    def close(self):
        self.outputFile.close()





