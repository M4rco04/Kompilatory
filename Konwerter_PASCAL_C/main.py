import sys
import os
from antlr4 import *
from Tools.PascalLexer import PascalLexer
from Tools.PascalParser import PascalParser
from Tools.PascalVisitor import PascalVisitor

# Importujemy naszą nową obsługę błędów
from error_handler import CustomErrorListener, SymbolTable, CompilerException


# ==========================================
# 1. Moduł budujący drzewo (z obsługą błędów)
# ==========================================
class ASTBuilder:
    """Odpowiada za wczytanie pliku i zbudowanie drzewa składniowego ANTLR."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stream = None

    def build(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {self.file_path}")

        input_stream = FileStream(self.file_path, encoding='utf-8')

        # Inicjalizacja Lexera
        lexer = PascalLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(CustomErrorListener())

        # Inicjalizacja strumienia i Parsera
        self.stream = CommonTokenStream(lexer)
        parser = PascalParser(self.stream)
        parser.removeErrorListeners()
        parser.addErrorListener(CustomErrorListener())

        return parser.program()


# ==========================================
# 2. Moduł generujący kod C
# ==========================================
class CodeGeneratorVisitor(PascalVisitor):
    """Przechodzi po drzewie AST Pascala i buduje tekstowy kod C."""

    def __init__(self, token_stream=None):
        self.indent_level = 0
        self.current_function = None
        self.token_stream = token_stream
        self.processed_comments = set()
        self.symbol_table = SymbolTable()

    def get_indent(self):
        return "    " * self.indent_level

    def get_comments_before(self, ctx):
        if not self.token_stream: return ""
        comments_code = ""
        hidden_tokens = self.token_stream.getHiddenTokensToLeft(ctx.start.tokenIndex, channel=Token.HIDDEN_CHANNEL)

        if hidden_tokens:
            for t in hidden_tokens:
                if t.tokenIndex not in self.processed_comments:
                    self.processed_comments.add(t.tokenIndex)
                    txt = t.text.strip()
                    if txt.startswith('{'):
                        comments_code += f"/* {txt[1:-1].strip()} */\n{self.get_indent()}"
                    elif txt.startswith('(*'):
                        comments_code += f"/* {txt[2:-2].strip()} */\n{self.get_indent()}"
        return comments_code

    # --- Struktura główna i deklaracje ---

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
                upper = range_ctx.constant(1).getText()
                size = str(int(upper) + 1) if upper.isdigit() else f"{upper} + 1"
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
            line = ident.getSymbol().line
            self.symbol_table.declare_variable(name, c_type, line)
            identifiers.append(f"{name}{array_dims}")

        return f"{c_type} {', '.join(identifiers)};\n"

    def visitSubprogramDeclarations(self, ctx: PascalParser.SubprogramDeclarationsContext):
        code = "\n"
        for decl in ctx.subprogramDeclaration():
            code += self.visit(decl) + "\n"
        return code

    def visitSubprogramDeclaration(self, ctx: PascalParser.SubprogramDeclarationContext):
        self.symbol_table.enter_scope()

        head_code, is_function, func_name = self.visit(ctx.subprogramHead())
        self.current_function = func_name if is_function else None

        c_code = f"{head_code} {{\n"
        self.indent_level += 1

        local_vars = self.visit(ctx.block().declarations())
        if local_vars: c_code += local_vars + "\n"

        body = self.visit(ctx.block().compoundStatement())
        if body: c_code += body

        self.indent_level -= 1
        c_code += self.get_indent() + "}\n"

        self.current_function = None
        self.symbol_table.exit_scope()
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

    def visitFormalParameterList(self, ctx: PascalParser.FormalParameterListContext):
        params = []
        for group in ctx.formalParameterGroup():
            params.extend(self.visit(group))
        return ", ".join(params)

    def visitFormalParameterGroup(self, ctx: PascalParser.FormalParameterGroupContext):
        pascal_type_ctx = ctx.type_().simpleType()
        c_type = "int"
        if pascal_type_ctx:
            if pascal_type_ctx.TYPE_REAL():
                c_type = "float"
            elif pascal_type_ctx.TYPE_BOOLEAN():
                c_type = "bool"
            elif pascal_type_ctx.TYPE_CHAR():
                c_type = "char"

        params = []
        for ident in ctx.identifierList().IDENTIFIER():
            name = ident.getText()
            self.symbol_table.declare_variable(name, c_type, ident.getSymbol().line)
            params.append(f"{c_type} {name}")
        return params

    # --- Przetwarzanie Instrukcji ---

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
        if ctx.getChildCount() == 0: return comments

        child_ctx = ctx.getChild(0)
        code = self.visit(child_ctx)

        if code is None:
            code = ""

        if ctx.procedureCall():
            return comments + code + ";"
        return comments + code

    def visitAssignmentStatement(self, ctx: PascalParser.AssignmentStatementContext):
        var_name = self.visit(ctx.variable())
        expr = self.visit(ctx.expression())

        if self.current_function and var_name.lower() == self.current_function.lower():
            return f"return {expr};"
        return f"{var_name} = {expr};"

    def visitVariable(self, ctx: PascalParser.VariableContext):
        var_name = ctx.IDENTIFIER().getText()
        line = ctx.IDENTIFIER().getSymbol().line

        is_return_target = self.current_function and var_name.lower() == self.current_function.lower()
        if not is_return_target:
            self.symbol_table.get_variable_type(var_name, line)

        if ctx.expression():
            indices = "".join([f"[{self.visit(e)}]" for e in ctx.expression()])
            return f"{var_name}{indices}"
        return var_name

    def visitIfStatement(self, ctx: PascalParser.IfStatementContext):
        cond = self.visit(ctx.expression())
        stmt_true = self.visit(ctx.statement(0))
        c_code = f"if ({cond}) {{\n{self.get_indent()}    {stmt_true}\n{self.get_indent()}}}"

        if ctx.KEYWORD_ELSE():
            stmt_false = self.visit(ctx.statement(1))
            c_code += f" else {{\n{self.get_indent()}    {stmt_false}\n{self.get_indent()}}}"
        return c_code

    def visitWhileStatement(self, ctx: PascalParser.WhileStatementContext):
        cond = self.visit(ctx.expression())
        stmt = self.visit(ctx.statement())
        return f"while ({cond}) {{\n{self.get_indent()}    {stmt}\n{self.get_indent()}}}"

    def visitForStatement(self, ctx: PascalParser.ForStatementContext):
        var_name = ctx.IDENTIFIER().getText()
        start_expr = self.visit(ctx.expression(0))
        end_expr = self.visit(ctx.expression(1))
        stmt = self.visit(ctx.statement())
        return f"for ({var_name} = {start_expr}; {var_name} <= {end_expr}; {var_name}++) {{\n{self.get_indent()}    {stmt}\n{self.get_indent()}}}"

    def visitRepeatStatement(self, ctx: PascalParser.RepeatStatementContext):
        cond = self.visit(ctx.expression())
        stmts_code = ""
        for stmt in ctx.statementList().statement():
            stmt_code = self.visit(stmt)
            if stmt_code:
                stmts_code += self.get_indent() + "    " + stmt_code + "\n"
        return f"do {{\n{stmts_code}{self.get_indent()}}} while (!({cond}));"

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
        if stmt: c_code += self.get_indent() + f"{stmt}\n"
        c_code += self.get_indent() + "break;\n"
        self.indent_level -= 1
        return c_code

    def visitProcedureCall(self, ctx: PascalParser.ProcedureCallContext):
        name = ctx.IDENTIFIER().getText()
        u_name = name.upper()
        args_list = []
        if ctx.argumentList():
            args_list = [str(self.visit(e)).strip() for e in ctx.argumentList().expression()]

        if u_name == "RANDOMIZE": return "srand(time(NULL))"
        if u_name == "RANDOM": return f"(rand() % {args_list[0]})" if args_list else "rand()"

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
                clean_name = arg.split('[')[0]
                v_type = self.symbol_table.get_variable_type(clean_name, ctx.IDENTIFIER().getSymbol().line)
                format_mask += "%f " if v_type == "float" else "%c " if v_type == "char" else "%d "
            c_args = ", ".join([f"&{arg}" for arg in args_list])
            return f'scanf("{format_mask.strip()}", {c_args})'

        args_str = ", ".join(args_list) if args_list else ""
        if not ctx.PUNCT_LPAREN():
            return name if not isinstance(ctx.parentCtx, PascalParser.StatementContext) else f"{name}()"
        return f"{name}({args_str})"

    # --- Wyrażenia ---

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

    def defaultResult(self):
        return ""


# ==========================================
# 3. Kompilator (Core)
# ==========================================
class CompilerCore:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def compile(self):
        print(f"--- ROZPOCZĘTO TRANSLACJĘ ---")
        print(f"Plik wejściowy: {self.input_file}")

        try:
            builder = ASTBuilder(self.input_file)
            tree = builder.build()

            generator = CodeGeneratorVisitor(builder.stream)
            c_code = generator.visit(tree)

            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(c_code)

            print(f"SUKCES: Zapisano do {self.output_file}")

        except CompilerException as e:
            print(f"\n[!] BŁĄD KOMPILACJI: {e}")
        except FileNotFoundError as e:
            print(f"\n[!] BŁĄD PLIKU: {e}")
        except Exception as e:
            print(f"\n[!] BŁĄD KRYTYCZNY (PYTHON): {e}")


def main():
    if len(sys.argv) < 2:
        print("Użycie: python main.py <nazwa_pliku.pas> [wynik.c]")
        sys.exit(1)

    input_pas = sys.argv[1]
    path_in = os.path.join("PASCAL_files", input_pas)
    output_name = sys.argv[2] if len(sys.argv) > 2 else input_pas.replace(".pas", ".c")
    path_out = os.path.join("C_files", output_name)

    compiler = CompilerCore(path_in, path_out)
    compiler.compile()


if __name__ == '__main__':
    main()