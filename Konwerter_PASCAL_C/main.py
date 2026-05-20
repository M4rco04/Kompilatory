import sys
import os
from antlr4 import *
from Tools.PascalLexer import PascalLexer
from Tools.PascalParser import PascalParser
from Tools.PascalVisitor import PascalVisitor

from error_handler import CustomErrorListener, SymbolTable, CompilerException


class ASTBuilder:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stream = None

    def build(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {self.file_path}")

        input_stream = FileStream(self.file_path, encoding='utf-8')

        lexer = PascalLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(CustomErrorListener())

        self.stream = CommonTokenStream(lexer)
        parser = PascalParser(self.stream)
        parser.removeErrorListeners()
        parser.addErrorListener(CustomErrorListener())

        return parser.program()


class CodeGeneratorVisitor(PascalVisitor):
    def __init__(self, token_stream=None):
        self.indent_level = 0
        self.current_function = None
        self.function_has_returned = False
        self.token_stream = token_stream
        self.processed_comments = set()
        self.symbol_table = SymbolTable()
        self.uses_concat = False

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

    # ==========================================
    # SYSTEM INFERENCJI TYPÓW
    # ==========================================
    def infer_type(self, ctx):
        if not ctx: return "void"

        if isinstance(ctx, PascalParser.ExpressionContext):
            if ctx.REL_OP(): return "bool"
            return self.infer_type(ctx.simpleExpression(0))

        if isinstance(ctx, PascalParser.SimpleExpressionContext):
            t = self.infer_type(ctx.term(0))
            for i in range(1, len(ctx.term())):
                op = ctx.getChild(2 * i - 1).getText().upper()
                if op == 'OR': return "bool"
                t2 = self.infer_type(ctx.term(i))
                if t == "float" or t2 == "float": t = "float"
            return t

        if isinstance(ctx, PascalParser.TermContext):
            t = self.infer_type(ctx.factor(0))
            for i in range(1, len(ctx.factor())):
                op = ctx.getChild(2 * i - 1).getText().upper()
                if op == 'AND': return "bool"
                if op == '/': return "float"
                if op in ['DIV', 'MOD']: return "int"
                t2 = self.infer_type(ctx.factor(i))
                if t == "float" or t2 == "float": t = "float"
            return t

        if isinstance(ctx, PascalParser.FactorContext):
            if ctx.LOG_OP_NOT(): return "bool"
            if ctx.ADD_OP(): return self.infer_type(ctx.factor(0))

            if ctx.NUMBER():
                return "float" if '.' in ctx.NUMBER().getText() else "int"
            if ctx.BOOLEAN_CONST(): return "bool"

            if ctx.STRING():
                text = ctx.STRING().getText()
                if len(text) == 3 or (len(text) == 4 and text == "''''"):
                    return "char"
                return "string"

            if ctx.variable():
                var_name = ctx.variable().IDENTIFIER().getText()
                line = ctx.variable().IDENTIFIER().getSymbol().line
                var_type = self.symbol_table.get_variable_type(var_name, line)
                if ctx.variable().expression():
                    return var_type.replace("_array", "")
                return var_type

            if ctx.procedureCall():
                func_name = ctx.procedureCall().IDENTIFIER().getText()
                line = ctx.procedureCall().IDENTIFIER().getSymbol().line

                # ZABEZPIECZENIE: Sprawdzamy czy to nie jest zmienna zinterpretowana przez parser jako funkcja!
                if not ctx.procedureCall().PUNCT_LPAREN() and self.symbol_table.is_variable(func_name):
                    return self.symbol_table.get_variable_type(func_name, line).replace("_array", "")

                func_info = self.symbol_table.get_function_info(func_name, line)
                return func_info['return_type']

            if ctx.expression():
                return self.infer_type(ctx.expression())

        return "void"

    # --- Struktura główna i deklaracje ---
    def visitProgram(self, ctx: PascalParser.ProgramContext):
        program_name = ctx.IDENTIFIER().getText()

        decl_code = self.visit(ctx.block().declarations()) or ""

        self.indent_level += 1
        main_body = self.visit(ctx.block().compoundStatement()) or ""
        self.indent_level -= 1

        c_code = f"// Wygenerowano z programu: {program_name}\n"
        c_code += "#include <stdio.h>\n"
        c_code += "#include <stdlib.h>\n"
        c_code += "#include <stdbool.h>\n"
        c_code += "#include <string.h>\n"
        c_code += "#include <time.h>\n\n"

        if self.uses_concat:
            c_code += "/* Helper do obslugi tekstow z Pascala */\n"
            c_code += "char* _concat(const char* s1, const char* s2) {\n"
            c_code += "    char* res = (char*)malloc(strlen(s1) + strlen(s2) + 1);\n"
            c_code += "    strcpy(res, s1); strcat(res, s2); return res;\n}\n\n"

        c_code += decl_code

        c_code += "\nint main(int argc, char *argv[]) {\n"

        c_code += main_body

        c_code += self.get_indent() + "return 0;\n"
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
        is_array = False

        if ctx.type_().arrayType():
            is_array = True
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
            self.symbol_table.declare_variable(name, c_type, line, is_array)
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
        self.function_has_returned = False

        c_code = self.get_indent() + f"{head_code} {{\n"
        self.indent_level += 1

        local_vars = self.visit(ctx.block().declarations())
        if local_vars: c_code += local_vars + "\n"

        body = self.visit(ctx.block().compoundStatement())
        if body: c_code += body

        if is_function and not self.function_has_returned:
            line = ctx.subprogramHead().IDENTIFIER().getSymbol().line
            raise SemanticError(
                f"Brak wartości zwracanej (Linia {line}): Funkcja '{func_name}' nie zwraca wyniku na każdej ścieżce wykonania.")

        self.indent_level -= 1
        c_code += self.get_indent() + "}\n"

        self.current_function = None
        self.symbol_table.exit_scope()
        return c_code

    def visitSubprogramHead(self, ctx: PascalParser.SubprogramHeadContext):
        name = ctx.IDENTIFIER().getText()
        line = ctx.IDENTIFIER().getSymbol().line
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

        params_code, param_types = "", []
        if ctx.formalParameterList():
            params_code, param_types = self.visit(ctx.formalParameterList())

        self.symbol_table.declare_function(name, c_type, param_types, line)

        return f"{c_type} {name}({params_code})", is_function, name

    def visitFormalParameterList(self, ctx: PascalParser.FormalParameterListContext):
        params = []
        param_types = []
        for group in ctx.formalParameterGroup():
            g_params, g_types = self.visit(group)
            params.extend(g_params)
            param_types.extend(g_types)
        return ", ".join(params), param_types

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
        param_types = []
        for ident in ctx.identifierList().IDENTIFIER():
            name = ident.getText()
            self.symbol_table.declare_variable(name, c_type, ident.getSymbol().line)
            params.append(f"{c_type} {name}")
            param_types.append(c_type)
        return params, param_types

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

        code = self.visit(ctx.getChild(0)) or ""
        if ctx.procedureCall():
            return comments + code + ";"
        return comments + code

    def visitAssignmentStatement(self, ctx: PascalParser.AssignmentStatementContext):
        var_name = self.visit(ctx.variable())
        expr_code = self.visit(ctx.expression())

        line = ctx.variable().IDENTIFIER().getSymbol().line
        inferred_expr_type = self.infer_type(ctx.expression())

        if self.current_function and var_name.lower() == self.current_function.lower():
            expected_type = self.symbol_table.get_function_info(self.current_function, line)['return_type']
            self.symbol_table.check_type_compatibility(expected_type, inferred_expr_type, line,
                                                       "Zwracanie wartości funkcji")

            self.function_has_returned = True
            return f"return {expr_code};"

        else:
            clean_var_name = ctx.variable().IDENTIFIER().getText()
            expected_type = self.symbol_table.get_variable_type(clean_var_name, line)

            if ctx.variable().expression():
                expected_type = expected_type.replace("_array", "")

            self.symbol_table.check_type_compatibility(expected_type, inferred_expr_type, line,
                                                       f"Przypisanie do '{clean_var_name}'")
            return f"{var_name} = {expr_code};"

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

        stmt_true = self.format_statement_body(ctx.statement(0))
        c_code = f"if ({cond}) {{{stmt_true}}}"

        if ctx.KEYWORD_ELSE():
            stmt_false = self.format_statement_body(ctx.statement(1))
            c_code += f" else {{{stmt_false}}}"

        return c_code

    def visitWhileStatement(self, ctx: PascalParser.WhileStatementContext):
        cond = self.visit(ctx.expression())
        body = self.format_statement_body(ctx.statement())
        return f"while ({cond}) {{{body}}}"

    def visitForStatement(self, ctx: PascalParser.ForStatementContext):
        var_name = ctx.IDENTIFIER().getText()
        start_expr = self.visit(ctx.expression(0))
        end_expr = self.visit(ctx.expression(1))
        body = self.format_statement_body(ctx.statement())
        return f"for ({var_name} = {start_expr}; {var_name} <= {end_expr}; {var_name}++) {{{body}}}"

    def visitRepeatStatement(self, ctx: PascalParser.RepeatStatementContext):
        cond = self.visit(ctx.expression())
        stmts_code = ""
        self.indent_level += 1
        if ctx.statementList():
            for stmt in ctx.statementList().statement():
                stmt_code = self.visit(stmt)
                if stmt_code:
                    stmts_code += self.get_indent() + stmt_code + "\n"
        self.indent_level -= 1
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
        if stmt:
            is_compound = ctx.statement().compoundStatement() is not None
            if is_compound:
                c_code += stmt
            else:
                c_code += self.get_indent() + f"{stmt}\n"
        c_code += self.get_indent() + "break;\n"
        self.indent_level -= 1
        return c_code

    def visitProcedureCall(self, ctx: PascalParser.ProcedureCallContext):
        name = ctx.IDENTIFIER().getText()
        u_name = name.upper()
        line = ctx.IDENTIFIER().getSymbol().line

        # ZABEZPIECZENIE: Zwróć zmienną, jeśli parser błędnie sklasyfikował ją jako funkcję
        if not ctx.PUNCT_LPAREN() and self.symbol_table.is_variable(name):
            return name

        args_list = []
        args_types = []
        if ctx.argumentList():
            args_list = [str(self.visit(e)).strip() for e in ctx.argumentList().expression()]
            args_types = [self.infer_type(e) for e in ctx.argumentList().expression()]

        func_info = self.symbol_table.get_function_info(name, line)
        if func_info['params'] != "any":
            expected_args = func_info['params']
            if len(expected_args) != len(args_types):
                raise SemanticError(
                    f"Nieprawidłowa liczba argumentów (Linia {line}): Wywołano '{name}' z {len(args_types)} argumentami, oczekiwano {len(expected_args)}.")

            for i, (exp, act) in enumerate(zip(expected_args, args_types)):
                self.symbol_table.check_type_compatibility(exp, act, line, f"Argument nr {i + 1} funkcji '{name}'")

        if u_name == "LENGTH": return f"strlen({args_list[0]})"
        if u_name == "CONCAT":
            self.uses_concat = True
            return f"_concat({args_list[0]}, {args_list[1]})"
        if u_name == "RANDOMIZE": return "srand(time(NULL))"
        if u_name == "RANDOM": return f"(rand() % {args_list[0]})" if args_list else "rand()"

        if u_name in ["WRITE", "WRITELN"]:
            if not args_list: return 'printf("\\n")'
            format_str, vars_list = "", []
            for arg, arg_type in zip(args_list, args_types):
                if arg.startswith('"') and arg.endswith('"'):
                    format_str += arg[1:-1]
                elif arg_type == "float":
                    format_str += "%f "; vars_list.append(arg)
                elif arg_type == "char":
                    format_str += "%c "; vars_list.append(arg)
                elif arg_type == "string":
                    format_str += "%s "; vars_list.append(arg)
                else:
                    format_str += "%d "; vars_list.append(arg)
            if u_name == "WRITELN": format_str = format_str.rstrip() + "\\n"
            return f'printf("{format_str}"{", " + ", ".join(vars_list) if vars_list else ""})'

        if u_name in ["READ", "READLN"]:
            if not args_list: return 'getchar()'
            format_mask = ""
            for arg, arg_type in zip(args_list, args_types):
                if arg_type == "float":
                    format_mask += "%f "
                elif arg_type == "char":
                    format_mask += "%c "
                elif arg_type == "string":
                    format_mask += "%s "
                else:
                    format_mask += "%d "
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
        if ctx.STRING():
            text = ctx.STRING().getText()
            if len(text) == 3:
                return f"'{text[1:-1]}'"

            if len(text) == 4 and text == "''''":
                return "'\\''"

            inner_text = text[1:-1]
            inner_text = inner_text.replace('"', '\\"')
            inner_text = inner_text.replace("''", "'")
            return f'"{inner_text}"'
        if ctx.expression(): return f"({self.visit(ctx.expression())})"
        return ""

    def defaultResult(self):
        return ""

    def format_statement_body(self, stmt_ctx):
        self.indent_level += 1
        stmt_code = self.visit(stmt_ctx) or ""

        is_compound = stmt_ctx.compoundStatement() is not None
        if is_compound:
            self.indent_level -= 1
            return f"\n{stmt_code}{self.get_indent()}" if stmt_code else f"\n{self.get_indent()}"
        else:
            if not stmt_code.strip():
                self.indent_level -= 1
                return f"\n{self.get_indent()}"
            formatted = f"\n{self.get_indent()}{stmt_code}\n"
            self.indent_level -= 1
            formatted += self.get_indent()
            return formatted


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