#​ ​Edite ​a classe​ LoxTransformer​ nesse​ arquivo. Boa​ prova!
"""
Implementa o transformador da árvore sintática que converte entre as representações

    lark.Tree -> lox.ast.Node.

A resolução de vários exercícios requer a modificação ou implementação de vários
métodos desta classe.
"""

from typing import Callable

from lark import Transformer, v_args

from . import runtime as op
from .ast import *


def op_handler(op: Callable):
    """
    Fábrica de métodos que lidam com operações binárias na árvore sintática.

    Recebe a função que implementa a operação em tempo de execução.
    """

    def method(self, left, right):
        return BinOp(left, right, op)
    return method


@v_args(inline=True)
class LoxTransformer(Transformer):
    # Programa
    def program(self, *stmts):
        return Program(list(stmts))
    
    # Operações matemáticas básicas
    mul = op_handler(op.mul)
    div = op_handler(op.truediv)
    sub = op_handler(op.sub)
    add = op_handler(op.add)

    # Comparações
    gt = op_handler(op.gt)
    lt = op_handler(op.lt)
    ge = op_handler(op.ge)
    le = op_handler(op.le)
    eq = op_handler(op.eq)
    ne = op_handler(op.ne)

    def not_(self, expr):
        return UnaryOp(op.not_, expr)

    def neg(self, expr):
        return UnaryOp(op.neg, expr)
    
    # Outras expressões
    def call(self, name: Var, params: list):
        return Call(name.name, params)

    def params(self, *args):
        return list(args)

    def assign(self, name: Var, value: Expr):
        return Assign(name.name, value)

    # Comandos
    def var_def(self, name: Var, expr: Expr | None = None):
        return VarDef(name.name, expr)

    def print_cmd(self, expr):
        return Print(expr)

    def block(self, *stmts: Stmt):
        return Block(list(stmts))

    def while_cmd(self, cond: Expr, body: Stmt):
        return While(cond, body)

    def list_elems(self, *elems):
        return list(elems)

    def list(self, *elems):
        if len(elems) == 1 and isinstance(elems[0], list):
            elems = elems[0]
        return List(list(elems))

    def VAR(self, token):
        return Var(str(token))

    def NUMBER(self, token):
        return Literal(float(token))

    def STRING(self, token):
        return Literal(str(token)[1:-1])

    def NIL(self, _):
        return Literal(None)

    def BOOL(self, token):
        return Literal(token == "true")
