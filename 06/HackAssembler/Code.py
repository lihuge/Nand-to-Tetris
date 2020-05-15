JUMP_DICTIONARY = {'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110',
             'JMP':'111'}
DEST_DICTIONARY = {'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'ADM':'111'}
COMP_DICTIONARY = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000',
            '!D':'0001101', '!A':'0110001', '-D':'0001111', '-A':'0110011', 'D+1':'0011111',
            'A+1':'0110111', 'D-1':'0001110', 'A-1':'0110010', 'D+A':'0000010','D-A':'0010011',
            'A-D':'0000111', 'D&A':'0000000', 'D|A':'0010101', 'M':'1110000', '!M':'1110001',
            '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010', 'D+M':'1000010', 'D-M':'1010011',
            'M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101'}


class Code:

    @staticmethod
    def dest(destString):
        if destString in DEST_DICTIONARY:
            return DEST_DICTIONARY[destString]
        else:
            return '000'

    @staticmethod
    def comp(compString):
        if compString in COMP_DICTIONARY:
            return COMP_DICTIONARY[compString]
        else:
            return '0000000'

    @staticmethod
    def jump(jumpString):
        if jumpString in JUMP_DICTIONARY:
            return JUMP_DICTIONARY[jumpString]
        else:
            return '000'
