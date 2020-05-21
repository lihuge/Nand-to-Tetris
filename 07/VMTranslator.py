import sys
import os.path
from os import path
from Parser import Parser
from Parser import Command_Type
from CodeWriter import CodeWriter


USAGE_INSTRUCTION = 'Usage: VMTranslator file.vm'
FILE_OPEN_ERROR = 'Error: Cannot open file'
FILE_WRITE_ERROR = 'Error: Cannot write to file'
VM_EXTENSION = 'vm'
DOT = '.'
POP = 'pop'
PUSH = 'push'

# Checking if arguments for program are ok and if vm file exists
def checkInput():
    if len(sys.argv) is not 2:
        print(USAGE_INSTRUCTION) # too many/less arguments
        sys.exit()
    fileSplit = sys.argv[1].strip().split(DOT)

    if len(fileSplit) < 2:
        print(USAGE_INSTRUCTION) # no '.'
        sys.exit()    
        
    ext = fileSplit[-1].strip().lower()

    if ext != VM_EXTENSION: # not .vm extension
        print(USAGE_INSTRUCTION)
        sys.exit()
    fileName = '.'.join(fileSplit[0:-1]).strip().lower()
    checkFile = path.exists(sys.argv[1])

    if checkFile is False: # file doesn't exists/can't open file
        print(FILE_OPEN_ERROR)
        sys.exit()
    return fileName

# running the function to parse commands and write the translation to a .asm file
def parseCommandsAndWriteOutput():
    while (parser.hasMoreLines()):
        parser.advance()
        instructionType = parser.instructionType()
        if (instructionType == Command_Type.C_ARITHMETIC):
            codeWriter.writeArithmetic(parser.arg1())
        elif (instructionType in [Command_Type.C_POP, Command_Type.C_PUSH]):
            segment = parser.arg1()
            index = int(parser.arg2())
            codeWriter.writePushPop(instructionType, segment, index)
    codeWriter.close()

fileName = checkInput()
parser = Parser(fileName + DOT + VM_EXTENSION)
try:
    codeWriter = CodeWriter(fileName)
    parseCommandsAndWriteOutput()
except IOError:
    print(FILE_WRITE_ERROR)
    sys.exit()