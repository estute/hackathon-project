
from tree_analyzer import (
    TreeAnalyzer,
    CommentedFunctionNode
)
import os
import sys
import ast


def analyze_tree(file_name):
    print("Parsing {} into an AST".format(file_name))
    if not os.path.isfile(file_name):
        print("File {} does not exist".format(file_name))
        sys.exit(1)

    file_contents = open(file_name, 'r').read()
    tree = ast.parse(file_contents)
    analyzer = TreeAnalyzer(file_name)
    analyzer.visit(tree)
    return analyzer


def get_corresponding_function(function_name, tree, source_file):
    """
    given the fully qualified name of a function (source.py:Class.function),
    get the fully qualified name of the corresponding function from another
    AST, if present
    """

    def trim_function_name(function_name):
        return function_name.split(':')[1]

    def generate_qualified_name(source_file, function_name):
        return "{}:{}".format(source_file, function_name)

    print("Looking for {} in the other AST".format(function_name))
    trimmed_name = trim_function_name(function_name)
    if trim_function_name(function_name) in [trim_function_name(f) for f in tree._functions]:
        print("Found a match")
        return tree._functions[generate_qualified_name(source_file, trimmed_name)]
    else:
        print("Could not find a match. Skipping")
        return False

def main():

    old_file_name = os.getenv('OLD_FILE_NAME', 'data/old_version.py')
    new_file_name = os.getenv('NEW_FILE_NAME', 'data/new_version.py')
    old_tree = analyze_tree(old_file_name)
    new_tree = analyze_tree(new_file_name)

    for function_name, function in new_tree._functions.items():
        print("="*100)
        corr_func = get_corresponding_function(function_name, old_tree, old_file_name)

        if not corr_func:
            continue

        stale_doc_string = function.diff_docstring(corr_func)
        if stale_doc_string:
            print("Doc string is stale (hasn't changed) for {}".format(function_name))

        code_change = not function.diff_code(corr_func)
        signature_change = not function.diff_signature(corr_func)

        if not code_change and not signature_change:
            print("But the code didn't change. This is ok for now")

        if signature_change and stale_doc_string:
            print("The method signature of function {} changed between {} and {}. but the docstring did not!".format(function_name, old_file_name, new_file_name))
            print("Consider updating it")

        if code_change and stale_doc_string:
            print("The body of function {} changed between {} and {}. but the docstring did not!".format(function_name, old_file_name, new_file_name))
            print("Consider updating it")



if __name__ == "__main__":
    main()
