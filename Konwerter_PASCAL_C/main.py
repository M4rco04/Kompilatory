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

    def build(self):
        input_stream = FileStream(self.file_path, encoding='utf-8')
        
        lexer = PascalLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PascalParser(stream)
        
        return parser.program()

# ==========================================
# 2. Moduł generujący kod C 
# ==========================================
class CodeGeneratorVisitor(PascalVisitor):
    """Przechodzi po drzewie AST Pascala i buduje tekstowy kod C."""
    
    def __init__(self):
        self.indent_level = 0
        self.current_function = None # Służy do śledzenia czy jesteśmy wewnątrz funkcji (dla 'return')
    
    def get_indent(self):
        return "    " * self.indent_level

    def visitProgram(self, ctx: PascalParser.ProgramContext):
        program_name = ctx.IDENTIFIER().getText()
        
        c_code = f"// Wygenerowano z programu: {program_name}\n"
        c_code += "#include <stdio.h>\n"
        c_code += "#include <stdlib.h>\n"
        c_code += "#include <stdbool.h>\n\n"
        
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
                upper_bound = range_ctx.constant(1).getText()
                if upper_bound.isdigit():
                    size = str(int(upper_bound) + 1)
                else:
                    size = f"{upper_bound} + 1"
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
            identifiers.append(f"{ident.getText()}{array_dims}")
            
        return f"{c_type} {', '.join(identifiers)};\n"

    def visitSubprogramDeclarations(self, ctx: PascalParser.SubprogramDeclarationsContext):
        code = "\n"
        for decl in ctx.subprogramDeclaration():
            code += self.visit(decl) + "\n"
        return code

    def visitSubprogramDeclaration(self, ctx: PascalParser.SubprogramDeclarationContext):
        head_code, is_function, func_name = self.visit(ctx.subprogramHead())
        
        # Zapisujemy nazwę bieżącej funkcji, by móc wygenerować 'return'
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
        
        params = ""
        if ctx.formalParameterList():
            params = self.visit(ctx.formalParameterList())
            
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
            params.append(f"{c_type} {ident.getText()}")
            
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
        if ctx.getChildCount() == 0:
            return ""
            
        child_ctx = ctx.getChild(0)
        code = self.visit(child_ctx)
        
        if ctx.procedureCall():
            return code + ";"
            
        return code
    
    def visitAssignmentStatement(self, ctx: PascalParser.AssignmentStatementContext):
        var_name = self.visit(ctx.variable())
        expr = self.visit(ctx.expression())
        
        # Transformacja pascalowego zwracania funkcji (NazwaFunkcji := X) na C (return X)
        if self.current_function and var_name.lower() == self.current_function.lower():
            return f"return {expr};"
            
        return f"{var_name} = {expr};"

    def visitVariable(self, ctx: PascalParser.VariableContext):
        var_name = ctx.IDENTIFIER().getText()
        if ctx.expression():
            indices = "".join([f"[{self.visit(e)}]" for e in ctx.expression()])
            return f"{var_name}{indices}"
        return var_name

    def visitIfStatement(self, ctx: PascalParser.IfStatementContext):
        cond = self.visit(ctx.expression())
        stmt_true = self.visit(ctx.statement(0))
        
        c_code = f"if ({cond}) {{\n"
        c_code += self.get_indent() + f"    {stmt_true}\n"
        c_code += self.get_indent() + "}"
        
        if ctx.KEYWORD_ELSE():
            stmt_false = self.visit(ctx.statement(1))
            c_code += f" else {{\n"
            c_code += self.get_indent() + f"    {stmt_false}\n"
            c_code += self.get_indent() + "}"
            
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

    def visitProcedureCall(self, ctx: PascalParser.ProcedureCallContext):
        name = ctx.IDENTIFIER().getText()
        
        args_list = []
        if ctx.argumentList():
            if hasattr(ctx.argumentList(), 'argument'):
                elements = ctx.argumentList().argument()
            else:
                elements = ctx.argumentList().expression()
                
            args_list = [str(self.visit(e)).strip() for e in elements]
            
        if name.upper() in ["WRITE", "WRITELN"]:
            if not args_list:
                return 'printf("\\n")'
                
            format_str = ""
            vars_list = []
            
            for arg in args_list:
                if arg.startswith('"') and arg.endswith('"'):
                    format_str += arg[1:-1]
                else:
                    format_str += "%d"
                    vars_list.append(arg)
                    
            if name.upper() == "WRITELN":
                format_str += "\\n"
                
            if vars_list:
                c_args = ", ".join(vars_list)
                return f'printf("{format_str}", {c_args})'
            else:
                return f'printf("{format_str}")'

        if name.upper() in ["READ", "READLN"]:
            if not args_list:
                return 'getchar()'
            else:
                format_mask = " ".join(["%d"] * len(args_list))
                c_args = ", ".join([f"&{arg}" for arg in args_list])
                return f'scanf("{format_mask}", {c_args})'
                
        args_str = ", ".join(args_list) if args_list else ""
        
        if not ctx.PUNCT_LPAREN():
            if not isinstance(ctx.parentCtx, PascalParser.StatementContext):
                return name
            else:
                return f"{name}()"
                
        return f"{name}({args_str})"

    def visitExpression(self, ctx: PascalParser.ExpressionContext):
        left = self.visit(ctx.simpleExpression(0))
        if ctx.REL_OP():
            op = ctx.REL_OP().getText()
            if op == '=': op = '=='
            elif op == '<>': op = '!='
            
            right = self.visit(ctx.simpleExpression(1))
            return f"{left} {op} {right}"
        return left

    def visitSimpleExpression(self, ctx: PascalParser.SimpleExpressionContext):
        res = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()
            if op.upper() == 'OR': op = '||'
            res += f" {op} {self.visit(ctx.term(i))}"
        return res

    def visitTerm(self, ctx: PascalParser.TermContext):
        res = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()
            if op.upper() == 'AND': op = '&&'
            elif op.upper() == 'DIV': op = '/'
            elif op.upper() == 'MOD': op = '%'
            res += f" {op} {self.visit(ctx.factor(i))}"
        return res

    def visitFactor(self, ctx: PascalParser.FactorContext):
        if ctx.LOG_OP_NOT():
            return f"!{self.visit(ctx.factor(0))}"
        elif ctx.ADD_OP():
            return f"{ctx.ADD_OP().getText()}{self.visit(ctx.factor(0))}"
        elif ctx.procedureCall():
            return self.visit(ctx.procedureCall())
        elif ctx.variable():
            return self.visit(ctx.variable())
        elif ctx.NUMBER():
            return ctx.NUMBER().getText()
        elif ctx.BOOLEAN_CONST():
            return "true" if ctx.BOOLEAN_CONST().getText().upper() == "TRUE" else "false"
        elif ctx.STRING():
            val = ctx.STRING().getText()
            return f'"{val[1:-1]}"'
        elif ctx.expression():
            return f"({self.visit(ctx.expression())})"
        return ""

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
            print("Parsowanie kodu Pascala...")
            builder = ASTBuilder(self.input_file)
            tree = builder.build()
            
            print("Generowanie kodu C...")
            generator = CodeGeneratorVisitor()

            c_code = generator.visit(tree) 
            
            print("Zapisywanie pliku wynikowego...")
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(c_code)
                
            print("Translacja zakończona pomyślnie.")
            
        except Exception as e:
            print(f"Błąd kompilacji: {e}")


def main():
    if len(sys.argv) < 2:
        print("Użycie: python compiler.py <plik_wejsciowy.pas> [plik_wyjsciowy.c]")
        sys.exit(1)

    input_pascal = sys.argv[1]
    output_c = sys.argv[2] if len(sys.argv) > 2 else input_pascal.replace(".pas", ".c")
    
    compiler = CompilerCore("PASCAL_files\\" + input_pascal, "C_files\\" + output_c)
    compiler.compile()


if __name__ == '__main__':
    main()