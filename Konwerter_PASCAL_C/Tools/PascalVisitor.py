# Generated from Pascal.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PascalParser import PascalParser
else:
    from PascalParser import PascalParser

# This class defines a complete generic visitor for a parse tree produced by PascalParser.

class PascalVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PascalParser#program.
    def visitProgram(self, ctx:PascalParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#block.
    def visitBlock(self, ctx:PascalParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#declarations.
    def visitDeclarations(self, ctx:PascalParser.DeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variableDeclarationPart.
    def visitVariableDeclarationPart(self, ctx:PascalParser.VariableDeclarationPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:PascalParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#identifierList.
    def visitIdentifierList(self, ctx:PascalParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#type.
    def visitType(self, ctx:PascalParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#simpleType.
    def visitSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#arrayType.
    def visitArrayType(self, ctx:PascalParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#indexRange.
    def visitIndexRange(self, ctx:PascalParser.IndexRangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#sign.
    def visitSign(self, ctx:PascalParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#subprogramDeclarations.
    def visitSubprogramDeclarations(self, ctx:PascalParser.SubprogramDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#subprogramDeclaration.
    def visitSubprogramDeclaration(self, ctx:PascalParser.SubprogramDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#subprogramHead.
    def visitSubprogramHead(self, ctx:PascalParser.SubprogramHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#formalParameterList.
    def visitFormalParameterList(self, ctx:PascalParser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#formalParameterGroup.
    def visitFormalParameterGroup(self, ctx:PascalParser.FormalParameterGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#variable.
    def visitVariable(self, ctx:PascalParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#compoundStatement.
    def visitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#statementList.
    def visitStatementList(self, ctx:PascalParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#statement.
    def visitStatement(self, ctx:PascalParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:PascalParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseStatement.
    def visitCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseElement.
    def visitCaseElement(self, ctx:PascalParser.CaseElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#caseLabelList.
    def visitCaseLabelList(self, ctx:PascalParser.CaseLabelListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#constant.
    def visitConstant(self, ctx:PascalParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#procedureCall.
    def visitProcedureCall(self, ctx:PascalParser.ProcedureCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#argumentList.
    def visitArgumentList(self, ctx:PascalParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#ifStatement.
    def visitIfStatement(self, ctx:PascalParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#whileStatement.
    def visitWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#repeatStatement.
    def visitRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#forStatement.
    def visitForStatement(self, ctx:PascalParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#expression.
    def visitExpression(self, ctx:PascalParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#simpleExpression.
    def visitSimpleExpression(self, ctx:PascalParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#term.
    def visitTerm(self, ctx:PascalParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PascalParser#factor.
    def visitFactor(self, ctx:PascalParser.FactorContext):
        return self.visitChildren(ctx)



del PascalParser