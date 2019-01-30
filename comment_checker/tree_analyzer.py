import ast
from _ast import ClassDef, FunctionDef


class TreeAnalyzer(ast.NodeVisitor):

    def __init__(self, source_name):
        """
        
        Arguments:
            source_name (str): 

        """
        super(ast.NodeVisitor, self)
        self.source_name = source_name
        self.current_level = [] 
        self._classes = {}
        self._functions = {}

    def visit_ClassDef(self, node):
        """
        blah
        """
        self.current_level.append(node.name)
        self._classes[self._qualified_node_name] = node
        self.generic_visit(node)
        self.current_level.pop()

    def visit_FunctionDef(self, node):
        """
        visit a python function definition in the AST
        """
        self.current_level.append(node.name)
        docstring = ast.get_docstring(node)
        function_node = CommentedFunctionNode(node, docstring)
        self._functions[self._qualified_node_name] = function_node
        self.generic_visit(node)
        self.current_level.pop()

    @property
    def _qualified_node_name(self):
        """
        the string format for the fully qualified name of the
        token/node. For example, if we have the following code in X.py:
        ```
            Class Y(object):
                
                def z(self):
                    pass
        ```
        the fully qualified name of of the Z function definition would be
        "X.py:Y.z"
        """
        return "{}:{}".format(
            self.source_name, '.'.join(self.current_level)
        )


class CommentedFunctionNode(object):
    """
    AST representation of a Python function, bundled with its docstring
    and inline comments
    """

    def __init__(self, node_ast, docstring):
        self.node_ast = node_ast
        self.docstring = docstring

    def __eq__(self):
        pass

    def __repr__(self):
        return self.node_ast.name
    
    def diff_code(self, other_node):
        """
        compare this CommentedFunctionNode to another, checking if there
        are any differences in the function body of the two functions
        """
        if not isinstance(other_node, CommentedFunctionNode):
            return False
        return self.node_ast.body == other_node.node_ast.body

    def diff_signature(self, other_node):
        """
        compare this CommentedFunctionNode to another, checking if there
        are any differences in the method signature of the two functions.
        """
        if not isinstance(other_node, CommentedFunctionNode):
            return False
        return self.node_ast.args == other_node.node_ast.args

    def diff_docstring(self, other_node):
        """
        compare this CommentedFunctionNode to another, checking if there
        are any differences in the docstring of the two functions.
        """
        # if not isinstance(other_node, CommentedFunctionNode):
            # return False
        return self.docstring == other_node.docstring
