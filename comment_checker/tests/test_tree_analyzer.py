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
    CommentedFunctionNode,
    compare_asts
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
    foo_body = tree._functions['non-existent-file.py:foo'].node_ast
    assert compare_asts(foo_body, expected_function)


def test_docstring_changes_detected():
    tree_a = TreeAnalyzer('non-existent-file.py')
    initial_code = """
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
    tree_a.visit(ast.parse(initial_code))

    tree_b = TreeAnalyzer('non-existent-file.py')
    unchanged_docstring_code = """
garbage_variable_list = [1, 3]

def foo(bar):
    \"\"\"
    baz!
    \"\"\"
    return bar

class MyClass(object):

    def method_1(a):
        return 'unrelated change'
"""
    tree_b.visit(ast.parse(unchanged_docstring_code))

    assert tree_a._functions['non-existent-file.py:foo'].diff_docstring(
        tree_b._functions['non-existent-file.py:foo']
    )

    tree_c = TreeAnalyzer('non-existent-file.py')
    changed_docstring_code = """
garbage_variable = 3

def foo(bar):
    \"\"\"
    I HAVE CHANGED THE TEXT HERE
    \"\"\"
    return bar

class MyClass(object):

    def method_1(a):
        return a
"""
    tree_c.visit(ast.parse(changed_docstring_code))

    assert not tree_a._functions['non-existent-file.py:foo'].diff_docstring(
        tree_c._functions['non-existent-file.py:foo']
    )
