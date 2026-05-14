import sys
from antlr4 import *
from Tools.PascalLexer import PascalLexer
from Tools.PascalParser import PascalParser
from Tools.PascalVisitor import PascalVisitor


# ==========================================
# 1. Moduł budujący drzewo
# ==========================================
class ASTBuilder:
    """Odpowiada za wczytanie pliku i zbudowanie drzewa składniowego ANTLR."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stream = None

    def build(self):
        input_stream = FileStream(self.file_path, encoding='utf-8')

        lexer = PascalLexer(input_stream)
        self.stream = CommonTokenStream(lexer)
        parser = PascalParser(self.stream)

        return parser.program()


# ==========================================
# 2. Moduł generujący kod C
# ==========================================
class CodeGeneratorVisitor(PascalVisitor):
    """Przechodzi po drzewie AST Pascala i buduje tekstowy kod C."""

    def __init__(self, token_stream=None):
        self.indent_level = 0
        self.current_function = None
        self.token_stream = token_stream  # Strumień do odczytu komentarzy
        self.processed_comments = set()  # Zbiór zapobiegający duplikatom
        self.symbol_table = {}  # Tabela typów zmiennych dla scanf

    def get_indent(self):
        return "    " * self.indent_level

    def get_comments_before(self, ctx):
        """Wyciąga komentarze z ukrytego kanału przed danym węzłem."""
        if not self.token_stream:
            return ""

        comments_code = ""
        hidden_tokens = self.token_stream.getHiddenTokensToLeft(ctx.start.tokenIndex, channel=Token.HIDDEN_CHANNEL)

        if hidden_tokens:
            for t in hidden_tokens:
                if t.tokenIndex not in self.processed_comments:
                    self.processed_comments.add(t.tokenIndex)
                    txt = t.text.strip()
                    # Konwersja na styl C
                    if txt.startswith('{'):
                        content = txt[1:-1].strip()
                        comments_code += f"/* {content} */\n{self.get_indent()}"
                    elif txt.startswith('(*'):
                        content = txt[2:-2].strip()
                        comments_code += f"/* {content} */\n{self.get_indent()}"
        return comments_code

    def visitProgram(self, ctx: PascalParser.ProgramContext):
        program_name = ctx.IDENTIFIER().getText()

        c_code = f"// Wygenerowano z programu: {program_name}\n"
        c_code += "#include <stdio.h>\n"
        c_code += "#include <stdlib.h>\n"
        c_code += "#include <stdbool.h>\n"
        c_code += "#include <time.h>\n\n"

        c_code += self.visit(ctx.block().declarations()) or ""

        c_code += "\nint main(int argc, char *argv[]) {\n"
        self.indent_level += 1

        c_code += self.visit(ctx.block().compoundStatement()) or ""

        c_code += self.get_indent() + "return 0;\n"
        self.indent_level -= 1
        c_code += "}\n"

        return c_code

    def visitDeclarations(self, ctx: PascalParser.DeclarationsContext):
        code = ""
        if ctx.variableDeclarationPart():
            code += self.visit(ctx.variableDeclarationPart())

        if ctx.subprogramDeclarations():
            code += self.visit(ctx.subprogramDeclarations())

        return code

    def visitVariableDeclarationPart(self, ctx: PascalParser.VariableDeclarationPartContext):
        code = ""
        for decl in ctx.variableDeclaration():
            code += self.get_indent() + self.visit(decl)
        return code

    def visitVariableDeclaration(self, ctx: PascalParser.VariableDeclarationContext):
        c_type = "void"
        array_dims = ""

        if ctx.type_().arrayType():
            array_ctx = ctx.type_().arrayType()
            pascal_type_ctx = array_ctx.type_().simpleType()

            for range_ctx in array_ctx.indexRange():
                # Zakładamy stałe numeryczne dla rozmiaru
                upper_bound = range_ctx.constant(1).getText()
                size = str(int(upper_bound) + 1) if upper_bound.isdigit() else f"{upper_bound} + 1"
                array_dims += f"[{size}]"
        else:
            pascal_type_ctx = ctx.type_().simpleType()

        if pascal_type_ctx:
            if pascal_type_ctx.TYPE_INTEGER() or pascal_type_ctx.TYPE_LONGINT():
                c_type = "int"
            elif pascal_type_ctx.TYPE_REAL():
                c_type = "float"
            elif pascal_type_ctx.TYPE_BOOLEAN():
                c_type = "bool"
            elif pascal_type_ctx.TYPE_CHAR():
                c_type = "char"

        identifiers = []
        for ident in ctx.identifierList().IDENTIFIER():
            name = ident.getText()
            self.symbol_table[name.lower()] = c_type  # Rejestracja w tabeli symboli
            identifiers.append(f"{name}{array_dims}")

        return f"{c_type} {', '.join(identifiers)};\n"

    def visitSubprogramDeclarations(self, ctx: PascalParser.SubprogramDeclarationsContext):
        code = "\n"
        for decl in ctx.subprogramDeclaration():
            code += self.visit(decl) + "\n"
        return code

    def visitSubprogramDeclaration(self, ctx: PascalParser.SubprogramDeclarationContext):
        head_code, is_function, func_name = self.visit(ctx.subprogramHead())
        self.current_function = func_name if is_function else None

        c_code = f"{head_code} {{\n"
        self.indent_level += 1

        local_vars = self.visit(ctx.block().declarations())
        if local_vars:
            c_code += local_vars + "\n"

        body = self.visit(ctx.block().compoundStatement())
        if body:
            c_code += body

        self.indent_level -= 1
        c_code += self.get_indent() + "}\n"

        self.current_function = None
        return c_code

    def visitSubprogramHead(self, ctx: PascalParser.SubprogramHeadContext):
        name = ctx.IDENTIFIER().getText()
        params = self.visit(ctx.formalParameterList()) if ctx.formalParameterList() else ""
        is_function = ctx.KEYWORD_FUNCTION() is not None
        c_type = "void"

        if is_function:
            pascal_type_ctx = ctx.type_().simpleType()
            if pascal_type_ctx:
                if pascal_type_ctx.TYPE_INTEGER() or pascal_type_ctx.TYPE_LONGINT():
                    c_type = "int"
                elif pascal_type_ctx.TYPE_REAL():
                    c_type = "float"
                elif pascal_type_ctx.TYPE_BOOLEAN():
                    c_type = "bool"
                elif pascal_type_ctx.TYPE_CHAR():
                    c_type = "char"

        return f"{c_type} {name}({params})", is_function, name

    def visitFormalParameterGroup(self, ctx: PascalParser.FormalParameterGroupContext):
        pascal_type_ctx = ctx.type_().simpleType()
        c_type = "void"
        if pascal_type_ctx:
            if pascal_type_ctx.TYPE_INTEGER() or pascal_type_ctx.TYPE_LONGINT():
                c_type = "int"
            elif pascal_type_ctx.TYPE_REAL():
                c_type = "float"
            elif pascal_type_ctx.TYPE_BOOLEAN():
                c_type = "bool"
            elif pascal_type_ctx.TYPE_CHAR():
                c_type = "char"

        params = []
        for ident in ctx.identifierList().IDENTIFIER():
            name = ident.getText()
            self.symbol_table[name.lower()] = c_type
            params.append(f"{c_type} {name}")
        return params

    def visitCompoundStatement(self, ctx: PascalParser.CompoundStatementContext):
        statements_code = ""
        if ctx.statementList():
            for stmt in ctx.statementList().statement():
                stmt_code = self.visit(stmt)
                if stmt_code:
                    statements_code += self.get_indent() + stmt_code + "\n"
        return statements_code

    def visitStatement(self, ctx: PascalParser.StatementContext):
        comments = self.get_comments_before(ctx)
        if ctx.getChildCount() == 0:
            return comments

        child_ctx = ctx.getChild(0)
        code = self.visit(child_ctx)

        # Dodanie średnika dla samodzielnych wywołań procedur
        if ctx.procedureCall():
            return comments + code + ";"
        return comments + code

    def visitAssignmentStatement(self, ctx: PascalParser.AssignmentStatementContext):
        var_name = self.visit(ctx.variable())
        expr = self.visit(ctx.expression())

        if self.current_function and var_name.lower() == self.current_function.lower():
            return f"return {expr};"
        return f"{var_name} = {expr};"

    def visitCaseStatement(self, ctx: PascalParser.CaseStatementContext):
        expr = self.visit(ctx.expression())
        c_code = f"switch ({expr}) {{\n"
        self.indent_level += 1
        for case_elem in ctx.caseElement():
            c_code += self.visit(case_elem)
        self.indent_level -= 1
        c_code += self.get_indent() + "}"
        return c_code

    def visitCaseElement(self, ctx: PascalParser.CaseElementContext):
        c_code = ""
        for const in ctx.caseLabelList().constant():
            c_code += self.get_indent() + f"case {const.getText()}:\n"

        self.indent_level += 1
        stmt = self.visit(ctx.statement())
        if stmt:
            c_code += self.get_indent() + f"{stmt}\n"
        c_code += self.get_indent() + "break;\n"
        self.indent_level -= 1
        return c_code

    def visitProcedureCall(self, ctx: PascalParser.ProcedureCallContext):
        name = ctx.IDENTIFIER().getText()
        args_list = []
        if ctx.argumentList():
            elements = ctx.argumentList().expression()
            args_list = [str(self.visit(e)).strip() for e in elements]

        u_name = name.upper()
        if u_name == "RANDOMIZE": return "srand(time(NULL))"
        if u_name == "RANDOM":
            return f"(rand() % {args_list[0]})" if args_list else "rand()"

        if u_name in ["WRITE", "WRITELN"]:
            if not args_list: return 'printf("\\n")'
            format_str, vars_list = "", []
            for arg in args_list:
                if arg.startswith('"') and arg.endswith('"'):
                    format_str += arg[1:-1]
                else:
                    format_str += "%d "
                    vars_list.append(arg)
            if u_name == "WRITELN": format_str = format_str.rstrip() + "\\n"
            return f'printf("{format_str}"{", " + ", ".join(vars_list) if vars_list else ""})'

        if u_name in ["READ", "READLN"]:
            if not args_list: return 'getchar()'
            format_mask = ""
            for arg in args_list:
                clean_name = arg.split('[')[0].lower()
                v_type = self.symbol_table.get(clean_name, "int")
                format_mask += "%f " if v_type == "float" else "%c " if v_type == "char" else "%d "
            c_args = ", ".join([f"&{arg}" for arg in args_list])
            return f'scanf("{format_mask.strip()}", {c_args})'

        args_str = ", ".join(args_list) if args_list else ""
        if not ctx.PUNCT_LPAREN():
            return name if not isinstance(ctx.parentCtx, PascalParser.StatementContext) else f"{name}()"
        return f"{name}({args_str})"

    def visitExpression(self, ctx: PascalParser.ExpressionContext):
        left = self.visit(ctx.simpleExpression(0))
        if ctx.REL_OP():
            op = ctx.REL_OP().getText()
            op = '==' if op == '=' else '!=' if op == '<>' else op
            return f"{left} {op} {self.visit(ctx.simpleExpression(1))}"
        return left

    def visitSimpleExpression(self, ctx: PascalParser.SimpleExpressionContext):
        res = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()
            op = '||' if op.upper() == 'OR' else op
            res += f" {op} {self.visit(ctx.term(i))}"
        return res

    def visitTerm(self, ctx: PascalParser.TermContext):
        res = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()
            op = '&&' if op.upper() == 'AND' else '/' if op.upper() == 'DIV' else '%' if op.upper() == 'MOD' else op
            res += f" {op} {self.visit(ctx.factor(i))}"
        return res

    def visitFactor(self, ctx: PascalParser.FactorContext):
        if ctx.LOG_OP_NOT(): return f"!{self.visit(ctx.factor(0))}"
        if ctx.ADD_OP(): return f"{ctx.ADD_OP().getText()}{self.visit(ctx.factor(0))}"
        if ctx.procedureCall(): return self.visit(ctx.procedureCall())
        if ctx.variable(): return self.visit(ctx.variable())
        if ctx.NUMBER(): return ctx.NUMBER().getText()
        if ctx.BOOLEAN_CONST(): return "true" if ctx.BOOLEAN_CONST().getText().upper() == "TRUE" else "false"
        if ctx.STRING(): return f'"{ctx.STRING().getText()[1:-1]}"'
        if ctx.expression(): return f"({self.visit(ctx.expression())})"
        return ""

    def visitVariable(self, ctx: PascalParser.VariableContext):
        var_name = ctx.IDENTIFIER().getText()
        if ctx.expression():
            indices = "".join([f"[{self.visit(e)}]" for e in ctx.expression()])
            return f"{var_name}{indices}"
        return var_name

    def defaultResult(self):
        return ""


# ==========================================
# 3. Kompilator
# ==========================================
class CompilerCore:
    """Zarządza procesem kompilacji źródło-źródło."""

    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def compile(self):
        print(f"Rozpoczynam translację: {self.input_file} -> {self.output_file}")
        try:
            builder = ASTBuilder(self.input_file)
            tree = builder.build()
            generator = CodeGeneratorVisitor(builder.stream)  # Przekazanie strumienia tokenów
            c_code = generator.visit(tree)

            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(c_code)
            print("Translacja zakończona pomyślnie.")
        except Exception as e:
            print(f"Błąd kompilacji: {e}")


def main():
    if len(sys.argv) < 2:
        print("Użycie: python main.py <plik_wejsciowy.pas> [plik_wyjsciowy.c]")
        sys.exit(1)
    input_pascal = sys.argv[1]
    output_c = sys.argv[2] if len(sys.argv) > 2 else input_pascal.replace(".pas", ".c")
    compiler = CompilerCore("PASCAL_files\\" + input_pascal, "C_files\\" + output_c)
    compiler.compile()


if __name__ == '__main__':
    main()