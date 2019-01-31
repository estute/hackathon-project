

class MyClass(object):
    

    def function1(self):
        """
        This function will remain unchanged,
        as will it's docstring, so do not expect
        anything
        """
        pass

    def function2(self, variable=False):
        """
        I will change the method signature of this
        function, but not the docstring, so it should be
        flagged
        """
        # I will change the default value of `variable`
        # which will have a drastic effect on this function
        if variable:
            return 1000000000
        else:
            return 1



def another_function(foo, bar):
    """
    I am going to update the code, but not the docstring,
    so this function should get flagged
    """
    baz = open('some-file', 'r').read()
    return baz

def boring_function(x):
    """
    I Changed what this function does!
    """
    return sum(range(1,100))

