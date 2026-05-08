# Generated from Pascal.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PascalParser import PascalParser
else:
    from PascalParser import PascalParser

# This class defines a complete listener for a parse tree produced by PascalParser.
class PascalListener(ParseTreeListener):

    # Enter a parse tree produced by PascalParser#program.
    def enterProgram(self, ctx:PascalParser.ProgramContext):
        pass

    # Exit a parse tree produced by PascalParser#program.
    def exitProgram(self, ctx:PascalParser.ProgramContext):
        pass


    # Enter a parse tree produced by PascalParser#block.
    def enterBlock(self, ctx:PascalParser.BlockContext):
        pass

    # Exit a parse tree produced by PascalParser#block.
    def exitBlock(self, ctx:PascalParser.BlockContext):
        pass


    # Enter a parse tree produced by PascalParser#declarations.
    def enterDeclarations(self, ctx:PascalParser.DeclarationsContext):
        pass

    # Exit a parse tree produced by PascalParser#declarations.
    def exitDeclarations(self, ctx:PascalParser.DeclarationsContext):
        pass


    # Enter a parse tree produced by PascalParser#variableDeclarationPart.
    def enterVariableDeclarationPart(self, ctx:PascalParser.VariableDeclarationPartContext):
        pass

    # Exit a parse tree produced by PascalParser#variableDeclarationPart.
    def exitVariableDeclarationPart(self, ctx:PascalParser.VariableDeclarationPartContext):
        pass


    # Enter a parse tree produced by PascalParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:PascalParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:PascalParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#identifierList.
    def enterIdentifierList(self, ctx:PascalParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by PascalParser#identifierList.
    def exitIdentifierList(self, ctx:PascalParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by PascalParser#type.
    def enterType(self, ctx:PascalParser.TypeContext):
        pass

    # Exit a parse tree produced by PascalParser#type.
    def exitType(self, ctx:PascalParser.TypeContext):
        pass


    # Enter a parse tree produced by PascalParser#simpleType.
    def enterSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#simpleType.
    def exitSimpleType(self, ctx:PascalParser.SimpleTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#arrayType.
    def enterArrayType(self, ctx:PascalParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by PascalParser#arrayType.
    def exitArrayType(self, ctx:PascalParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by PascalParser#indexRange.
    def enterIndexRange(self, ctx:PascalParser.IndexRangeContext):
        pass

    # Exit a parse tree produced by PascalParser#indexRange.
    def exitIndexRange(self, ctx:PascalParser.IndexRangeContext):
        pass


    # Enter a parse tree produced by PascalParser#sign.
    def enterSign(self, ctx:PascalParser.SignContext):
        pass

    # Exit a parse tree produced by PascalParser#sign.
    def exitSign(self, ctx:PascalParser.SignContext):
        pass


    # Enter a parse tree produced by PascalParser#subprogramDeclarations.
    def enterSubprogramDeclarations(self, ctx:PascalParser.SubprogramDeclarationsContext):
        pass

    # Exit a parse tree produced by PascalParser#subprogramDeclarations.
    def exitSubprogramDeclarations(self, ctx:PascalParser.SubprogramDeclarationsContext):
        pass


    # Enter a parse tree produced by PascalParser#subprogramDeclaration.
    def enterSubprogramDeclaration(self, ctx:PascalParser.SubprogramDeclarationContext):
        pass

    # Exit a parse tree produced by PascalParser#subprogramDeclaration.
    def exitSubprogramDeclaration(self, ctx:PascalParser.SubprogramDeclarationContext):
        pass


    # Enter a parse tree produced by PascalParser#subprogramHead.
    def enterSubprogramHead(self, ctx:PascalParser.SubprogramHeadContext):
        pass

    # Exit a parse tree produced by PascalParser#subprogramHead.
    def exitSubprogramHead(self, ctx:PascalParser.SubprogramHeadContext):
        pass


    # Enter a parse tree produced by PascalParser#formalParameterList.
    def enterFormalParameterList(self, ctx:PascalParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by PascalParser#formalParameterList.
    def exitFormalParameterList(self, ctx:PascalParser.FormalParameterListContext):
        pass


    # Enter a parse tree produced by PascalParser#formalParameterGroup.
    def enterFormalParameterGroup(self, ctx:PascalParser.FormalParameterGroupContext):
        pass

    # Exit a parse tree produced by PascalParser#formalParameterGroup.
    def exitFormalParameterGroup(self, ctx:PascalParser.FormalParameterGroupContext):
        pass


    # Enter a parse tree produced by PascalParser#variable.
    def enterVariable(self, ctx:PascalParser.VariableContext):
        pass

    # Exit a parse tree produced by PascalParser#variable.
    def exitVariable(self, ctx:PascalParser.VariableContext):
        pass


    # Enter a parse tree produced by PascalParser#compoundStatement.
    def enterCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#compoundStatement.
    def exitCompoundStatement(self, ctx:PascalParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#statementList.
    def enterStatementList(self, ctx:PascalParser.StatementListContext):
        pass

    # Exit a parse tree produced by PascalParser#statementList.
    def exitStatementList(self, ctx:PascalParser.StatementListContext):
        pass


    # Enter a parse tree produced by PascalParser#statement.
    def enterStatement(self, ctx:PascalParser.StatementContext):
        pass

    # Exit a parse tree produced by PascalParser#statement.
    def exitStatement(self, ctx:PascalParser.StatementContext):
        pass


    # Enter a parse tree produced by PascalParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:PascalParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:PascalParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#caseStatement.
    def enterCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#caseStatement.
    def exitCaseStatement(self, ctx:PascalParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#caseElement.
    def enterCaseElement(self, ctx:PascalParser.CaseElementContext):
        pass

    # Exit a parse tree produced by PascalParser#caseElement.
    def exitCaseElement(self, ctx:PascalParser.CaseElementContext):
        pass


    # Enter a parse tree produced by PascalParser#caseLabelList.
    def enterCaseLabelList(self, ctx:PascalParser.CaseLabelListContext):
        pass

    # Exit a parse tree produced by PascalParser#caseLabelList.
    def exitCaseLabelList(self, ctx:PascalParser.CaseLabelListContext):
        pass


    # Enter a parse tree produced by PascalParser#constant.
    def enterConstant(self, ctx:PascalParser.ConstantContext):
        pass

    # Exit a parse tree produced by PascalParser#constant.
    def exitConstant(self, ctx:PascalParser.ConstantContext):
        pass


    # Enter a parse tree produced by PascalParser#procedureCall.
    def enterProcedureCall(self, ctx:PascalParser.ProcedureCallContext):
        pass

    # Exit a parse tree produced by PascalParser#procedureCall.
    def exitProcedureCall(self, ctx:PascalParser.ProcedureCallContext):
        pass


    # Enter a parse tree produced by PascalParser#argumentList.
    def enterArgumentList(self, ctx:PascalParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by PascalParser#argumentList.
    def exitArgumentList(self, ctx:PascalParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by PascalParser#ifStatement.
    def enterIfStatement(self, ctx:PascalParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#ifStatement.
    def exitIfStatement(self, ctx:PascalParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#whileStatement.
    def enterWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#whileStatement.
    def exitWhileStatement(self, ctx:PascalParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#repeatStatement.
    def enterRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#repeatStatement.
    def exitRepeatStatement(self, ctx:PascalParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#forStatement.
    def enterForStatement(self, ctx:PascalParser.ForStatementContext):
        pass

    # Exit a parse tree produced by PascalParser#forStatement.
    def exitForStatement(self, ctx:PascalParser.ForStatementContext):
        pass


    # Enter a parse tree produced by PascalParser#expression.
    def enterExpression(self, ctx:PascalParser.ExpressionContext):
        pass

    # Exit a parse tree produced by PascalParser#expression.
    def exitExpression(self, ctx:PascalParser.ExpressionContext):
        pass


    # Enter a parse tree produced by PascalParser#simpleExpression.
    def enterSimpleExpression(self, ctx:PascalParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by PascalParser#simpleExpression.
    def exitSimpleExpression(self, ctx:PascalParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by PascalParser#term.
    def enterTerm(self, ctx:PascalParser.TermContext):
        pass

    # Exit a parse tree produced by PascalParser#term.
    def exitTerm(self, ctx:PascalParser.TermContext):
        pass


    # Enter a parse tree produced by PascalParser#factor.
    def enterFactor(self, ctx:PascalParser.FactorContext):
        pass

    # Exit a parse tree produced by PascalParser#factor.
    def exitFactor(self, ctx:PascalParser.FactorContext):
        pass



del PascalParser