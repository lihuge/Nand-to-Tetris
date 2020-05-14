JUMP_DICTIONARY = {'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110',
             'JMP':'111'}
DEST_DICTIONARY = {'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'ADM':'111'}
COMP_DICTIONARY = {'0':'110101010', '1':'110111111', '-1':'110111010', 'D':'110001100', 'A':'110110000',
            '!D':'110001101', '!A':'110001111', '-D':'110001111', '-A':'110110011', 'D+1':'110011111',
            'A+1':'110110111', 'D-1':'110001110', 'A-1':'110110010', 'D+A':'110000010','D-A':'110010011',
            'A-D':'110000111', 'D&A':'110000000', 'D|A':'110010101', 'M':'111110000', '!M':'111110001',
            '-M':'111110011', 'M+1':'111110111', 'M-1':'111110010', 'D+M':'111000010', 'D-M':'111010011',
            'M-D':'111000111', 'D&M':'111000000', 'D|M':'111010101'}


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
