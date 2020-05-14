from Parser import *
from Code import Code
from SymbolTable import SymbolTable


parser = Parser('test.txt')
symbolTable = SymbolTable()
while (parser.hasMoreLines):
    parser.advance()
    if (parser.instructionType == Command_Type.L_INSTRUCTION):
        symbolTable.addEntry(parser.symbol, parser.nextLine - 1)

parser = Parser('test.txt')
while (parser.hasMoreLines):
    parser.advance()
    if (parser.instructionType == Command_Type.A_INSTRUCTION):
        symbol = parser.symbol()
        if (symbolTable.contains(symbol) == False):
            symbolTable.addEntry(symbol, parser.nextLine - 1)
        
