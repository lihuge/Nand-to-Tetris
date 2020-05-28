import sys
import os.path
from os import path
from Parser import Parser
from Parser import Command_Type
from CodeWriter import CodeWriter


USAGE_INSTRUCTION = 'Usage: VMTranslator <file.vm or directory>'
NO_VM_FILES = 'Error: No .vm files in directory'
FILE_OPEN_ERROR = 'Error: Cannot open file'
FILE_WRITE_ERROR = 'Error: Cannot write to file'
VM_EXTENSION = 'vm'
DOT = '.'
BACK_SLASH = '\\'
POP = 'pop'
PUSH = 'push'

def checkInputFolder():
    folderName = sys.argv[1]
    if (folderName[-1] == BACK_SLASH or folderName[-1] == '"' or folderName[-1] == "'"):
        folderName = folderName[:-1]
    checkFolder = path.isdir(folderName)
    if (checkFolder):
        return folderName
    return None

# Checking if arguments for program are ok and if vm file exists
def checkInput():
    if len(sys.argv) is not 2:
        print(USAGE_INSTRUCTION) # too many/less arguments
        sys.exit()
    fileSplit = sys.argv[1].strip().split(DOT)

    if len(fileSplit) < 2: 
        return None
        
    ext = fileSplit[-1].strip().lower()

    if ext != VM_EXTENSION: # not .vm extension
        return None
    fileName = '.'.join(fileSplit[0:-1]).strip()
    checkFile = path.exists(sys.argv[1])

    if checkFile is False: # file doesn't exists/can't open file
        print(FILE_OPEN_ERROR)
        sys.exit()
    if (path.isdir(sys.argv[1])):
        return None
    elif (path.isfile(sys.argv[1])):
        return fileName

    return None

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
        elif (instructionType == Command_Type.C_LABEL):
            labelName = parser.arg1()
            codeWriter.writeLabel(labelName)
        elif (instructionType == Command_Type.C_GOTO):
            labelJump = parser.arg1()
            codeWriter.writeGoto(labelJump)
        elif (instructionType == Command_Type.C_IF):
            labelCondition = parser.arg1()
            codeWriter.writeIf(labelCondition)
        elif (instructionType == Command_Type.C_FUNCTION):
            functionName = parser.arg1()
            numberOfVars = int(parser.arg2())
            codeWriter.writeFunction(functionName, numberOfVars)
        elif (instructionType == Command_Type.C_RETURN):
            codeWriter.writeReturn()
    codeWriter.close()

fileName = checkInput()
if (fileName != None): # this case handles single file
    parser = Parser(fileName + DOT + VM_EXTENSION)
    try:
        codeWriter = CodeWriter(fileName)
        parseCommandsAndWriteOutput()
    except IOError:
        print(FILE_WRITE_ERROR)
        sys.exit()
else:
    pathName = checkInputFolder()
    if (pathName == None):
        print(USAGE_INSTRUCTION)
        sys.exit()
    try: # this case handles a directory
        fileName = pathName.split(BACK_SLASH)[-1]
        codeWriter = CodeWriter(pathName + BACK_SLASH + fileName)
        #parseCommandsAndWriteOutput()
    except IOError:
        print(FILE_WRITE_ERROR)
        sys.exit()


