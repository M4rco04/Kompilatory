import sys
from antlr4 import *
from PascalLexer import PascalLexer
from PascalParser import PascalParser

def main():
    input_file = "test.pas"
    input_stream = FileStream(input_file, encoding='utf-8')

    lexer = PascalLexer(input_stream)
    
    stream = CommonTokenStream(lexer)
    
    parser = PascalParser(stream)
    
    tree = parser.program()
    
    print("Drzewo składniowe:")
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()
