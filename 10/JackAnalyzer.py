import sys
import os.path
from os import path
from JackTokenizer import JackTokenizer
from JackTokenizer import TokenType
from CompilationEngine import CompilationEngine

USAGE_INSTRUCTION = 'Usage: JackAnalyzer <file.jack or directory>'
NO_VM_FILES = 'Error: No .jack files in directory'
FILE_OPEN_ERROR = 'Error: Cannot open file'
FILE_WRITE_ERROR = 'Error: Cannot write to file'
NO_FILES_ERROR = 'No .jack files found in the directory'
XML_EXTENSION = 'xml'
JACK_EXTENSION = 'jack'
DOT = '.'
BACK_SLASH = '\\'


def check_input_folder():
    folder_name = sys.argv[1]
    if folder_name[-1] == BACK_SLASH or folder_name[-1] == '"' or folder_name[-1] == "'":
        folder_name = folder_name[:-1]
    check_folder = path.isdir(folder_name)
    if check_folder:
        return folder_name
    return None


# Checking if arguments for program are ok and if vm file exists
def check_input():
    if len(sys.argv) is not 2:
        print(USAGE_INSTRUCTION)  # too many/less arguments
        sys.exit()
    file_split = sys.argv[1].strip().split(DOT)

    if len(file_split) < 2:
        return None

    ext = file_split[-1].strip().lower()

    if ext != JACK_EXTENSION:  # not .jack extension
        return None
    file_name = '.'.join(file_split[0:-1]).strip()
    check_file = path.exists(sys.argv[1])

    if check_file is False:  # file doesn't exists/can't open file
        print(FILE_OPEN_ERROR)
        sys.exit()
    if path.isdir(sys.argv[1]):
        return None
    elif path.isfile(sys.argv[1]):
        return file_name

    return None


# running the function to parse commands and write the translation to an .asm file
def parse_commands_and_write_output():
    if (parser.has_more_tokens()):
        parser.advance()
    code_writer.compile_class()
    """while parser.has_more_tokens():
        parser.advance()
        token_type = parser.token_type()
        if (token_type == TokenType.)
        if instruction_type == CommandType.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif instruction_type in [CommandType.C_POP, CommandType.C_PUSH]:
            segment = parser.arg1()
            index = int(parser.arg2())
            code_writer.write_push_pop(instruction_type, segment, index)
        elif instruction_type == CommandType.C_LABEL:
            label_name = parser.arg1()
            code_writer.write_label(label_name)
        elif instruction_type == CommandType.C_GOTO:
            label_jump = parser.arg1()
            code_writer.write_goto(label_jump)
        elif instruction_type == CommandType.C_IF:
            label_condition = parser.arg1()
            code_writer.write_if(label_condition)
        elif instruction_type == CommandType.C_FUNCTION:
            function_name = parser.arg1()
            number_of_vars = int(parser.arg2())
            code_writer.write_function(function_name, number_of_vars)
        elif instruction_type == CommandType.C_RETURN:
            code_writer.write_return()
        elif instruction_type == CommandType.C_CALL:
            function_name = parser.arg1()
            number_of_args = int(parser.arg2())
            code_writer.write_call(function_name, number_of_args)"""


file_name = check_input()
if file_name is not None:  # this case handles single file
    parser = JackTokenizer(file_name + DOT + JACK_EXTENSION)
    try:
        code_writer = CompilationEngine(file_name, False, parser)
        parse_commands_and_write_output()
    except IOError:
        print(FILE_WRITE_ERROR)
        sys.exit()
else:
    path_name = check_input_folder()
    if path_name is None:
        print(USAGE_INSTRUCTION)
        sys.exit()
    try:  # this case handles a directory
        file_name = path_name.split(BACK_SLASH)[-1]
        files_to_parse = []
        for root, dirs, files in os.walk(path_name):
            for file_in_folder in files:
                check_extension = file_in_folder.split(DOT)[-1]
                if check_extension == JACK_EXTENSION:
                    files_to_parse.append(file_in_folder)
        number_of_files = len(files_to_parse)
        if number_of_files > 1:
            code_writer = CompilationEngine(
                path_name + BACK_SLASH + file_name, True, parser)
        elif number_of_files == 1:
            code_writer = CompilationEngine(
                path_name + BACK_SLASH + file_name, False, parser)
        else:
            print(NO_FILES_ERROR)
            sys.exit()
        for jack_file in files_to_parse:
            parser = JackTokenizer(path_name + BACK_SLASH + jack_file)
            code_writer.set_file_name(jack_file.split(DOT)[0])
            parse_commands_and_write_output()
        code_writer.close()
    except IOError:
        print(FILE_WRITE_ERROR)
        sys.exit()
