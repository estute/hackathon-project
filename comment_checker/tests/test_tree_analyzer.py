import ast
from _ast import (
    FunctionDef,
    Expr,
    Return,
    Name,
    Str,
    Load,
    arguments,
    arg
)

from ..tree_analyzer import (
    TreeAnalyzer,
    CommentedFunctionNode
)


def test_qualified_name():
    """
    verify that the TreeAnalyzer labels the functions and classes
    it finds with correctly formatted fully-qualified names
    """
    tree = TreeAnalyzer('non-existent-file.py')
    code_text = """
def foo(bar):
    return bar

class MyClass(object):

    def method_1(a):
        return a

    def method_2(b):
        return b
"""
    code = ast.parse(code_text)
    tree.visit(code)
    assert 'non-existent-file.py:foo' in tree._functions
    assert 'non-existent-file.py:MyClass' in tree._classes
    assert 'non-existent-file.py:MyClass.method_1' in tree._functions
    assert 'non-existent-file.py:MyClass.method_2' in tree._functions


def test_function_collected_properly():
    """
    Make sure that all of the pertinent components of a function
    are collected when the AST is parsed
    """
    tree = TreeAnalyzer('non-existent-file.py')
    code_text = """
garbage_variable = 3

def foo(bar):
    \"\"\"
    baz!
    \"\"\"
    return bar

class MyClass(object):

    def method_1(a):
        return a
"""
    code = ast.parse(code_text)
    tree.visit(code)
    expected_function = FunctionDef(
        name='foo',
        args=arguments(
            args=[arg(arg='bar', annotation=None)], vararg=None,
            kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
        ),
        body=[
            Expr(value=Str(s='\n    baz!\n    ')),
            Return(value=Name(id='bar', ctx=Load()))
        ],
        decorator_list=[],
        returns=None
    )
    assert tree._functions['non-existent-file.py:foo'].docstring == 'baz!'
    print(ast.dump(tree._functions['non-existent-file.py:foo'].node_ast))
    print(ast.dump(expected_function))
    assert tree._functions['non-existent-file.py:foo'].node_ast == expected_function