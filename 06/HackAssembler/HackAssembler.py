import sys
import os.path
from os import path
from Parser import *
from Code import Code
from SymbolTable import SymbolTable

HACK_EXTENSION = 'hack'
ASM_EXTENSION = 'asm'
DOT = '.'
USAGE_INSTRUCTION = 'Usage: HackAssembler file.asm'
FILE_OPEN_ERROR = 'Error: Cannot open file'
FILE_WRITE_ERROR = 'Error: Cannot write to file'
NEW_LINE = '\n'
C_INSTRUCTION_PREFIX = '111'

# Checking if arguments for program are ok and if asm file exists
def checkInput():
    if len(sys.argv) is not 2:
        print(USAGE_INSTRUCTION) # too many/less arguments
        sys.exit()
    fileSplit = sys.argv[1].strip().split(DOT)

    if len(fileSplit) is not 2:
        print(USAGE_INSTRUCTION) # more than one '.'
        sys.exit()
    fileName = fileSplit[0].strip()
    ext = fileSplit[1].strip().lower()

    if ext != ASM_EXTENSION: # not .asm extension
        print(USAGE_INSTRUCTION)
        sys.exit()
    fileName = fileSplit[0].strip()
    checkFile = path.exists(sys.argv[1])

    if checkFile is False: # file doesn't exists/can't open file
        print(FILE_OPEN_ERROR)
        sys.exit()
    return fileName

# running first time to capture the loop instructions and add them to Symbol table
def firstRunForLInstructions():
    while (parser.hasMoreLines()):
        parser.advance()
        if (parser.instructionType() == Command_Type.L_INSTRUCTION):
            symbolTable.addEntry(parser.symbol(), parser.nextLine - 1)
            del parser.linesArray[parser.nextLine - 1]
            parser.nextLine -= 1

# running second time to capture all other instructions and convert them to binary commands
def secondRunForParsingFile():
    while (parser.hasMoreLines()):
        parser.advance()
        if (parser.instructionType() == Command_Type.A_INSTRUCTION):
            outputFile.write(dealWithACommand())
            if parser.hasMoreLines():
                outputFile.write(NEW_LINE)
        elif (parser.instructionType() == Command_Type.C_INSTRUCTION):
            outputFile.write(dealWithCCommand())
            if parser.hasMoreLines():
                outputFile.write(NEW_LINE)
        

# compose a binary c-instruction
def dealWithCCommand():
    destString = Code.dest(parser.dest())
    compString = Code.comp(parser.comp())
    jumpString = Code.jump(parser.jump())
    return C_INSTRUCTION_PREFIX + compString + destString + jumpString
# compose a binary a-instruction
def dealWithACommand():
    symbol = parser.symbol()
    isInt = False
    try:
        # if integer set address to it
        address = int(symbol)
        isInt = True
    except ValueError:
        pass
    # if not integer, deal with the symbol
    if not isInt:                
        if (symbolTable.contains(symbol) == False):
            address = symbolTable.nextFreeAddress
            symbolTable.addEntry(
                symbol, symbolTable.nextFreeAddress)
            symbolTable.nextFreeAddress += 1
        else:
            address = symbolTable.getAddress(symbol)

    return '{0:016b}'.format(address)



fileName = checkInput()
asmFile = sys.argv[1]
try:
    outputFile = open(fileName + DOT + HACK_EXTENSION, "w")
    parser = Parser(asmFile)
    symbolTable = SymbolTable()
    firstRunForLInstructions()
    parser = Parser(asmFile)
    secondRunForParsingFile()
except IOError:
    print(FILE_WRITE_ERROR)
    sys.exit()
